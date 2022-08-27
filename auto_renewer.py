from os import getenv
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementNotInteractableException, SessionNotCreatedException

from helper_functions import get_books_due, get_next_due_date, send_confirmation_email
from library_book import LibraryBook, format_due_date
from emailer import send_email
from dotenv import load_dotenv
load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')


class AutoRenewer:
    def __init__(self):
        try:
            self.driver = selenium.webdriver.Chrome(getenv('CHROME_DRIVER_LOCATION'), options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.driver.get(getenv('LIBRARY_URL'))
            self.driver.implicitly_wait(10)
        except SessionNotCreatedException:
            send_email('Failed to create session.')
            exit(1)

    def log_in(self) -> None:
        try:
            self.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
            self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[6]')))
            # enter credentials
            self.driver.find_element_by_id('j_username').send_keys(getenv('LIBRARY_USER_NAME'))
            self.driver.find_element_by_id('j_password').send_keys(getenv('LIBRARY_PASSWORD'))
            self.driver.find_element_by_id('submit_0').click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            send_email(f'Log in failed. {e}')
            exit(1)

    def log_out(self) -> None:
        try:
            self.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
            self.wait.until(ec.element_to_be_clickable((By.ID, 'okButton'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            send_email(f'Log out failed. {e}')
            exit(1)

    def navigate_to_holds(self) -> None:
        """ navigate to holds section from home page once logged in"""
        try:
            # click 'My Account' tab
            self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="libInfoContainer"]/div[4]/a'))).click()
            # click 'Loans / Renewals' tab
            self.wait.until(ec.element_to_be_clickable((By.ID, 'ui-id-16'))).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            send_email(f'Failed to navigate to holds. {e}')
            exit(1)

    def books_from_table_rows(self) -> list[LibraryBook]:
        books = []
        try:
            table_rows = self.driver.find_elements_by_xpath(
                '//*[@id="myCheckouts_checkoutslistnonmobile_table"]/tbody/tr'
            )
            for row in table_rows:
                title = row.find_element_by_class_name('hideIE').text
                author = row.find_element_by_class_name('checkouts_author').text
                due_date = row.find_element_by_class_name('checkoutsDueDate').text
                times_renewed = row.find_element_by_class_name('checkoutsRenewCount').text
                check_box = row.find_element_by_class_name('checkoutsCoverArt') \
                    .find_element_by_class_name('checkoutsCheckbox')

                book = LibraryBook(title, author, due_date, times_renewed, check_box)
                books.append(book)
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            send_email(f'Error getting books from table rows. {e}')
            exit(1)
        return books

    def renew_books(self, books_due: list[LibraryBook]) -> None:
        for book in books_due:
            book.check_box.click()
        try:
            # click the 'Renew' button
            self.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_topCheckoutsRenewButton'))
            ).click()
            # click the 'Yes' (confirmation) button
            self.wait.until(
                ec.element_to_be_clickable((By.ID, 'myCheckouts_checkoutslistnonmobile_checkoutsDialogConfirm'))
            ).click()
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            send_email(f'Error renewing books. {e}')
            exit(1)

    def run(self) -> None:
        try:
            self.log_in()
            self.navigate_to_holds()
            all_books = self.books_from_table_rows()
            books_due = get_books_due(all_books)
            if len(books_due) > 0:
                self.renew_books(books_due)
                updated_books = self.books_from_table_rows()
                updated_books_due = get_books_due(updated_books)
                renewed_books = [book for book in books_due if book not in updated_books_due]
                if len(updated_books_due) > 0:
                    send_confirmation_email(renewed_books, updated_books_due)
                else:
                    send_confirmation_email(renewed_books)
            self.log_out()
        finally:
            self.driver.close()


def main():
    auto_renewer = AutoRenewer()
    auto_renewer.run()


if __name__ == '__main__':
    main()
