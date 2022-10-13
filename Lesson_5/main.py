
def verification_incoming_data_value() -> int:
    """Entering the value of the sequence size and checking the correctness of the input"""
    while True:
        data = input(f'Enter size of array: ')
        try:
            isinstance(int(data), int)
        except ValueError:
            print(f"You didn't enter a number!\n")
        else:
            break
    return int(data)


def exponentiation_number(data: int) -> int:
    """Raises each digit from a number to a power equal to the ordinal number and sums the result among themselves"""
    splitted_number = [int(number) for number in str(data)]
    square_number = map(lambda x: x ** (splitted_number.index(x) + 1), splitted_number)
    return sum(number for number in square_number)


def get_result(size_array: int) -> list[int]:
    """Get a list with a total value"""
    result_array = [number for number in range(1, size_array) if number == exponentiation_number(number)]
    return result_array


def main():
    """Main function"""
    size_array = verification_incoming_data_value()
    result_array = get_result(size_array)
    return print(result_array)


if __name__ == '__main__':
    main()
