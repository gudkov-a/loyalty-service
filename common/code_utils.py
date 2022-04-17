import random
from typing import List, Set
import string

from flask import current_app

from app.models import DiscountCode


class CodesGenerator:

    def __init__(self, desired_amount: int):
        self._desired_amount = desired_amount
        self._maximum_code_length = current_app.config['DEFAULT_CODE_LENGTH']

        self._percent_of_letters = 70
        self._percent_of_digits = 100 - self._percent_of_letters

        self._number_of_letters = (self._percent_of_letters * self._maximum_code_length) // 100
        self._number_of_integers = (self._percent_of_digits * self._maximum_code_length) // 100

        self._existing_codes = self._load_existing_codes()

    def _load_existing_codes(self) -> List[str]:
        return [item.code for item in DiscountCode.query.all()]

    def _generate_code(self) -> str:
        """
        Generate new code consisting of a letters and digits. If code already exists method will call itself recursively
        """
        rand_letters = list(random.choices(string.ascii_uppercase, k=self._number_of_letters))
        rand_integers = list(random.choices(string.digits, k=self._number_of_integers))

        letters_and_integers = rand_letters + rand_integers
        random.shuffle(letters_and_integers)
        new_code = ''.join(letters_and_integers)

        if new_code not in self._existing_codes:
            return new_code
        return self._generate_code()

    def generate(self) -> Set[str]:
        result = set()
        while len(result) != self._desired_amount:
            new_code = self._generate_code()
            result.add(new_code)
        return result
