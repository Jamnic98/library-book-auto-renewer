import unittest
from datetime import date
from helper_functions import get_next_due_date
from library_book import LibraryBook, format_author, parse_date

books = [
    LibraryBook('book_1', 'author_1', '31/1/1998', '1', None),
    LibraryBook('book_2', 'author_2', date.today().strftime('%d/%m/%y'), '2', None),
    LibraryBook('book_3', 'author_3', '1/1/3000', '3', None),
]


class TestLibraryBook(unittest.TestCase):

    def test_parse_date(self):
        self.assertEqual(parse_date('01/01/2021'), date(2021, 1, 1))
        self.assertEqual(parse_date('31/01/98'), date(1998, 1, 31))
        self.assertEqual(parse_date('18/09/2021 23:59'), date(2021, 9, 18))

    def test_format_author(self):
        self.assertEqual(format_author('Hart, Kevin'), 'Kevin Hart')
        self.assertEqual(format_author('Covey, Stephen R.'), 'Stephen R. Covey')
        self.assertEqual(format_author('Roberts, Alice, 1973-'), 'Alice Roberts')
        self.assertEqual(
            format_author('Huffington, Arianna Stassinopoulos, 1950-'),
            'Arianna Stassinopoulos Huffington'
        )

    def test_is_due(self):
        self.assertEqual(books[0].is_due(), True)
        self.assertEqual(books[1].is_due(), True)
        self.assertEqual(books[2].is_due(), False)


if __name__ == '__main__':
    unittest.main()
