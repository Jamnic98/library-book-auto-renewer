from datetime import date


def parse_date(due_date_string):
    full_due_date = due_date_string.split('/')
    due_date = date(int(full_due_date[2]), int(full_due_date[1]), int(full_due_date[0]))
    return due_date


def is_due(due_date):
    return (due_date - date.today()).days == 0


def format_author(author):
    return ' '.join(reversed(author.split(', ')))


def get_books_due(books):
    books_due = []
    for book in books:
        due_date = parse_date(book.due_date)
        if is_due(due_date):
            books_due.append(book)
    return books_due
