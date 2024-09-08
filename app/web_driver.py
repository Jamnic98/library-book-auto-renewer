from selenium.webdriver import Chrome, ChromeService, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")


class WebDriver:
    def __new__(cls):
        service = ChromeService()
        driver = Chrome(service=service, options=chrome_options)
        driver.wait = WebDriverWait(driver, 5)
        return driver
