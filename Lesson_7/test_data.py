"""Check functions."""

def check_file_txt(file_txt):
    """Check file for type txt and check if the file exists."""
    try:
        open(file_txt, mode='rt').readline()
    except UnicodeDecodeError:
        return 'App can use only text files'
    except FileNotFoundError:
        return 'File not found.'
    return False


def verification_incoming_data_value(data: str):
    """Checking the correctness of the input"""
    try:
        isinstance(int(data), int)
    except ValueError:
        return f"You entered '{data}'.\nYou need to enter an integer value.\n"
    return False


def verification_range_of_data(data: str, file: dict[list]) -> bool | str:
    """Checking the allowable range of the number of protons."""
    if int(data) <= 0 or int(data) > len(file):
        return f"You need to enter an integer value between 0 and {len(file)}."
    return False


def verification_range_of_data_args(data: str, file: list[list]) -> bool | str:
    """Checking the allowable range of the number of protons."""
    if int(data) <= 0 or int(data) > len(file):
        return f"You need to enter an integer value between 0 and {len(file)}.\n"
    return False
