from datetime import date

from app.utlis import format_author, parse_date, format_due_date


class LibraryBook:
    def __init__(self, title: str, author: str, due_date: str, times_renewed: str):
        self.title = title
        self.author = format_author(author)
        self.due_date = parse_date(due_date)
        self.times_renewed = times_renewed

    def is_due(self) -> bool:
        return (self.due_date - date.today()).days <= 0

    def __repr__(self):
        return f'<Title: {self.title}\n' + f'Author: {self.author}\n' + f'Due: {format_due_date(self.due_date)}>'


def get_books_due(books: list[LibraryBook]) -> list[LibraryBook]:
    return [book for book in books if book.is_due()]

def get_next_due_date(books: list[LibraryBook]) -> date:
    return min((book.due_date for book in books if book.due_date > date.today()), default=None)
