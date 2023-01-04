"""Generate cities for database."""
import json
from pathlib import Path
from collections import defaultdict
from random import randint, shuffle


CITIES_JSONFILE = 'cities.json'
UA_COUNTRY_CODE = 'UA'
FIVE_COUNTRIES = ('UA', 'JP', 'GB', 'US', 'AU')


def get_pat_to_jsonfile(file_json):
    """Get path to json file 'cities.json'."""
    path_to_dir = Path(__file__).parent.absolute()
    path_to_cities_jsonfile = path_to_dir / file_json
    return path_to_cities_jsonfile


def read_data_from_jsonfile(path_to_file: Path):
    """Read cities from json file."""
    with open(path_to_file, encoding='UTF-8') as file_json:
        data = json.load(file_json)
    return data


def get_cities(all_cities: list[dict[str]]) -> defaultdict[str, list[str]]:
    """Get cities for all countries."""
    data = defaultdict(list)
    for city in all_cities:
        data[city['country']].append(city['name'])
    return data


def get_cities_for_countries(all_cities: list[dict[str]]) -> defaultdict[str, list[str]]:
    """Get cities for five countries."""
    cities = defaultdict(list)
    for city in all_cities:
        if city['country'] in FIVE_COUNTRIES:
            cities[city['country']].append(city['name'])
    return cities


def fifty_cities_for_5_country(cities_for_5_country: dict[str, list[str]]) -> list[dict[str, str]]:
    """Get ten cities for each country."""
    selected_cities = []
    for country, cities in cities_for_5_country.items():
        for _ in range(10):
            city = {
                'country': country,
                'city_name': cities.pop(randint(1, len(cities) - 1))
            }
            selected_cities.append(city)
    return selected_cities


def get_ua_cities() -> dict[str, list[str]]:
    """Get cities for Ukraine."""
    path_to_file_json = get_pat_to_jsonfile(CITIES_JSONFILE)
    all_cities = read_data_from_jsonfile(path_to_file_json)
    cities = {UA_COUNTRY_CODE: [city['name'] for city in all_cities if city['country'] == UA_COUNTRY_CODE]}
    return cities


def get_all_cities() -> defaultdict[str, list[str]]:
    """Get cities for all countries."""
    path_to_file_json = get_pat_to_jsonfile(CITIES_JSONFILE)
    all_cities = read_data_from_jsonfile(path_to_file_json)
    cities = get_cities(all_cities)
    return cities


def get_cities_for_5_country() -> list[dict[str, str]]:
    """Get ten cities for each country from list."""
    path_to_file_json = get_pat_to_jsonfile(CITIES_JSONFILE)
    all_cities = read_data_from_jsonfile(path_to_file_json)
    cities_for_5_country = get_cities_for_countries(all_cities)
    cities = fifty_cities_for_5_country(cities_for_5_country)
    shuffle(cities)
    return cities


