""""""
import requests
import re
from datetime import datetime
from collections import defaultdict
from functools import lru_cache

from app.handlers.get_apy_id_weather import get_apy_id
from utils.weather.getting_weather import get_weather_icon_url, get_country_name


def get_weather_5d(city: str, apy_id: str, country_code: str = None):
    """Get weather to city name"""
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&appid={apy_id}&units=metric'
    response = requests.get(url)
    if response.status_code != 200:
        message = f'openweathermap.org returned non-200 code. Actual code is: {response.status_code},' \
                  f' message is: {response.json()["message"]}'
        raise RuntimeError(message)
    return response.json()


def parse_weather_data(city_weather: dict):
    """Parse weather data"""
    country_name = get_country_name(city_weather['city']['country'])

    forecast = defaultdict(list)
    for weather in city_weather['list']:

        date = datetime.utcfromtimestamp(weather['dt']).strftime('%Y-%m-%d')
        time = datetime.utcfromtimestamp(weather['dt']).strftime('%H:%M:%S')
        temperature = weather['main']['temp']
        description = weather['weather'][0]['description']
        clouds = weather['clouds']['all']
        wind_speed = weather['wind']['speed']
        icon_url = get_weather_icon_url(weather['weather'][0]['icon'])

        weather_data = {
            'time': time,
            'temperature': temperature,
            'description': description,
            'clouds': clouds,
            'wind_speed': wind_speed,
            'icon_url': icon_url,
        }
        forecast[date].append(weather_data)

    all_weather_data = {
        'country_name': country_name,
        'forecast': forecast,
    }
    return all_weather_data


@lru_cache(maxsize=100)
def main(city_name, country_code=None):
    """Main controller"""
    apy_id = get_apy_id()

    try:
        city_weather = get_weather_5d(city_name, apy_id, country_code)
    except RuntimeError as error:
        message = re.findall(r'(?<=message is: ).*', str(error)).pop().capitalize()
        return {'error': message}
    else:
        weather_data = parse_weather_data(city_weather)
    return weather_data
