"""Modul Operation"""
from typing import NamedTuple


class Operation(NamedTuple):
    """Initialization class Operation."""
    first_number: str = ''
    second_number: str = ''
    operator: str = ''

    def get_result(self) -> float:
        """Get the desired result."""
        match self:
            case Operation(operator='+'):
                return float(self.first_number) + float(self.second_number)
            case Operation(operator='-'):
                return float(self.first_number) - float(self.second_number)
            case Operation(operator='*'):
                return float(self.first_number) * float(self.second_number)
            case Operation(operator='/'):
                return float(self.first_number) / float(self.second_number)
            case _:
                raise 'Operator must be - +,-,*, /'
