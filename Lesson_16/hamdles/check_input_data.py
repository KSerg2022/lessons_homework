"""Modul check input data."""


class CheckData:
    """Initialization class CheckData."""

    @staticmethod
    def check_nums(first_num: str, second_num: str) -> bool:
        """Check numbers of float type"""
        try:
            float(first_num)
            float(second_num)
        except ValueError as error:
            print(f"You entered operand '{first_num}' and '{second_num}'. {str(error).capitalize()}.\n")
            return True
        return False

    @staticmethod
    def check_op(operation: str) -> bool:
        """Check user value in +,-,*, /"""
        if operation in {'+', '-', '*', '/'}:
            return False
        else:
            print(f"\nYou entered operand - '{operation}', but operand may be - ('+', '-', '*', '/').\n")
            return True

    @staticmethod
    def check_division_by_zero(second_num: str, operator: str) -> bool:
        """Check division by zero."""
        if operator == '/' and not float(second_num):
            print('Zero division error.\n')
            return True
        else:
            return False
