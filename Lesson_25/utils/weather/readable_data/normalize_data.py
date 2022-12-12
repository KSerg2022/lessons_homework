"""Create data for human-readable viewing."""
import json

from app.handlers.get_apy_id_weather import get_apy_id
from utils.weather.getting_weather import get_weather

def normalize_data(data):
    """Writing to file human-readable data."""
    filename = 'readable_data.json'
    with open(filename, 'w') as file_json:
        json.dump(data, file_json, indent=4)
    return True


if __name__ == '__main__':
    city_name = 'Tokyo'
    apy_id = get_apy_id()
    data_json = get_weather(city_name, apy_id)
    normalize_data(data_json)
