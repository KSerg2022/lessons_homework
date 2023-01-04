"""Create json file with country codes and names."""
import json
from datapackage import Package, DataPackageException
from pathlib import Path


def get_codes(url: str):
    """Get countries codes from datapackage json"""
    try:
        package = Package(url)
    except DataPackageException:
        return None
    else:
        for resource in package.resources:
            if resource.descriptor['datahub']['type'] == 'derived/csv':
                return resource.read()


def prepare_data_to_json(codes: list[list[str]]):
    """Prepare data to json"""
    json_data = []
    for country_code in codes:
        country = {
            'code': country_code[1],
            'name': country_code[0],
        }
        json_data.append(country)
    return json_data


def get_path_to_file_countries_codes():
    path_to_file = Path(__file__).parent.absolute()
    path_to_file_json = path_to_file / FILENAME
    return path_to_file_json


def write_codes_data_to_json(json_data: list[dict[str]]):
    """Write codes data to json file"""
    path_to_file_json = get_path_to_file_countries_codes()
    with open(path_to_file_json, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    return True


def read_codes_data_from_json(filename=None):
    """Read codes from json file"""
    filename = get_path_to_file_countries_codes()
    with open(filename) as json_file:
        country_json = json.load(json_file)
    return country_json


def main(url: str):
    """Main controller"""
    codes = get_codes(url)
    if not codes:
        raise RuntimeError('Countries codes data not found')
    json_data = prepare_data_to_json(codes)
    write_json = write_codes_data_to_json(json_data)
    return write_json


URL_CODES_JSON = 'https://datahub.io/core/country-list/datapackage.json'
FILENAME = 'countries_codes.json'
