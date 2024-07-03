from app.logger import logger
from datetime import date
# from app.emailer import send_email
from app.library_book import LibraryBook, format_due_date


def get_books_due(books: list[LibraryBook]) -> list[LibraryBook]:
    return [book for book in books if book.is_due()] if books else []


def get_next_due_date(books: list[LibraryBook]) -> date:
    due_dates = [book.due_date for book in books]
    return min(due_date for due_date in due_dates if due_date > date.today())


# def send_confirmation_email(renewed_books: list[LibraryBook], books_due=None) -> None:
#     confirmation_msg = f'Books renewed: {", ".join(book.title for book in renewed_books)}\n' \
#                        f'Next due date: {format_due_date(get_next_due_date(renewed_books))}\n'
#     if books_due is not None:
#         confirmation_msg +=
#         f'\nFailed to renew: {", ".join(book.title for book in renewed_books)}\n'
#
#     # send_email(confirmation_msg)
#     logger = logging.getLogger('logger')
#     logger.info(f'Email sent. {confirmation_msg}')
