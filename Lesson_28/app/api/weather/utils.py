""""""
from utils.weather.generate_data.generate_data_capitels import read_json_file_capitals, FILENAME
from utils.weather.country_codes import read_codes_data_from_json


def verify_name_capital(capital_name: str):
    """Checking if such a capital name exists"""
    capitals_json = read_json_file_capitals(FILENAME)
    for capital in capitals_json:
        if capital['capital'] == capital_name:
            return True
    return False


def verify_name_country(country_name: str):
    """Checking if such a country name exists."""
    countries_json = read_codes_data_from_json()
    for country in countries_json:
        if country['name'] == country_name:
            return True
    return False


def get_country_code(country_name: str):
    """Get country code."""
    countries_json = read_codes_data_from_json()
    for capital in countries_json:
        if capital['name'] == country_name:
            return capital['code']

