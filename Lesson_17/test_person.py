""""""
import unittest

from person import Person, PersonData

class TestPerson(unittest.TestCase):
    """"""
    def setUp(self) -> None:
        self.person_data = PersonData('Петров Петр Петрович', 36, 'ВР-415141', 75.8)
        self.person = Person(self.person_data)

        self.__full_name = 'Петров Петр Петрович'
        self.__age = 50
        self.__weight = 50.0
        self.__passport = 'АА-111111'

        self.__full_names_for_test = ('Петров Петр Петрович', 444444, 'Петров Петр', 'Петров1 Петр Петрович', '')
        self.__full_name_exceptions_context = ('Значение должно быть "string".',
                                               'Вы ввели некорректное ФИО. Шаблон "Ф И О".')
        self.__ages_for_test = (20, '20', 12,)
        self.__age_exceptions_context = (
            'Значение должно быть "integer".',
            f'Вы ввели некорректный возраст.'
            f'Значение должно быть в диапазоне - {self.person.MINIMUM_AGE} - {self.person.MAXIMUM_AGE} лет.',
        )
        self.__passports_for_test = ('ВР-415141', 123456, 'ВР-415',)
        self.__passport_exceptions_context = (
            'Значение должно быть "string".',
            'Вы ввели некорректный номер паспорта. Образец - "ВР-415141".',
        )
        self.__weights_for_test = (50.0, '50', 10.0,)
        self.__weight_exceptions_context = (
            'Значение должно быть "float".',
            f'Вы ввели некорректный вес. '
            f'Значение должно быть в диапазоне - {self.person.MINIMUM_WEIGHT} - {self.person.MAXIMUM_WEIGHT} кг.',
        )

    def tearDown(self) -> None:
        del self.person
        del self.person_data

    def test_check_full_name_data(self):
        for index, full_name in enumerate(self.__full_names_for_test):
            if not index:
                self.assertIsNone(self.person.check_full_name_data(full_name))
            else:
                with self.assertRaises(Exception) as exception_full_name_errors_context:
                    self.person.check_full_name_data(full_name)
                self.assertIn(str(exception_full_name_errors_context.exception), self.__full_name_exceptions_context)

    def test_check_age_data(self):
        for index, age in enumerate(self.__ages_for_test):
            if not index:
                self.assertIsNone(self.person.check_age_data(age))
            else:
                with self.assertRaises(Exception) as exception_age_errors_context:
                    self.person.check_age_data(age)
                self.assertIn(str(exception_age_errors_context.exception), self.__age_exceptions_context)

    def test_check_passport_data(self):
        for index, passport in enumerate(self.__passports_for_test):
            if not index:
                self.person.check_passport_data(passport)
            else:
                with self.assertRaises(Exception) as exception_passport_errors_context:
                    self.person.check_passport_data(passport)
                self.assertIn(str(exception_passport_errors_context.exception), self.__passport_exceptions_context)

    def test_weight_data(self):
        for index, weight in enumerate(self.__weights_for_test):
            if not index:
                self.person.check_weight_data(weight)
            else:
                with self.assertRaises(Exception) as exception_weight_errors_context:
                    self.person.check_weight_data(weight)
                self.assertIn(str(exception_weight_errors_context.exception), self.__weight_exceptions_context)

    def test_full_name(self):
        self.assertEqual(self.person.full_name, self.person_data.full_name)

    def test_full_name_set(self):
        self.person.full_name = self.__full_name
        self.assertEqual(self.person.full_name, self.__full_name)

    def test_age(self):
        self.assertEqual(self.person.age, self.person_data.age)

    def test_age_set(self):
        self.person.age = self.__age
        self.assertEqual(self.person.age, self.__age)

    def test_weight(self):
        self.assertEqual(self.person.weight, self.person_data.weight)

    def test_weight_set(self):
        self.person.weight = self.__weight
        self.assertEqual(self.person.weight, self.__weight)

    def test_passport(self):
        self.assertEqual(self.person.passport, self.person_data.passport)

    def test_passport_set(self):
        self.person.passport = self.__passport
        self.assertEqual(self.person.passport, self.__passport)

    def test__str__(self):
        self.assertEqual(str(self.person), self.person.full_name)


if __name__ == '__main__':
    unittest.main()
