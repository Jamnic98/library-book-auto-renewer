from re import match
from datetime import date, datetime


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
