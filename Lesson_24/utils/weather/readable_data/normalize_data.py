"""Create data for human-readable viewing."""
import json

from utils.weather.getting_weather import get_weather, APP_ID


def normalize_data(data):
    """Writing to file human-readable data."""
    filename = 'readable_data.json'
    with open(filename, 'w') as file_json:
        json.dump(data, file_json, indent=4)
    return True


if __name__ == '__main__':
    city_name = 'Tokyo'
    data_json = get_weather(city_name, APP_ID)
    normalize_data(data_json)
