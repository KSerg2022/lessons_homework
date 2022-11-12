"""Unittest class Person and PersonVerify."""
import unittest
from person import Person, PersonData


class TestPerson(unittest.TestCase):
    """Unittest class Person"""

    def setUp(self) -> None:
        self.person_data = PersonData('Иванов Иван Иванович', 36, 'ВР-415141', 101.3)
        self.person = Person(self.person_data)
        self.test_person_data = PersonData('Петров Петр Петрович', 50, 'АА-111111', 50.0)

    def tearDown(self) -> None:
        del self.person
        del self.person_data

    def test_get_value(self):
        self.assertEqual(self.person.full_name, self.person_data.full_name)
        self.assertEqual(self.person.age, self.person_data.age)
        self.assertEqual(self.person.weight, self.person_data.weight)
        self.assertEqual(self.person.id_card, self.person_data.id_card)

    def test_set_value(self):
        self.person.full_name = self.test_person_data.full_name
        self.person.age = self.test_person_data.age
        self.person.weight = self.test_person_data.weight
        self.person.id_card = self.test_person_data.id_card

        self.assertEqual(self.person.full_name, self.test_person_data.full_name)
        self.assertEqual(self.person.age, self.test_person_data.age)
        self.assertEqual(self.person.weight, self.test_person_data.weight)
        self.assertEqual(self.person.id_card, self.test_person_data.id_card)

    def test__str__(self):
        self.assertEqual(str(self.person), self.person.full_name)

    def test_verify_full_name_errors(self):
        with self.assertRaises(TypeError) as exception_full_name_type_error_context:
            self.person.full_name = 50
        self.assertEqual(str(exception_full_name_type_error_context.exception),
                         'Full name must be a string')
        with self.assertRaises(TypeError) as exception_full_name_type_error_context:
            self.person.full_name = ''
        self.assertEqual(str(exception_full_name_type_error_context.exception),
                         'Full name must contain at least one character')

        with self.assertRaises(TypeError) as exception_full_name_type_error_context:
            self.person.full_name = 'Иванов  Иванович '
        self.assertEqual(str(exception_full_name_type_error_context.exception),
                         'Invalid name format')

        with self.assertRaises(TypeError) as exception_full_name_type_error_context:
            self.person.full_name = 'Иванов1 Иван Иванович'
        self.assertEqual(str(exception_full_name_type_error_context.exception),
                         'Full name can only contain letter')

    def test_age_errors(self):
        with self.assertRaises(TypeError) as exception_age_error_context:
            self.person.age = '20'
        self.assertEqual(str(exception_age_error_context.exception), 'Age must be an integer')

        with self.assertRaises(ValueError) as exception_age_error_context:
            self.person.age = 12
        self.assertIn('Age must be between', str(exception_age_error_context.exception))

        with self.assertRaises(ValueError) as exception_age_error_context:
            self.person.age = 120
        self.assertIn('Age must be between', str(exception_age_error_context.exception))

    def test_weight_errors(self):
        with self.assertRaises(TypeError) as exception_weight_type_error_context:
            self.person.weight = 50
        self.assertEqual(str(exception_weight_type_error_context.exception), 'Weight must be an float number')

        with self.assertRaises(ValueError) as exception_weight_value_error_context:
            self.person.weight = 10.0
        self.assertIn('Weight should be between', str(exception_weight_value_error_context.exception))

        with self.assertRaises(ValueError) as exception_weight_value_error_context:
            self.person.weight = 150.0
        self.assertIn('Weight should be between', str(exception_weight_value_error_context.exception))

    def test_id_card_errors(self):
        with self.assertRaises(TypeError) as exception_id_card_type_error_context:
            self.person.id_card = 55555
        self.assertEqual(str(exception_id_card_type_error_context.exception), 'Invalid data type for card id')

        with self.assertRaises(ValueError) as exception_id_card_value_error_context:
            self.person.id_card = 'ВР-4151'
        self.assertEqual(str(exception_id_card_value_error_context.exception),
                         'Invalid card id data format XX-XXXXXX', )


if __name__ == '__main__':
    unittest.main()
