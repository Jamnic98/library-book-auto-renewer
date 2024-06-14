from app.logger import Logger
from os import getenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementNotInteractableException, SessionNotCreatedException
from utlis.helper_functions import get_books_due, send_confirmation_email
from app.library_book import LibraryBook
# from app.emailer import send_email
from app.web_driver import WebDriver
from dotenv import load_dotenv
load_dotenv()


class AutoRenewer:
    def __init__(self, browser_name='chrome'):
        try:
            self.logger = Logger()
            self.driver = WebDriver(browser_name)
            self.driver.get(getenv('LIBRARY_URL'))
            self.driver.implicitly_wait(10)

        except SessionNotCreatedException:
            error_msg = 'Failed to create session'
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)
            
    def run(self) -> None:
        try:
            self._log_in()
            self._navigate_to_holds()
            all_books = self._books_from_table_rows()
            books_due = get_books_due(all_books)
            if len(books_due) > 0:
                self._renew_books(books_due)
                updated_books = self._books_from_table_rows()
                updated_books_due = get_books_due(updated_books)
                renewed_books = [book for book in books_due if book not in updated_books_due]
                if len(updated_books_due) > 0:
                    # failed to renew some books
                    send_confirmation_email(renewed_books, updated_books_due)
                else:
                    send_confirmation_email(renewed_books)
            self._log_out()
            # self.logger.info('Program ran successfully')
        finally:
            self.driver.close()

    def _log_in(self) -> None:
        self.logger.info('Attempting to log in')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
            self.driver.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[6]')))
            # enter credentials
            self.driver.find_element(By.ID, 'j_username').send_keys(getenv('USER_NAME'))
            self.driver.find_element(By.ID, 'j_password').send_keys(getenv('PASSWORD'))
            self.driver.find_element(By.ID, 'submit_0').click()
            self.logger.info('Logged in')
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log in: {e}'
            # send_email(error_msg)
            self.logger.error(error_msg)
            exit(1)

    def _log_out(self) -> None:
        self.logger.info('Attempting to log out')
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'okButton'))).click()
            self.logger.info('Logged out')
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to log out: {e}'
            # send_email(error_msg)
            self.logger(error_msg)
            exit(1)

    def _navigate_to_holds(self) -> None:
        self.logger.info('Navigating to holds')
        """ navigate to holds section from home page once logged in"""
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
            self.logger(error_msg)
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
            self.logger(error_msg)
            exit(1)

    def _renew_books(self, books_due: list[LibraryBook]) -> None:
        self.logger.info(f'Attempting to renew {len(books_due)} books')
        try:
            # click checkbox to select each book on the page
            for book in books_due:
                book.check_box.click()
            # click the 'Renew' button
            self.driver.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_topCheckoutsRenewButton'))
            ).click()
            # click the 'Yes' (confirmation) button
            self.driver.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_checkoutsDialogConfirm'))
            ).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            error_msg = f'Failed to renew books: {e}'
            # send_email(error_msg)
            self.logger(error_msg)
            exit(1)
