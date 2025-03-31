from datetime import date
from app.models.library_book import LibraryBook, get_next_due_date, get_books_due

books = [
    LibraryBook('book_1', 'author_1', '31/1/1998', '1'),
    LibraryBook('book_2', 'author_2', date.today().strftime('%d/%m/%y'), '2'),
    LibraryBook('book_3', 'author_3', '1/1/3000', '3'),
    LibraryBook('book_4', 'author_4', '4/4/4444', '4'),
]


class TestHelperFunctions:
    def test_get_books_due(self):
        books_due = get_books_due(books)
        assert books[0] in books_due
        assert books[1] in books_due

    def test_get_next_due_date(self):
        assert get_next_due_date(books) == date(3000, 1, 1)
