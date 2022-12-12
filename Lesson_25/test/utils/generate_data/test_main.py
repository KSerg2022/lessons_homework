from utils.generate_data.data import emails_data
from utils.generate_data.main import *


def test_generate_full_names():
    data = generate_full_names(emails_data)
    assert isinstance(data, list) is True

