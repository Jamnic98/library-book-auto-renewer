from auto_renewer import AutoRenewer
import unittest
from dotenv import load_dotenv
load_dotenv()


class TestAutoRenewer(unittest.TestCase):

    auto_renewer = None

    @classmethod
    def setUpClass(cls):
        cls.auto_renewer = AutoRenewer()
        cls.auto_renewer.log_in()

    def test_loads_page(self):
        self.assertIn("Library Links", self.auto_renewer.driver.title)
        welcome_text = self.auto_renewer.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[1]/div/div[1]/span').text
        self.assertIn('Welcome', welcome_text)

    @ classmethod
    def tearDownClass(cls):
        cls.auto_renewer.log_out()
        cls.auto_renewer.driver.close()
        del cls.auto_renewer


if __name__ == "__main__":
    unittest.main()
