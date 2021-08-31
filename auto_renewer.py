from os import getenv, path, environ
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from helper_functions import is_due, parse_date, format_author
from emailer import Emailer
# from mime_email import MimeEmail
from library_book import LibraryBook
from dotenv import Dotenv
dotenv = Dotenv(path.join(path.dirname(__file__), ".env")) # Of course, replace by your correct path
environ.update(dotenv)

RECEIVER = getenv('RECEIVER_ADDRESS')


class AutoRenewer:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = selenium.webdriver.Chrome(getenv('CHROME_DRIVER_LOCATION'), options=chrome_options)
        self.emailer = Emailer('smtp.gmail.com')

    def run(self):
        try:
            self.log_in()
            self.navigate_to_holds()
            table_rows = self.get_table_rows()
            all_books = self.books_from_table_rows(table_rows)
            books_due = self.get_books_due(all_books)
            self.renew_books(books_due)
            self.log_out()
        finally:
            self.driver.close()

    def log_in(self):
        try:
            self.driver.get(getenv('LIBRARY_URL'))
            login_button = self.driver.find_element_by_link_text('Log In')
            login_button.click()
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, 'j_username'))
            ).send_keys(getenv('USER_NAME'))
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, 'j_password'))
            ).send_keys(getenv('PASSWORD'))
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, 'submit_0'))
            ).click()
            self.driver.implicitly_wait(1)

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error logging in. {e}')

    def log_out(self):
        try:
            # click the log out button
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[1]/div[2]/a').click()
            # confirm log out
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.ID, 'okButton'))
            ).click()

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error logging out. {e}')

    def navigate_to_holds(self):
        """ navigates to the holds section from the home page """
        try:
            # click my account tab
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="libInfoContainer"]/div[4]/a'))
            ).click()
            # click holds tab
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="ui-id-16"]'))
            ).click()

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error navigating to holds page. {e}')

    def get_table_rows(self):
        table_rows = []
        try:
            self.driver.find_element_by_xpath('//*[@id="myCheckouts_checkoutslistnonmobile_table"]/tbody/tr')
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error getting table rows. {e}')
        return table_rows

    def books_from_table_rows(self, table_rows):
        books = []
        try:
            for row in table_rows:
                title = row.find_element_by_class_name('hideIE').text
                author = row.find_element_by_class_name('checkouts_author').text
                due_date = row.find_element_by_class_name('checkoutsDueDate').text
                times_renewed = row.find_element_by_class_name('checkoutsRenewCount').text
                check_box = row.find_element_by_class_name('checkoutsCoverArt') \
                    .find_element_by_class_name('checkoutsCheckbox')
                book = LibraryBook(title, format_author(author), due_date, times_renewed, check_box)
                books.append(book)
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error getting book info from table rows. {e}')
        return books

    def get_books_due(self, books):
        books_due = []
        for book in books:
            due_date = parse_date(book.due_date)
            if is_due(due_date):
                books_due.append(book)
        return books_due

    def renew_books(self, books_due):
        try:
            if len(books_due) > 0:
                # select each book
                for book in books_due:
                    book.check_box.click()

                # click the submit button
                self.driver.find_element_by_xpath(
                  '/html/body/div[6]/div[1]/div[4]/div/div[2]/div/div[1]/div['
                  '2]/div/div/div[1]/div/div[2]/form/div[2]/div[2]/input').click()
                # click the confirmation button
                WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div[2]/input[1]'))
                ).click()

                self.send_confirmation_email(renewed_books=books_due)

        except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
            # send error message via email
            self.emailer.send_email(RECEIVER, f'Error renewing books. {e}')

    def send_confirmation_email(self, renewed_books):
        # TODO: create detailed HTML message (as a list or table)
        #  confirming which books were renewed with their due dates
        # send email confirming renewal
        self.emailer.send_email(RECEIVER, f'{len(renewed_books)} books renewed.')


def main():
    auto_renewer = AutoRenewer()
    auto_renewer.run()


if __name__ == '__main__':
    main()
