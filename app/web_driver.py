from os import getenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.os_manager import ChromeType

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")


class WebDriver:
    def __new__(cls, browser_name: str):
        if browser_name == 'chrome':
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=chrome_options
            )
        elif browser_name == 'chromium':
            driver = webdriver.Chrome(
                service=ChromiumService(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                ),
                options=chrome_options
            )
        else:
            # Specify the path to the downloaded ChromeDriver
            chrome_driver_path = getenv('CHROME_DRIVER_LOCATION')
            # Set up the Chrome driver with the specified path
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.wait = WebDriverWait(driver, 5)
        return driver
