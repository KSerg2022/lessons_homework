import argparse


def parse_ars():
    """Parse CLI args"""
    parser = argparse.ArgumentParser(
        prog='Finding information about a chemical element -',
        usage='%(prog)s main.py [-qp], [-sn], [-fn]',
        description=f'The program displays the designation and name of the chemical element\nwith the number of protons.'
    )
    parser.add_argument(
        '-qp',
        dest='qwt_protons',
        type=str,
        help='The number of protons.',
        required=False,
        default=''
    )
    parser.add_argument(
        '-sn',
        dest='shot_name',
        type=str,
        help='Abbreviation for a chemical element',
        required=False,
        default=''
    )
    parser.add_argument(
        '-fn',
        dest='full_name',
        type=str,
        help='Full name for a chemical element',
        required=False,
        default=''
    )

    args = parser.parse_args()
    return args
