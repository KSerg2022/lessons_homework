"""Create data for human-readable viewing."""
import json

from app.handlers.get_apy_id_weather import get_apy_id
from utils.weather.getting_weather import get_weather
from utils.weather.getting_forecast_5d import get_weather_5d

FILENAME = 'readable_data.json'
FORECAST_5D = 'forecast_5d.json'


def normalize_data(data):
    """Writing to file human-readable data."""

    with open(FORECAST_5D, 'w') as file_json:
        json.dump(data, file_json, indent=4)
    return True


if __name__ == '__main__':
    city_name = 'bon'
    apy_id = get_apy_id()
    data_json = get_weather_5d(city_name, apy_id)
    normalize_data(data_json)
