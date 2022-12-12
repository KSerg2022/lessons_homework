"""Create list of capitals to fill out database."""
from random import randint
import json
from typing import NamedTuple
from countryinfo import CountryInfo

from utils.weather.country_codes import main as get_file_json, URL_CODES_JSON, get_path_to_file


class Capitals(NamedTuple):
    country: str
    capital: str


def read_json_file():
    path_to_file_json = get_path_to_file()
    try:
        with open(path_to_file_json) as file_json:
            countries = json.load(file_json)
    except FileNotFoundError:
        get_file_json(URL_CODES_JSON)
    else:
        if len(countries) < 50:
            get_file_json(URL_CODES_JSON)
            countries = read_json_file()
        return countries


def get_capitals(countries: list[dict[str]]):
    capitals = []
    qty = 0
    while qty < 25:
        country = countries.pop(randint(1, len(countries) - 1))
        country_name = country['name']
        try:
            capital_name = CountryInfo(country_name).capital()
        except KeyError:
            continue
        if not capital_name:
            continue
        capitals.append(Capitals(country_name, capital_name))
        qty += 1
    capitals = sorted(capitals, key=lambda x: x[1])
    return capitals


def main():
    countries = read_json_file()
    capitals = get_capitals(countries)
    return capitals
