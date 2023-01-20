from os import getenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementNotInteractableException, StaleElementReferenceException, SessionNotCreatedException
from utlis.helper_functions import get_books_due, send_confirmation_email
from app.library_book import LibraryBook
from app.emailer import send_email
from app.web_driver import WebDriver
from dotenv import load_dotenv
load_dotenv()


class AutoRenewer:
    def __init__(self, browser_name):
        try:
            self.driver = WebDriver(browser_name)
            self.driver.get(getenv('LIBRARY_URL'))
        except SessionNotCreatedException:
            error_msg = 'Failed to create session.'
            send_email(error_msg)

    def log_in(self) -> None:
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
            # wait for modal to open
            self.driver.wait.until(ec.presence_of_element_located((By.ID, 'ui-id-1')))
            # enter credentials
            self.driver.find_element(By.ID, 'j_username').send_keys(getenv('LIBRARY_USER_NAME'))
            self.driver.find_element(By.ID, 'j_password').send_keys(getenv('LIBRARY_PASSWORD'))
            self.driver.find_element(By.ID, 'submit_0').click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
            error_msg = F'Log-in failed. {e}'
            send_email(error_msg)

    def log_out(self) -> None:
        try:
            self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'okButton'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
            error_msg = F'Log-out failed. {e}'
            send_email(error_msg)

    def navigate_to_holds(self) -> None:
        """ navigate to holds section from home page once logged in"""
        try:
            # click 'My Account' tab
            self.driver.wait.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="libInfoContainer"]/div[4]/a'))
            ).click()
            # click 'Loans / Renewals' tab
            self.driver.wait.until(ec.element_to_be_clickable((By.ID, 'ui-id-16'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
            error_msg = F'Failed to navigate to holds. {e}'
            send_email(error_msg)

    def books_from_table_rows(self) -> list[LibraryBook]:
        books = []
        try:
            table_rows = self.driver.wait.until(
              ec.presence_of_all_elements_located((By.XPATH, '//*[@id="myCheckouts_checkoutslistnonmobile_table"]/tbody/tr'))
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
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
            error_msg = F'Failed to get books from table rows. {e}'
            send_email(error_msg)
        return books

    def renew_books(self, books_due: list[LibraryBook]) -> None:
        for book in books_due:
            book.check_box.click()
        try:
            # click the 'Renew' button
            self.driver.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_topCheckoutsRenewButton'))
            ).click()
            # click the 'Yes' (confirmation) button
            self.driver.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_checkoutsDialogConfirm'))
            ).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
            error_msg = F'Failed to renew books. {e}'
            send_email(error_msg)

    def run(self) -> None:
        try:
            self.log_in()
            self.navigate_to_holds()
            all_books = self.books_from_table_rows()
            if len(books_due:= get_books_due(all_books)) > 0:
                self.renew_books(books_due)
                self.driver.get(getenv('LIBRARY_URL'))
                self.navigate_to_holds()
                updated_books = self.books_from_table_rows()
                updated_books_due = get_books_due(updated_books)
                renewed_books = [book for book in books_due if book not in updated_books_due]
                if len(updated_books_due) > 0:
                    # failed to renew some books
                    send_confirmation_email(renewed_books, updated_books_due)
                else:
                    send_confirmation_email(renewed_books)
            self.log_out()
        finally:
            self.driver.close()
