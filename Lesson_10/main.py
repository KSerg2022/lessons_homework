"""Finding a sequence of button presses on a push-button phone to display the requested text."""
import re


def verify_char(char: str) -> str | None:
    """Checks if the given character is allowed."""
    match = re.search(r'[A-Z.,?!:\s]', char)
    return match


def find_char(char_from_text: str, buttons: dict) -> str:
    """Finds the required number of presses of the desired button to display the requested character."""
    result = ''
    for button, clicks in buttons.items():
        for qwt_click, char in clicks.items():
            if char_from_text == char:
                result = str(button) * qwt_click
    return result


def get_dialing_sequence(text: str, buttons: dict[int: dict[int: str]]) -> str:
    """Get a sequence of button presses to display the requested text."""
    button_sequence = ''
    for char in text.upper():
        check_char = verify_char(char)
        if check_char:
            button = find_char(char, buttons)
            button_sequence += str(button)
    return button_sequence


def main(buttons: dict[int: dict[int: str]]):
    """Main controller."""
    while True:
        print(f'Enter text, and you get sequence of button presses'
              f' on a push-button phone to display the requested text.')
        print(f'If you want to exit - press "Enter".')
        text = input(f'Please, enter text: ')
        if not text:
            print('\nBye!!!')
            exit()
        dialing_sequence = get_dialing_sequence(text, buttons)
        print(f'To get the text - "{text}",\n'
              f'you need to press the buttons on the phone in the following sequence - "{dialing_sequence}".\n')


if __name__ == '__main__':
    char_on_phone_buttons = {
        1: {1: '.', 2: ',', 3: '?', 4: '!', 5: ':'},
        2: {1: 'A', 2: 'B', 3: 'C'},
        3: {1: 'D', 2: 'E', 3: 'F'},
        4: {1: 'G', 2: 'H', 3: 'I'},
        5: {1: 'J', 2: 'K', 3: 'L'},
        6: {1: 'M', 2: 'N', 3: 'O'},
        7: {1: 'P', 2: 'Q', 3: 'R', 4: 'S'},
        8: {1: 'T', 2: 'U', 3: 'V'},
        9: {1: 'W', 2: 'X', 3: 'Y', 4: 'Z'},
        0: {1: ' '},
    }
    main(char_on_phone_buttons)
