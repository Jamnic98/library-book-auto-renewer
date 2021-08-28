import os
from datetime import date
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv
load_dotenv()


class AutoRenewer:
    def __init__(self):
        self.driver = selenium.webdriver.Chrome('C:\\Users\\jamie\\chromedriver.exe')
        self.driver.get("https://libraries.havering.gov.uk/client/en_GB/havering/")

    def run(self):
        self.log_in()
        self.navigate_to_holds()
        self.renew_library_holds()
        self.log_out()

    def log_in(self):
        login_button = self.driver.find_element_by_link_text('Log In')
        login_button.click()
        self.driver.find_element_by_id('j_username').send_keys(os.getenv('USER_NAME'))
        self.driver.find_element_by_id('j_password').send_keys(os.getenv('PASSWORD'))
        self.driver.find_element_by_id('submit_0').click()

    def log_out(self):
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[1]/div[2]/a').click()

    def navigate_to_holds(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[1]/div[4]/a'))
        ).click()
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[1]/div[4]/div/ul/li[2]/a'))
        ).click()

    def renew_library_holds(self):
        table_rows = self.driver.find_elements_by_xpath(
            '/html/body/div[6]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div/div['
            '1]/div/div[2]/form/div[2]/table/tbody/tr'
        )

        if len(table_rows):
            books_due = 0
            for row in table_rows:
                due_date = parse_date(row.find_element_by_class_name('checkoutsDueDate').text)
                if is_due(due_date):
                    books_due += 1
                    row \
                        .find_element_by_class_name('checkoutsCoverArt') \
                        .find_element_by_class_name('checkoutsCheckbox') \
                        .click()

            if books_due > 0:
                self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[4]/div/div[2]/div/div[1]/div['
                                                  '2]/div/div/div[1]/div/div[2]/form/div[2]/div[2]/input').click()
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div[2]/input[1]'))
                ).click()


def parse_date(due_date_string):
    full_due_date = due_date_string.split('/')
    due_date = date(int(full_due_date[2]), int(full_due_date[1]), int(full_due_date[0]))
    return due_date


def is_due(due_date):
    return (due_date - date.today()).days == 0


def main():
    auto_renewer = AutoRenewer()
    auto_renewer.run()


if __name__ == '__main__':
    main()
