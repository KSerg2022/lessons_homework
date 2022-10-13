"""The probability of getting the sum of numbers when throwing two dice."""
from random import randint
from collections import Counter
from prettytable import PrettyTable
from datetime import datetime


def calc_time(func):
    """Calc execution time"""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        func_result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f'Execution time {func.__name__}: {end_time - start_time}')
        return func_result
    return wrapper


def roll_dice(die: int) -> int:
    """Roll die."""
    return randint(1, die)


def throwing_dices(die_1: int, die_2: int, throws: int) -> dict:
    """Throw the dice a certain number of times, fix the results by summing the resulting values."""
    results = [roll_dice(die_1) + roll_dice(die_2) for _ in range(throws)]
    return Counter(results)


def get_frequency_number(result: dict, throws: int) -> dict:
    """Calculate the % chance of a number."""
    return {position: round(result[position] / throws * 100, 2) for position in result}


def get_all_expected_variants(die_1: int, die_2: int) -> list[int]:
    """Get all possible variants for roll two dice."""
    return [value_1 + value_2 for value_1 in range(1, die_1 + 1) for value_2 in range(1, die_2 + 1)]


def get_expected_results(die_1: int, die_2: int) -> dict:
    """Getting the expected result according to the theory of probability."""
    all_variants = get_all_expected_variants(die_1, die_2)
    len_all_variants = len(all_variants)
    all_variants = sorted(Counter(all_variants).items(), key=lambda x: x[0])
    return {position: round(value / len_all_variants * 100, 2) for position, value in all_variants}


def create_table(frequency_data: dict, expected_data: dict) -> PrettyTable:
    """Print statistics in table."""
    result_table = PrettyTable()
    result_table.field_names = ['Exodus', 'Simulation percentage', 'Expected result']
    for position_exp in expected_data:
        for position_fr in frequency_data:
            result = frequency_data[position_fr]
            if position_exp == position_fr:
                result_table.add_row([position_exp, result, expected_data[position_exp]])
    return result_table


def wright_to_file(die_1: int, die_2: int, data: PrettyTable) -> bool:
    """Wright ot file result table."""
    filename = f"table_results_roll_ two_ dice_d{die_1}_d{die_2}.txt"
    with open(filename, 'w') as f:
        print(data, file=f)
    return True


def print_result(data: PrettyTable) -> None:
    """Print."""
    return print(data)


@calc_time
def main(die_1: int, die_2: int, throws: int):
    """Main controller."""
    result_of_throwing = throwing_dices(die_1, die_2, throws)

    frequency_result = get_frequency_number(result_of_throwing, throws)
    expected_result = get_expected_results(die_1, die_2)

    result_table = create_table(frequency_result, expected_result)

    wright_to_file(die_1, die_2, result_table)
    print_result(result_table)


if __name__ == '__main__':
    die1 = 6
    die2 = 6
    number_of_throws = 1000
    main(die1, die2, number_of_throws)
