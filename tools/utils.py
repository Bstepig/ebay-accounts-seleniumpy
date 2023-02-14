import random
import secrets
import string
from datetime import date, timedelta
from random import randrange

DIGITS_LEN = random.randint(2, 5)
LETTERS_LEN = random.randint(4, 15)
SPECIAL_LEN = random.randint(2, 5)


def generate_password():
    digits_password = random_sub(string.digits, DIGITS_LEN)
    letters_password = random_sub(string.ascii_letters, LETTERS_LEN)
    special_password = random_sub(string.punctuation, SPECIAL_LEN)

    password_list = digits_password + letters_password + special_password
    random.shuffle(password_list)
    password = ''.join(password_list)
    return password


def random_sub(arr, length):
    return [secrets.choice(arr) for i in range(length)]


def random_letter_sub(min_length=8, max_length=16, letters=string.ascii_letters):
    length = random.randint(min_length, max_length)
    return ''.join(secrets.choice(letters) for i in range(length))


def random_date(start: date, end: date):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
