"""Encoding / decoding caesar cipher."""


def get_user_language() -> str:
    """User selects the language for the text."""
    while True:
        menu_languages = ("Program menu:\n"
                          "1. Coding english language.\n"
                          "2. Coding ukraine language.")
        print(menu_languages)
        user_language_choice = input('make your choice: ')
        if user_language_choice == '1':
            return EN_LANG
        elif user_language_choice == '2':
            return UK_LANG
        else:
            print(f'Your choice may be 1 or 2. Bye.')


def get_coding_status() -> bool:
    """User selects encode or decode."""
    while True:
        menu_coding = ("Program menu:\n"
                       "1. Encoding.\n"
                       "2. Decoding.")
        print(menu_coding)
        user_coding_choice = input('make your choice: ')
        if user_coding_choice == '1':
            return True
        elif user_coding_choice == '2':
            return False
        else:
            print(f'Your choice may be 1 or 2. Bye.')


def get_displacement_step(language) -> str:
    """User selects displacement step for coding."""
    while True:
        displacement_step = input(f'Enter step for encoding / decoding. It integer from 1 to {len(language)}: ')
        if int(displacement_step) < 1 or int(displacement_step) > len(language):
            print(f'Your choice may be from 1 to {len(language)}. Bye.')
        else:
            return displacement_step


def get_check_data(user_language: str, user_coding: bool, displacement_step: str, user_text: str) -> str:
    """Validation of the correctness of the entered data by the user."""
    while True:
        print(f'\nYou data:\n'
              f'Language - {user_language},\n'
              f'Text for coding - "{user_text}",\n'
              f'Displacement step - {displacement_step},\n'
              f'Encoding (True) / decoding (False) - {user_coding}.')
        check_data = input("Your data is correct? Enter 'y'/'n': ")
        if check_data == 'y' or check_data == 'n':
            return check_data
        else:
            print("You must enter in english 'y'/'n'.")


def get_date_for_coding(language: str, step: str) -> dict[str: str]:
    """Make a convenient data structure."""
    date_for_coding = {}
    for index, letter in enumerate(language):
        if index < len(language) - int(step):
            date_for_coding[letter] = language[index + int(step)]
        else:
            date_for_coding[letter] = language[index + int(step) - len(language)]
    reverse_date_for_coding = {code: letter for letter, code in date_for_coding.items()}
    return date_for_coding, reverse_date_for_coding


def get_coded_text(text: str, codes: dict[str: str], language: str) -> str:
    """Get encoded or decoded text."""
    coded_text = ''
    for char in text:
        if char in language:
            coded_text += codes[char]
        else:
            coded_text += char
    return coded_text


def main():
    """Main controller."""
    while True:
        print("\nWelcome to encoding / decoding caesar cipher program.""")
        user_language = get_user_language()
        user_coding = get_coding_status()
        user_text = input('Enter text for encoding / decoding: ')
        displacement_step = get_displacement_step(user_language)

        check_data = get_check_data(user_language, user_coding, displacement_step, user_text)
        if check_data == 'y':
            date_for_coding, reverse_date_for_coding = get_date_for_coding(user_language, displacement_step)
            if user_coding:
                encoded_text = get_coded_text(user_text, date_for_coding, user_language)
                print(f'Your encoded text - "{encoded_text}".')
            else:
                decoded_text = get_coded_text(user_text, reverse_date_for_coding, user_language)
                print(f'Your decoded text - "{decoded_text}".')

        want_continue = input("\nIf you want to continue press - 'Enter'.\n"
                              "If you want to stop press - 'q'.")
        if want_continue == 'q':
            print('Bye!')
            exit()


EN_LANG = 'abcdefghijklmnopqrstuvwxyz'
UK_LANG = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'

if __name__ == '__main__':
    main()
