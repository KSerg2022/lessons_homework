def ins_even_result(odd, numbers):
    '''
    Function of insert even numbers into sorted list with odd numbers.
    :param odd: List of sorted odd numbers.
    :param even: Inition array of numbers.
    :return: List of result.
    '''

    for number in numbers:
        if int(number) % 2 == 0:
            odd.insert(numbers.index(number), number)
    return odd


def main(array):
    sort_odd_numbers = sorted(list(filter(lambda x: x % 2 != 0, array)))
    return ins_even_result(sort_odd_numbers, array)


if __name__ == '__main__':
    CASES = (
        ([3, 1], [1, 3,]),
        ([3, 2, -1, 4], [-1, 2, 3, 4]),
        ([5, 3, 2, 8, 1, 4], [1, 3, 2, 8, 5, 4])
    )
    for cases, answer in CASES:
        assert main(cases) == answer
        print(f'\nincoming data - {cases}\n\tsolution - {main(cases)}\n\tverification answer - {answer}')
