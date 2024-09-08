from datetime import date, datetime
from re import match

from app.library_book import LibraryBook

def get_books_due(books: list[LibraryBook]) -> list[LibraryBook]:
    return [book for book in books if book.is_due()]

def get_next_due_date(books: list[LibraryBook]) -> date:
    return min((book.due_date for book in books if book.due_date > date.today()), default=None)

def format_author(author_str: str) -> str:
    author_names = [string for string in author_str.split(', ') if match('[a-zA-Z.-]', string)]
    return ' '.join(reversed(author_names))

def format_due_date(due_date: date) -> str:
    return due_date.strftime('%d/%m/%y')

def parse_date(due_date_string: str) -> date:
    """convert due date string into a date"""
    formatted_string = due_date_string.strip().split(' ')[0]
    try:
        datetime_object = datetime.strptime(formatted_string, '%d/%m/%Y')
    except ValueError:
        datetime_object = datetime.strptime(formatted_string, '%d/%m/%y')
    return datetime_object.date()
