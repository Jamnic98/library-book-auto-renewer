from datetime import date

from emailer import send_email
from library_book import LibraryBook, format_due_date


def get_books_due(books: list[LibraryBook]) -> list[LibraryBook]:
    books_due = []
    for book in books:
        if book.is_due():
            books_due.append(book)
    return books_due


def get_next_due_date(books: list[LibraryBook]) -> date:
    due_dates = [book.due_date for book in books]
    return min(due_date for due_date in due_dates if due_date > date.today())


def send_confirmation_email(renewed_books: list[LibraryBook], books_due=None) -> None:
    confirmation_msg = f'Books renewed: {", ".join(book.title for book in renewed_books)}\n' \
                       f'Next due date: {format_due_date(get_next_due_date(renewed_books))}'
    if books_due is not None:
        confirmation_msg += f'Failed to renew: {", ".join(book.title for book in renewed_books)}\n'

    send_email(confirmation_msg)
