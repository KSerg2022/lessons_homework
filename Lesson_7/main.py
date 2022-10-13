"""The program returns information about chemical elements: designation, name and number of protons."""
from parsing import parse_ars

from test_data import (check_file_txt,
                       verification_incoming_data_value,
                       verification_range_of_data_args)
from working_with_file import (get_path_to_file, read_data_from_file_to_list)


def find_information(protons: str, s_name: str, f_name: str, file: list[list]) -> bool | str:
    """Returns information about chemical elements on the entered request."""
    for line in file:
        result = [value for value in line if
                  value == protons.upper() or value == s_name.upper() or value == f_name.upper()]
        if result:
            print(f'The element with -{line[0]}- protons is "{line[2].title()}"'
                  f' that has the designation "{line[1].title()}".\n')
            exit()
    return False


def main(protons='', s_name='', f_name=''):
    current_file = get_path_to_file()

    check = check_file_txt(current_file)
    if check:
        print(check)
        exit()

    working_file = read_data_from_file_to_list(current_file)

    if protons != '':
        verification_type = verification_incoming_data_value(protons)
        if verification_type:
            print(verification_type)
            exit()

    if protons != '':
        verification_range = verification_range_of_data_args(protons, working_file)
        if verification_range:
            print(verification_range)
            exit()

    result = find_information(protons, s_name, f_name, working_file)
    if not result:
        print(f'No data found for your request.')
        exit()


if __name__ == '__main__':
    cli_args = parse_ars()
    qwt_protons = cli_args.qwt_protons
    shot_name = cli_args.shot_name
    full_name = cli_args.full_name

    main(qwt_protons, shot_name, full_name)
