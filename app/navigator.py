# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
#     ElementNotInteractableException, SessionNotCreatedException
# from app.library_book import LibraryBook
# from app.web_driver import WebDriver
# from app.emailer import Emailer
# from utlis.logger import logger
# from utlis.helper_functions import get_books_due
# from utlis.settings import config
#
# class Navigator:
#     def __init__(self):
#         self.logger = logger
#         # set up web driver
#         self.driver = WebDriver()
#
#     def __log_in(self) -> None:
#         self.logger.info('Logging in')
#         try:
#             self.driver.wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'Log In'))).click()
#             self.driver.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[6]')))
#             # enter credentials
#             self.driver.find_element(By.ID, 'j_username').send_keys(config['USER_NAME'])
#             self.driver.find_element(By.ID, 'j_password').send_keys(config['PASSWORD'])
#             self.driver.find_element(By.ID, 'submit_0').click()
#         except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
#             error_msg = f'Failed to log in: {e}'
#             self.logger.error(error_msg)
#             self.emailer.send_email(error_msg)
#             exit(1)