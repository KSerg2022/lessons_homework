"""Decrypts text using a vertical permutation cipher."""
from math import ceil


def get_numbers_chars_in_column(text_to_decrypt, crypt_key):
    """Get the number of characters in each column."""
    string_length = len(text_to_decrypt) // len(crypt_key)
    length_incomplete_string = len(text_to_decrypt) % len(crypt_key)
    number_lines = ceil(len(text_to_decrypt) / len(crypt_key))
    columns = []
    for number_column in range(len(crypt_key)):
        if number_column < length_incomplete_string:
            columns.append(number_lines)
        else:
            columns.append(string_length)
    chars_columns = sorted(zip(crypt_key, columns))
    return chars_columns


def get_text_in_columns(text_to_decrypt, number_chars_in_column):
    """Get the text in each of the columns."""
    columns = []
    start, end = 0, 0
    for number_column, qwt_chars in number_chars_in_column:
        end += qwt_chars
        columns.append(text_to_decrypt[start:end])
        start += qwt_chars
    return columns


def get_decrypt_table(text_in_columns, crypt_key):
    """Get encryption table."""
    text_table = []
    for key in crypt_key:
        for position, text_column in enumerate(text_in_columns, 1):
            if key == position:
                text_table.append(text_column)
    return text_table


def get_decrypt_text(decrypt_table, crypt_key):
    """Get decrypted text."""
    number_lines = ceil(len(''.join(decrypt_table)) / len(crypt_key))
    text = []
    for number_string in range(number_lines):
        for column in decrypt_table:
            if number_string < len(column):
                text.append(column[number_string])
    return ''.join(text)


def main(text_to_decrypt, crypt_key):
    """Main controller."""
    number_chars_in_column = get_numbers_chars_in_column(text_to_decrypt, crypt_key)
    text_in_columns = get_text_in_columns(text_to_decrypt, number_chars_in_column)
    decrypt_table = get_decrypt_table(text_in_columns, crypt_key)
    decrypt_text = get_decrypt_text(decrypt_table, crypt_key)
    return decrypt_text


if __name__ == '__main__':
    CASES = (
        ('р рйеоматпткпршорниму свернеаи',
         (3, 1, 4, 2, 5), 'пример маршрутной перестановки'),

        ('р рйео1матптк9пршорн !иму св9ернеаи5',
         (3, 1, 4, 2, 5), 'пример маршрутной перестановки 1995!'),

        ('ecmrardteealhnuptn rh.   erirt!mitunu  tet(odmwoei!Th)dsba an! eeo  sssg',
         (6, 3, 1, 7, 4, 2, 5), 'The math.ceil() method rounds a number upwards to its nearest integer!!!'),
    )
    for cryptogram, test_key, test_text in CASES:
        assert main(cryptogram, test_key) == test_text
        # print(f'\n{cryptogram} - incoming data,\n{main(cryptogram, test_key)} - solution,\n'
        #       f'{test_text} - verification answer.')
