"""Generate cities for database."""
import json
from pathlib import Path
from collections import defaultdict


CITIES_JSONFILE = 'cities.json'
UA_COUNTRY_CODE = 'UA'


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


def get_cities(all_cities: list[dict[str]]):
    """Get cities for all countries."""
    d = defaultdict(list)
    for city in all_cities:
        d[city['country']].append(city['name'])
    return d


def get_ua_cities():
    """Get cities for Ukraine."""
    path_to_file_json = get_pat_to_jsonfile(CITIES_JSONFILE)
    all_cities = read_data_from_jsonfile(path_to_file_json)
    cities = {UA_COUNTRY_CODE: [city['name'] for city in all_cities if city['country'] == UA_COUNTRY_CODE]}
    return cities


def get_all_cities():
    """Main controller"""
    path_to_file_json = get_pat_to_jsonfile(CITIES_JSONFILE)
    all_cities = read_data_from_jsonfile(path_to_file_json)
    cities = get_cities(all_cities)
    return cities


# q = get_ua_cities()
# print(len(q))
# print(q)

# w = get_all_cities()
# print(len(w))
# print(w.keys())
# print(w['AD'])
# print(w['UA'])
# print(len(w['UA']))

