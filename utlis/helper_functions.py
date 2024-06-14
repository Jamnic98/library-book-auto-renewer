import logging
from datetime import date
# from app.emailer import send_email
from app.library_book import LibraryBook, format_due_date


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
    confirmation_msg = F'Books renewed: {", ".join(book.title for book in renewed_books)}\n' \
                       F'Next due date: {format_due_date(get_next_due_date(renewed_books))}\n'
    if books_due is not None:
        confirmation_msg += F'\nFailed to renew: {", ".join(book.title for book in renewed_books)}\n'

    # send_email(confirmation_msg)
    logger = logging.getLogger('logger')
    logger.info(F'Email sent. {confirmation_msg}')
