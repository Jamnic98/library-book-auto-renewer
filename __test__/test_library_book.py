from datetime import date
from app.models.library_book import LibraryBook, format_author, parse_date

books = [
    LibraryBook('book_1', 'author_1', '31/1/1998', '1'),
    LibraryBook('book_2', 'author_2', date.today().strftime('%d/%m/%y'), '2'),
    LibraryBook('book_3', 'author_3', '1/1/3000', '3'),
]


class TestLibraryBook:
    def test_parse_date(self):
        assert parse_date('01/01/2021') == date(2021, 1, 1)
        assert parse_date('31/01/98') == date(1998, 1, 31)
        assert parse_date('18/09/2021 23:59') == date(2021, 9, 18)

    def test_format_author(self):
        assert format_author('Hart, Kevin') == 'Kevin Hart'
        assert format_author('Covey, Stephen R.') == 'Stephen R. Covey'
        assert format_author('Roberts, Alice, 1973-') == 'Alice Roberts'
        assert format_author('Huffington, Arianna Stassinopoulos, 1950-') == 'Arianna Stassinopoulos Huffington'

    def test_is_due(self):
        assert books[0].is_due() is True
        assert books[1].is_due() is True
        assert books[2].is_due() is False
