from app.auto_renewer import AutoRenewer
from selenium.webdriver.common.by import By


def test_loads_page():
    auto_renewer = AutoRenewer()
    auto_renewer.log_in()

    assert 'Library Links' in auto_renewer.driver.title
    welcome_text = auto_renewer.driver.find_element(
        By.XPATH,
        '/html/body/div[2]/div/div/div[1]/div/div[1]/span'
    ).text
    assert 'Welcome' in welcome_text

    auto_renewer.log_out()
    auto_renewer.driver.close()
    del auto_renewer
