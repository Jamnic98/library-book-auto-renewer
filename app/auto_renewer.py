from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementNotInteractableException, SessionNotCreatedException
from app.library_book import LibraryBook
from app.web_driver import WebDriver
from app.emailer import Emailer
from utlis.logger import logger
from utlis.helper_functions import get_books_due
from utlis.settings import config

class AutoRenewer:
    def __init__(self):
        try:
            # setup logging
            self.logger = logger
            # set up emailer
            self.emailer = Emailer()
            # set up web driver
            self.driver = WebDriver()
        except SessionNotCreatedException:
            error_msg = 'Failed to create session'
            self.logger.error(error_msg)
            self.emailer.send_email(error_msg)
            exit(1)
            
    def run(self) -> None:
        try:
            self.__go_to_home_page()
            self.__log_in()
            all_books = self.__fetch_books()
            books_due = get_books_due(all_books)
            if renewed_books := self.__renew_books(books_due):
                # all_books = self.__books_from_table()
                self.__send_confirmation_email(renewed_books)
            self.__log_out()
        finally:
            self.driver.close()

    def __go_to_home_page(self) -> None:
        self.driver.get(config['LIBRARY_URL'])
        self.driver.wait.until(ec.presence_of_element_located((By.ID, 'logo_container')))

    def __log_in(self) -> None:
        self.logger.info('Logging in')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
            self.driver.wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]')))
            # enter credentials
            self.driver.find_element(By.ID, 'j_username').send_keys(config['USER_NAME'])
            self.driver.find_element(By.ID, 'j_password').send_keys(config['PASSWORD'])
            self.driver.find_element(By.ID, 'submit_0').click()

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log in: {e}'
            self.logger.error(error_msg)
            self.emailer.send_email(error_msg)
            exit(1)


    def __fetch_books(self):
        self.__navigate_to_holds()
        return self.__books_from_table()

    def __navigate_to_holds(self) -> None:
        """ navigate to holds section from home page once logged in"""
        self.logger.info('Navigating to holds page')
        try:
            # click 'My Account' tab
            self.driver.wait.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="libInfoContainer"]/div[4]/a'))
            ).click()
            # click 'Loans / Renewals' tab
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'ui-id-16'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to navigate to holds: {e}'
            self.logger.error(error_msg)
            self.emailer.send_email(error_msg)
            exit(1)

    def __renew_books(self, books_due: list[LibraryBook]) -> list[LibraryBook]:
        if len(books_due) > 0:
            try:
                self.logger.info(f'Attempting to renew {len(books_due)} books')
                # click checkbox to select each book on the page
                for book in books_due:
                    book.check_box.click()
                # click the 'Renew' button
                self.driver.wait.until(
                    ec.element_to_be_clickable(
                        (By.ID, 'myCheckouts_checkoutslistnonmobile_topCheckoutsRenewButton')
                    )
                ).click()
                # click the 'Yes' (confirmation) button
                self.driver.wait.until(
                    ec.element_to_be_clickable(
                        (By.ID, 'myCheckouts_checkoutslistnonmobile_checkoutsDialogConfirm')
                    )
                ).click()
                # return a list of books which have been renewed
                updated_books = self.__books_from_table()
                return [book for book in updated_books if book in books_due]

            except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                error_msg = f'Failed to renew books: {e}'
                self.logger.error(error_msg)
                self.emailer.send_email(error_msg)

        else:
            self.logger.info(f'No books are due')

        return []

    def __books_from_table(self) -> list[LibraryBook]:
        self.logger.info('Collecting information on current holds')
        books = []
        try:
            table_rows = self.driver.find_elements(
                By.XPATH, '//*[@id="myCheckouts_checkoutslistnonmobile_table"]/tbody/tr'
            )
            for row in table_rows:
                title = row.find_element(By.CLASS_NAME, 'hideIE').text
                author = row.find_element(By.CLASS_NAME, 'checkouts_author').text
                due_date = row.find_element(By.CLASS_NAME, 'checkoutsDueDate').text
                times_renewed = row.find_element(By.CLASS_NAME, 'checkoutsRenewCount').text
                check_box = row.find_element(By.CLASS_NAME, 'checkoutsCoverArt') \
                    .find_element(By.CLASS_NAME, 'checkoutsCheckbox')
                book = LibraryBook(title, author, due_date, times_renewed, check_box)
                books.append(book)
            return books

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to get books from table rows: {e}'
            self.logger.error(error_msg)
            self.emailer.send_email(error_msg)
            exit(1)

    def __send_confirmation_email(self, _books_held: list[LibraryBook]):  #, renewed_books: list[LibraryBook]):
        self.emailer.send_email()

    def __log_out(self) -> None:
        self.logger.info('Logging out')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'okButton'))).click()

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log out: {e}'
            self.logger.error(error_msg)
            self.emailer.send_email(error_msg)
            exit(1)
