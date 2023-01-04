"""Get  capitals to fill out database."""
import json
from typing import Dict, List

from countryinfo import CountryInfo
from pathlib import Path

from utils.weather.country_codes import main as get_file_json, URL_CODES_JSON, get_path_to_file_countries_codes


def read_json_file():
    """Read data from json file."""
    path_to_file_json = get_path_to_file_countries_codes()
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


def get_capitals(countries: list[dict[str]]) -> list[dict[str, str]]:
    """Get capitals for countries."""
    capitals = []
    for country in countries:
        try:
            capital_name = CountryInfo(country['code']).capital()
        except KeyError:
            continue
        if not capital_name:
            continue
        json_data = prepare_data_to_json( capital_name, country['name'])

        capitals.append(json_data)
    return capitals


def prepare_data_to_json(capital_name: str, country_name: str) -> dict[str, str]:
    """Prepare data to json"""
    json_data = {
        'capital': capital_name,
        'country': country_name,
    }
    return json_data


def get_path_to_file(filename: str):
    path_to_dir = Path(__file__).parent
    path_to_file = path_to_dir / filename
    return path_to_file


def wright_to_json_file_capitals(data: list[dict[str, str]], filename: str):
    """Wright data to file "capitals.json"."""
    path_to_file = get_path_to_file(filename)
    with open(path_to_file, 'w') as file:
        json.dump(data, file, indent=4)
    return True


def read_json_file_capitals(filename: str) -> dict[str, str] | None:
    """Get data from file "capitals.json" if it exists."""
    path_to_file = get_path_to_file(filename)
    try:
        with open(path_to_file) as file_json:
            capitals = json.load(file_json)
    except FileNotFoundError:
        return None
    return capitals


def main() -> dict[str, str] | list[dict[str, str]]:
    """Main controller"""
    capitals = read_json_file_capitals(FILENAME)
    if capitals:
        return capitals
    countries = read_json_file()
    capitals = get_capitals(countries)
    wright_to_json_file_capitals(capitals, FILENAME)
    return capitals


FILENAME = 'capitals.json'
