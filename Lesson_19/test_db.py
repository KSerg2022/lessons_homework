"""Unitest db.py"""
import unittest
from unittest.mock import patch
from io import StringIO

from db import DataBase, DataBaseDTO


class TestDataBase(unittest.TestCase):
    def setUp(self) -> None:
        self.database_dto = DataBaseDTO('postgres', 'user', 'qwertyR1!', '127.0.0.1', '5001')
        self.database = DataBase(self.database_dto)
        print(' ' * 20 + f'---{self._testMethodName}---')

    def tearDown(self) -> None:
        del self.database
        del self.database_dto

    def test_del(self):
        self.assertEqual(None, self.database.__del__())

    def test_enter(self):
        self.assertEqual(self.database, self.database.__enter__())

    def test_exit(self):
        self.assertIsNone(self.database.__exit__(1, 1, 1))

    def test_connect(self):
        with patch('sys.stdout', new=StringIO()) as message:
            self.database.connect()
        self.assertTrue('Connect to DB:' in message.getvalue())

    def test_close(self):
        with patch('sys.stdout', new=StringIO()) as message:
            self.database.close()
        self.assertTrue('Close connect to DB:' in message.getvalue())

    def test_read(self):
        with patch('sys.stdout', new=StringIO()) as message:
            self.database.read('test_name')
        self.assertTrue('Read data from database:' in message.getvalue())

    def test_wright(self):
        with patch('sys.stdout', new=StringIO()) as message:
            self.database.write('test_name', 'test_data')
        self.assertTrue('Write' in message.getvalue())

    def test_instance_when_connected(self):
        self.assertEqual(self.database, self.database.instance())

    def test_instance_when_closed(self):
        self.database.__del__()
        self.assertEqual(None, self.database.instance())

    def test_instance_singleton(self):
        data_postgres = DataBaseDTO('postgres', 'user', 'qwertyR1!', '127.0.0.1', '5001')
        data_mysql = DataBaseDTO('mysql', 'user', 'qwertyR1!', '127.0.0.1', '5001')

        database_postgres = DataBase(data_postgres)
        database_mysql = DataBase(data_mysql)
        self.assertEqual(id(database_postgres), id(database_mysql))

    def test_get_values(self):
        self.assertEqual(self.database.databases, ('postgres', 'mysql', 'sqlite'))
        self.assertIn(self.database.db_name, ('postgres', 'mysql', 'sqlite'))
        self.assertIn(self.database.user, self.database_dto.user)
        self.assertIn(self.database.password, self.database_dto.password)
        self.assertIn(self.database.host, self.database_dto.host)
        self.assertIn(self.database.port, self.database_dto.port)

    def test_set_values(self):
        self.database.db_name = 'mysql'
        self.database.user = 'bob'
        self.database.password = '1qa2WSde#'
        self.database.host = '127.0.0.2'
        self.database.port = '11111'

        self.assertIn(self.database.db_name, 'mysql')
        self.assertIn(self.database.user, 'bob')
        self.assertIn(self.database.password, '1qa2WSde#')
        self.assertIn(self.database.host, '127.0.0.2')
        self.assertIn(self.database.port, '11111')

    def test_verify_db_name(self):
        with self.assertRaises(TypeError) as error:
            self.database.db_name = 1111
        self.assertIn('must be a string', str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.database.db_name = ''
        self.assertEqual(str(error.exception), 'Empty string in values')

        with self.assertRaises(Exception) as error:
            self.database.db_name = 'qwerty'
        self.assertIn('Unsupported DB:', str(error.exception))

    def test_verify_user(self):
        with self.assertRaises(TypeError) as error:
            self.database.user = 1111
        self.assertIn('must be a string', str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.database.user = ''
        self.assertEqual(str(error.exception), 'Empty string in values')

        with self.assertWarns(Warning) as warning:
            self.database.user = 'root'
        self.assertEqual('Use root user is dangerous', str(warning.warning))

    def test_verify_password(self):
        with self.assertRaises(TypeError) as error:
            self.database.password = 1111
        self.assertIn('must be a string', str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.database.password = ''
        self.assertEqual(str(error.exception), 'Empty string in values')

        for password in ('q', 'qqawWSde#', '1qa2wsde#', '1QA2WSDE#', '1qa2WSde3'):
            with self.assertRaises(Exception) as error:
                self.database.password = password
            self.assertIn('Password must be', str(error.exception))

    def test_verify_host(self):
        with self.assertRaises(TypeError) as error:
            self.database.host = 1111
        self.assertIn('must be a string', str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.database.host = ''
        self.assertEqual(str(error.exception), 'Empty string in values')

        with self.assertRaises(Exception) as error:
            self.database.host = '198.162.0.300'
        self.assertIn('does not appear', str(error.exception))

        with self.assertRaises(Exception) as error:
            self.database.host = '192.168.88.100'
        self.assertIn('is not avaliable', str(error.exception))

    def test_verify_port(self):
        with self.assertRaises(TypeError) as error:
            self.database.port = 1111
        self.assertIn('must be a string', str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.database.port = ''
        self.assertEqual(str(error.exception), 'Empty string in values')

        with self.assertRaises(Exception) as error:
            self.database.port = 'qqqq'
        self.assertIn('Port must contains numbers not', str(error.exception))

        for port in ('0', '65001'):
            with self.assertRaises(Exception) as error:
                self.database.port = port
            self.assertIn('Port must be between 0-65000', str(error.exception))


if __name__ == '__main__':
    unittest.main()
