"""Verify inputted country name jn page 'Add city'."""
import json

from utils.weather.country_codes import main as get_file_json, URL_CODES_JSON, get_path_to_file


def read_json_file():
    """Read data from json file."""
    path_to_file_json = get_path_to_file()
    try:
        with open(path_to_file_json) as file_json:
            countries = json.load(file_json)
    except FileNotFoundError:
        get_file_json(URL_CODES_JSON)
    return countries


def get_country_names_and_codes(countries: list[dict[str]]):
    """Get list of countries names and countries codes."""
    country_names = []
    country_codes = []
    for country in countries:
        country_names.append(country['name'].lower())
        country_codes.append(country['code'].lower())
    return country_names, country_codes


def verify_country_name(country_name: str, country_names: list[str], country_codes: list[str]):
    """Verify inputted country name."""
    if not country_name:
        return True
    elif country_name.lower() in country_names:
        return True
    elif country_name.lower() in country_codes:
        return True
    else:
        return False


def main(country_name: str):
    """Main controller"""
    countries = read_json_file()
    country_names, country_codes = get_country_names_and_codes(countries)
    country_name = verify_country_name(country_name, country_names, country_codes)
    return country_name
