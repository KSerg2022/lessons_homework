"""Modul output result."""


class OutputResult:
    """Initialization class OutputResult."""

    @staticmethod
    def print_result(result: float, first_num: str, second_num: str, operator: str):
        """Print result to console."""
        print(
            f'You want to do {first_num} {operator} {second_num}.'
            f' Result = {result}'
            )
