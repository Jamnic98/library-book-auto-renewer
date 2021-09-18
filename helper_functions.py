from datetime import datetime, date


def parse_date(due_date_string):
    s = due_date_string.strip().split(' ')[0]
    try:
        datetime_object = datetime.strptime(s, '%d/%m/%Y')
    except ValueError:
        datetime_object = datetime.strptime(s, '%d/%m/%y')

    return datetime_object.date()


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
