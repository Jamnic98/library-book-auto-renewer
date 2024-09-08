from selenium.webdriver import Chrome, ChromeService, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from utlis.settings import config

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")


class WebDriver:
    def __new__(cls):
        # Specify the path to the downloaded ChromeDriver
        chrome_driver_path = config['CHROME_DRIVER_LOCATION']
        if chrome_driver_path:
            # Set up the Chrome driver with the specified path
            service = Service(chrome_driver_path)
        else:
            service = ChromeService()
        driver = Chrome(service=service, options=chrome_options)
        driver.wait = WebDriverWait(driver, 10)
        return driver
