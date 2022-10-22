"""Encrypts text using a vertical permutation cipher."""


def get_crypt_table(normalize_text, crypt_key):
    """Creates character columns in table."""
    columns_table = []
    for position_in_string in range(len(crypt_key)):
        step = 0 + position_in_string
        column_table = []
        for _ in range(len(normalize_text)):
            if step < len(normalize_text):
                column_table.append(normalize_text[step])
                step += len(crypt_key)
        columns_table.append(''.join(column_table))
    return dict(zip(crypt_key, columns_table))


def get_encrypt_text(crypt_table):
    """Creates ciphertext."""
    normalize_table = dict(sorted(crypt_table.items()))
    encrypt_columns = normalize_table.values()
    return ''.join(encrypt_columns)


def main(text_to_crypt, crypt_key):
    """Main controller."""
    crypt_table = get_crypt_table(text_to_crypt, crypt_key)
    encrypt_text = get_encrypt_text(crypt_table)
    return encrypt_text


if __name__ == '__main__':
    CASES = (
        ('пример маршрутной перестановки',
         (3, 1, 4, 2, 5), 'р рйеоматпткпршорниму свернеаи'),

        ('пример маршрутной перестановки 1995!',
         (3, 1, 4, 2, 5), 'р рйео1матптк9пршорн !иму св9ернеаи5'),

        ('The math.ceil() method rounds a number upwards to its nearest integer!!!',
         (6, 3, 1, 7, 4, 2, 5), 'ecmrardteealhnuptn rh.   erirt!mitunu  tet(odmwoei!Th)dsba an! eeo  sssg'),

    )
    for test_text, test_key, cryptogram in CASES:
        assert main(test_text, test_key) == cryptogram
        # print(f'\n{test_text} - incoming data,\n{main(test_text, test_key)} - solution,\n'
        #       f'{cryptogram} - verification answer.')
