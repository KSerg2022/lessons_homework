import pytest

from utils.weather.generate_data_capitels import *
from utils.weather.country_codes import get_path_to_file


def test_read_json_file():
    path = get_path_to_file() / '1'
    result = read_json_file()
    assert isinstance(result, list) is True

    with pytest.raises(FileNotFoundError) as context_error:
        open(path)
    print(str(context_error.value))
    assert 'No such file or directory' in str(context_error.value)


def test_main():
    result = main()
    assert isinstance(result, list) is True



