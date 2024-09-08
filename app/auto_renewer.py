from os import getenv
from app.emailer import Emailer
from app.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementNotInteractableException, SessionNotCreatedException
from utlis.helper_functions import get_books_due
from app.library_book import LibraryBook
from app.web_driver import WebDriver


class AutoRenewer:
    def __init__(self):
        try:
            # setup logging
            self.logger = logger
            # set up emailer
            self.emailer = Emailer()
            # setup driver
            self.driver = WebDriver()
            self.driver.get(getenv('LIBRARY_URL'))
            self.driver.implicitly_wait(5)
        except SessionNotCreatedException:
            error_msg = 'Failed to create session'
            self.emailer.send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)
            
    def run(self) -> None:
        try:
            self._log_in()
            all_books = self._fetch_books()
            self._renew_books(all_books)
            # if renewed_books:
            #     self.emailer.send_email()
            self._log_out()
        finally:
            self.driver.close()

    def _fetch_books(self):
        self._navigate_to_holds()
        return self._books_from_table_rows()

    def _log_in(self) -> None:
        self.logger.info('Logging in')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
            self.driver.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[6]')))
            # enter credentials
            self.driver.find_element(By.ID, 'j_username').send_keys(getenv('USER_NAME'))
            self.driver.find_element(By.ID, 'j_password').send_keys(getenv('PASSWORD'))
            self.driver.find_element(By.ID, 'submit_0').click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log in: {e}'
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)

    def _log_out(self) -> None:
        self.logger.info('Logging out')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'okButton'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log out: {e}'
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)

    def _navigate_to_holds(self) -> None:
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
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)

    def _books_from_table_rows(self) -> list[LibraryBook]:
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
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)

    def _renew_books(self, all_books: list[LibraryBook]) -> list[LibraryBook]:
        try:
            books_due = get_books_due(all_books)
            if len(books_due) > 0:
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
                updated_books = self._books_from_table_rows()
                return [book for book in updated_books if book in books_due]

            else:
                self.logger.info(f'No books are due')

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to renew books: {e}'
            # send_email(error_msg)
            self.logger.error(error_msg)

        return []
