"""Get weather for city from openweathermap.org"""
import requests
import re
import json
from functools import lru_cache

from app.handlers.get_apy_id_weather import get_apy_id
from utils.weather.country_codes import main as get_file_json, URL_CODES_JSON, get_path_to_file_countries_codes


def get_weather(city: str, country_code: str, apy_id: str):
    """Get weather to city name"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={apy_id}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        message = f'openweathermap.org returned non-200 code. Actual code is: {response.status_code},' \
                  f' message is: {response.json()["message"]}'
        raise RuntimeError(message)

    return response.json()


def get_weather_icon_url(icon_name: str):
    """Get weather url icon"""
    icon_url = f'http://openweathermap.org/img/w/{icon_name}.png'
    return icon_url


def parse_weather_data(city_weather: dict):
    """Parse weather data"""
    city_name = city_weather['name']
    icon_name = city_weather['weather'][0]['icon']
    country_code = city_weather['sys']['country']
    country_name = get_country_name(country_code)

    icon_url = get_weather_icon_url(icon_name)
    latitude = city_weather['coord']['lat']
    longitude = city_weather['coord']['lon']
    sky = city_weather['weather'][0]['description']
    temperature = city_weather['main']['temp']
    wind_speed = city_weather['wind']['speed']

    weather_data = {
        'city_name': city_name,
        'country_name': country_name,
        'country_code': country_code,
        'latitude': latitude,
        'longitude': longitude,
        'sky': sky,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'icon_url': icon_url,
    }

    return weather_data


def get_country_name(country_code):
    path_to_file_json = get_path_to_file_countries_codes()
    try:
        with open(path_to_file_json) as file_json:
            countries = json.load(file_json)
    except FileNotFoundError:
        get_file_json(URL_CODES_JSON)
    else:
        for country in countries:
            if country['code'] == country_code:
                country_name = country['name']
                return country_name


@lru_cache(maxsize=100)
def main(city_name, country_code=None):
    """Main controller"""
    apy_id = get_apy_id()
    try:
        city_weather = get_weather(city_name, country_code, apy_id)
    except RuntimeError as error:
        message = re.findall(r'(?<=message is: ).*', str(error)).pop().capitalize()
        return {'error': message}
    weather_data = parse_weather_data(city_weather)
    return weather_data
