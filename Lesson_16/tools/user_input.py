"""Modul user input data."""


class UserInput:
    """Initialization class UserInput."""

    def __init__(self):
        """Initialization parameters."""
        self.informational_text = ("\nThis calculator can help you to do next operation:\n"
                                   "1. add - '+'\n"
                                   "2. minus - '-'\n"
                                   "3. multiply - '*'\n"
                                   "4. divide - '/'"
                                   )
        self.first_number = 0
        self.second_number = 0
        self.operator = ''
        self.quit = ''

    def print_greeting(self):
        print(self.informational_text)

    def get_input(self) -> tuple:
        """Get user data"""
        self.first_number = input(f'Enter your fist number: ')
        self.second_number = input(f'Enter your second number: ')
        self.operator = input(f'Enter your operation: ')
        return self.first_number, self.second_number, self.operator

    def want_repeat(self):
        """Want to continue calculating."""
        self.quit = input(f'To quit enter "q".'
                          f' To continue press "Enter".')
        if self.quit == 'q':
            print('Bey!')
            exit()
        print(f'\nYou want to continue.')
