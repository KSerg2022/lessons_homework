"""Modul Calculator."""

from Lesson_16.tools.operation import Operation
from Lesson_16.tools.user_input import UserInput
from Lesson_16.hamdles.check_input_data import CheckData
from Lesson_16.tools.output_result import OutputResult


class Calculator:
    """Initialization class Calculator."""
    user_input = UserInput()
    output_result = OutputResult()

    def __init__(self):
        """Initialization parameters."""
        self.data = ()
        self.result = 0

    def run(self):
        """Main controller"""
        self.user_input.print_greeting()
        while True:
            self.data = self.user_input.get_input()
            if self._check_data():
                continue
            self.result = Operation(*self.data).get_result()
            self.output_result.print_result(self.result,
                                            self.user_input.first_number,
                                            self.user_input.second_number,
                                            self.user_input.operator
                                            )
            self.user_input.want_repeat()

    def _check_data(self):
        """Check input data."""
        if CheckData.check_division_by_zero(self.user_input.second_number, self.user_input.operator):
            return True
        if CheckData.check_nums(self.user_input.first_number, self.user_input.second_number):
            return True
        if CheckData.check_op(self.user_input.operator):
            return True


if __name__ == '__main__':
    calculator = Calculator()
    calculator.run()
