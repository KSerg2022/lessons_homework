"""Class Person."""
import re
from typing import NamedTuple


class PersonData(NamedTuple):
    full_name: str
    age: int
    passport: str
    weight: float


class Person:
    """Class Person."""
    MINIMUM_AGE, MAXIMUM_AGE = (18, 66)
    MINIMUM_WEIGHT, MAXIMUM_WEIGHT = (40, 130)
    FULL_NAME_FORMAT = re.compile(r'^[А-Я][а-я]+\s[А-Я][а-я]+\s[А-Я][а-я]+$')
    PASSPORT_FORMAT = re.compile(r'^[А-Я]{2}-\d{6}$')

    def __init__(self, obj: PersonData):
        """Initialization parameters."""
        self.check_all_data(obj)
        self.__full_name = obj.full_name
        self.__age = obj.age
        self.__passport = obj.passport
        self.__weight = obj.weight

    def __str__(self):
        return self.full_name

    @classmethod
    def check_all_data(cls, data: PersonData):
        """Returns True if checks for all parameters are passed."""
        cls.check_full_name_data(data.full_name)
        cls.check_age_data(data.age)
        cls.check_passport_data(data.passport)
        cls.check_weight_data(data.weight)

    @classmethod
    def check_full_name_data(cls, full_name: str):
        """Data validation full name."""
        if not isinstance(full_name, str):
            raise TypeError('Значение должно быть "string".')
        if not cls.FULL_NAME_FORMAT.match(full_name):
            raise ValueError('Вы ввели некорректное ФИО. Шаблон "Ф И О".')

    @classmethod
    def check_age_data(cls, age: int):
        """Data validation age."""
        if not isinstance(age, int):
            raise TypeError('Значение должно быть "integer".')
        if not cls.MINIMUM_AGE <= age <= cls.MAXIMUM_AGE:
            raise ValueError(f'Вы ввели некорректный возраст.'
                             f'Значение должно быть в диапазоне - {cls.MINIMUM_AGE} - {cls.MAXIMUM_AGE} лет.')

    @classmethod
    def check_passport_data(cls, passport: str):
        """Data validation passport number."""
        if not isinstance(passport, str):
            raise TypeError('Значение должно быть "string".')
        if not cls.PASSPORT_FORMAT.match(passport):
            raise ValueError(f'Вы ввели некорректный номер паспорта. Образец - "ВР-415141".')

    @classmethod
    def check_weight_data(cls, weight: float):
        """Data validation weight."""
        if not isinstance(weight, float):
            raise TypeError('Значение должно быть "float".')
        if not cls.MINIMUM_WEIGHT <= weight <= cls.MAXIMUM_WEIGHT:
            raise ValueError(f'Вы ввели некорректный вес. '
                             f'Значение должно быть в диапазоне - {cls.MINIMUM_WEIGHT} - {cls.MAXIMUM_WEIGHT} кг.')

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, full_name: str):
        self.check_full_name_data(full_name)
        self.__full_name = full_name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age: int):
        self.check_age_data(age)
        self.__age = age

    @property
    def passport(self):
        return self.__passport

    @passport.setter
    def passport(self, passport: str):
        self.check_passport_data(passport)
        self.__passport = passport

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight: float):
        self.check_weight_data(weight)
        self.__weight = weight
