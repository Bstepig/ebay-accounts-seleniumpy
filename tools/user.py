import random
from datetime import date

import names
from tools.utils import generate_password, random_letter_sub, random_date

OLDEST = date(1960, 1, 1)
YOUNGEST = date(2004, 12, 31)


class Profile:
    email_prefix = "@gmx.de"
    email_attempt = 0

    def __init__(self, data: dict) -> None:
        self.genderIndex = random.randint(0, 2)
        self.gender = ['male', 'female', 'unknown'][self.genderIndex]

        self.firstName = names.get_first_name(self.gender)
        self.lastName = names.get_last_name()

        self.postalCode = data.get('zip', str(random.randint(10000, 99999)))
        self.town = data.get('city', 'Berlin')
        self.street = data.get('street', random_letter_sub())
        self.home = data.get('home', str(random.randint(1, 40)))

        self.birthday = random_date(OLDEST, YOUNGEST)
        self.birthDay = self.birthday.day
        self.birthMonth = self.birthday.month
        self.birthYear = self.birthday.year

        self.email_name = self.firstName.lower() + self.lastName.lower() + \
            str(self.birthYear) + str(random.randint(1, 99))
        self.email_password = generate_password()
        self.email_phone = "155" + random_letter_sub(8, 8, '1234567890')

        self.ebay_password = generate_password()
        self.ebay_phone = None

    def get_email(self):
        return self.get_email_name() + self.email_prefix

    def get_email_name(self):
        if self.email_attempt == 0:
            return self.email_name
        return f'{self.email_name}{self.email_attempt}'

    def next_email_name(self):
        self.email_attempt += 1