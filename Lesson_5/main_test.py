
def verification_incoming_data_type(data: (list[int])) -> bool:
    """checks data according for type matching"""
    if not isinstance(data, list):
        return False

    len_numbers = len([number for number in data if isinstance(number, int)])
    return len_numbers == len(data)


def exponentiation_number(data: int) -> int:
    """Raises each digit from a number to a power equal to the ordinal number and sums the result among themselves"""
    index = 0
    result = 0
    while index < len(str(data)):
        number = int(str(data)[index]) ** (index + 1)
        result += number
        index += 1
    return result


def get_result(incoming_data: list[int]) -> list[int]:
    """Get a list with a total value"""
    start_num = int(incoming_data[0])
    end_num = int(incoming_data[1])
    result_array = [number for number in range(start_num, end_num) if number == exponentiation_number(number)]
    return result_array


def main(incoming_data: list[int]) -> list[int] | str | None:
    if not verification_incoming_data_type(incoming_data):
        return print(f'Incoming data type must be list[int], not {incoming_data}, can not take')

    result_array = get_result(incoming_data)
    return result_array


if __name__ == '__main__':
    CASES = (
        ([1, '10'], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([1, 100], [1, 2, 3, 4, 5, 6, 7, 8, 9, 89]),
        ([90, 100], []),
    )
    for cases, answer in CASES:
        try:
            main(cases) == answer
        except TypeError:
            break
        print(f'\n{cases} incoming data,\n{main(cases)} solution,\n{answer} verification answer.')
