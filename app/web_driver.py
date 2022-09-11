from os import getenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("window-size=1400,1500")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")


class WebDriver:
    def __new__(cls, browser_name: str):
        driver = None
        browser_name = browser_name.lower()
        try:
            if browser_name == 'chrome':
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options
                )
            elif browser_name == 'chromium':
                driver = webdriver.Chrome(
                    service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                    options=chrome_options
                )
        except ValueError:
            driver = webdriver.Chrome(service=Service(executable_path=getenv("CHROME_DRIVER_LOCATION")))
        driver.wait = WebDriverWait(driver, 10)
        return driver
