import unittest
from datetime import date
from helper_functions import is_due, parse_date


class TestHelperFunctions(unittest.TestCase):

    def test_is_due(self):
        self.assertEqual(is_due(date(1998, 1, 31)), False)  # past
        self.assertEqual(is_due(date.today()), True)  # present
        self.assertEqual(is_due(date(3000, 1, 1)), False)  # future

    def test_parse_date(self):
        self.assertEqual(parse_date('01/01/2021'), date(2021, 1, 1))
        self.assertEqual(parse_date('31/01/1998'), date(1998, 1, 31))
