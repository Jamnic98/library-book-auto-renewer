from datetime import date, datetime
from re import match


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


class LibraryBook:
    def __init__(self, title: str, author: str, due_date: str, times_renewed: str, check_box):
        self.title = title
        self.author = format_author(author)
        self.due_date = parse_date(due_date)
        self.times_renewed = times_renewed
        self.check_box = check_box

    def is_due(self) -> bool:
        return (self.due_date - date.today()).days <= 0

    def __repr__(self):
        return f'Title: {self.title}\n' + f'Author: {self.author}\n' + f'Due: {format_due_date(self.due_date)}\n'
