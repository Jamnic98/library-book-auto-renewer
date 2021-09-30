import unittest
from datetime import date
from helper_functions import is_due, parse_date, format_author, get_next_due_date
from library_book import LibraryBook


class TestHelperFunctions(unittest.TestCase):

    def test_is_due(self):
        self.assertEqual(is_due(date(1998, 1, 31)), False)  # past
        self.assertEqual(is_due(date.today()), True)  # present
        self.assertEqual(is_due(date(3000, 1, 1)), False)  # future

    def test_parse_date(self):
        self.assertEqual(parse_date('01/01/2021'), date(2021, 1, 1))
        self.assertEqual(parse_date('31/01/98'), date(1998, 1, 31))
        self.assertEqual(parse_date('18/09/2021 23:59'), date(2021, 9, 18))

    def test_format_author(self):
        self.assertEqual(format_author('Hart, Kevin'), 'Kevin Hart')
        self.assertEqual(format_author('Covey, Stephen R.'), 'Stephen R. Covey')

    def test_get_next_due_date(self):
        books = [
          LibraryBook('book1', 'author1', date(1998, 1, 31), 1, None),
          LibraryBook('book2', 'author2', date(2002, 6, 3), 1, None),
          LibraryBook('book2', 'author2', date(2012, 1, 1), 1, None),
        ]
        self.assertEqual(get_next_due_date(books), date(1998, 1, 31))


if __name__ == '__main__':
    unittest.main()
