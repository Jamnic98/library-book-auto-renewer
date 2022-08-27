import unittest
from datetime import date
from helper_functions import get_next_due_date, get_books_due
from library_book import LibraryBook

books = [
    LibraryBook('book_1', 'author_1', '31/1/1998', '1', None),
    LibraryBook('book_2', 'author_2', date.today().strftime('%d/%m/%y'), '2', None),
    LibraryBook('book_3', 'author_3', '1/1/3000', '3', None),
    LibraryBook('book_4', 'author_4', '4/4/4444', '4', None),
]


class TestHelperFunctions(unittest.TestCase):
    def test_get_books_due(self):
        books_due = get_books_due(books)
        self.assertIn(books[0], books_due)
        self.assertIn(books[1], books_due)

    def test_get_next_due_date(self):
        self.assertEqual(get_next_due_date(books), date(3000, 1, 1))


if __name__ == '__main__':
    unittest.main()
