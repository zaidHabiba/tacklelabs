import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_int_valid(value):
    try:
        value = int(value)
        return True
    except Exception:
        return False


def is_date_time_valid(date):
    date_format = '%Y-%m-%d,%I:%M:%S'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False

def is_date_valid(date):
    date_format = '%Y-%m-%d'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False

def is_email_valid(email):
    try:
        validate_email(email)
        # if pass mean email is valid
        return True
    except ValidationError:
        return False


# password between 30-8
# password have at lest upper char
# password have at lest lower char
# password have at lest number
def is_password_valid(password):
    if 8 < len(password) < 30:
        if re.search("[a-z]", password) \
                or re.search("[A-Z]", password) \
                and re.search("[0-9]", password):
            return True
    return False


def is_name_valid(name):
    # name contains numbers or special characters
    if name.isalpha():
        return True
    else:
        return False


# make sure gender is one of those chars (m,f)
def is_gender_valid(gender):
    if gender == 'm' or gender == 'f':
        return True
    else:
        return False


def is_rating_valid(rating):
    try:
        float(rating)
        if 0 <= rating <= 5:
            return True
        else:
            return False
    except ValueError:
        return False
