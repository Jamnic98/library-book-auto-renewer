from os import getenv
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from helper_functions import is_due, parse_date
from dotenv import load_dotenv
load_dotenv()


class AutoRenewer:
    def __init__(self):
        self.driver = selenium.webdriver.Chrome(getenv('CHROME_DRIVER_LOCATION'))

    def run(self):
        try:
            self.log_in()
            self.navigate_to_holds()
            # self.renew_books(self.get_books_due())
            self.log_out()
        finally:
            self.driver.close()

    def log_in(self):
        try:
            self.driver.get(getenv('LIBRARY_URL'))
            login_button = self.driver.find_element_by_link_text('Log In')
            login_button.click()
            self.driver.implicitly_wait(10)
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'j_username'))
            ).send_keys(getenv('USER_NAME'))
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'j_password'))
            ).send_keys(getenv('PASSWORD'))
            self.driver.find_element_by_id('submit_0').click()

        except (TimeoutException, NoSuchElementException) as e:
            # TODO: send error message email (error logging in)
            print(str(e))
            pass

    def log_out(self):
        try:
            # click the log out button
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[1]/div[2]/a').click()
            # confirm log out
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.ID, 'okButton'))
            ).click()

        except (TimeoutException, NoSuchElementException) as e:
            # TODO: send error message email (error logging out)
            print(str(e))
            pass

    def navigate_to_holds(self):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/a'))
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[1]/div[4]/div/ul/li[2]/a'))
            ).click()

        except (TimeoutException, NoSuchElementException) as e:
            # TODO: send error message email (error navigating to holds)
            print(str(e))
            pass

    def get_books_due(self):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/a'))
            ).click()
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[1]/div[4]/div/ul/li[2]/a'))
            ).click()

        except NoSuchElementException as e:
            # TODO: send error message email (error finding which books are due)
            print(str(e))
            pass

        books_due = []
        table_rows = self.driver.find_elements_by_xpath(
            '/html/body/div[6]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div/div['
            '1]/div/div[2]/form/div[2]/table/tbody/tr'
        )
        for book_row in table_rows:
            due_date = parse_date(book_row.find_element_by_class_name('checkoutsDueDate').text)
            if is_due(due_date):
                books_due.append(book_row)
        return books_due

    def renew_books(self, books_due):
        try:
            if len(books_due):
                for book_row in books_due:
                    # check the selection box
                    book_row \
                        .find_element_by_class_name('checkoutsCoverArt') \
                        .find_element_by_class_name('checkoutsCheckbox') \
                        .click()

                # click the submit button
                self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[4]/div/div[2]/div/div[1]/div['
                                                  '2]/div/div/div[1]/div/div[2]/form/div[2]/div[2]/input').click()

                # click the confirmation button
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div[2]/input[1]'))
                ).click()

        except (TimeoutException, NoSuchElementException) as e:
            # TODO: send error message email (error renewing books)
            print(str(e))
            pass


def main():
    auto_renewer = AutoRenewer()
    auto_renewer.run()


if __name__ == '__main__':
    main()
