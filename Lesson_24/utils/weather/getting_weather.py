"""Get weather for city from openweathermap.org"""
import requests

from app.handlers.get_apy_id_weather import get_apy_id


def get_weather(city: str, apy_id: str):
    """Get weather to city name"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apy_id}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        message = f'openweathermap.org returned non-200 code. Actual code is: {response.status_code},' \
                  f' message is: {response.json()["message"]}'
        raise RuntimeError(message)

    return response.json()


def determine_temperature(city: dict):
    """Determine temperature"""
    temperature = city['main']['temp']
    if temperature > 25:
        return 'hot'
    elif 5 <= temperature <= 25:
        return 'warm'
    elif -5 <= temperature < 5:
        return 'cool'
    else:
        return 'cold'


def main(city: str):
    apy_id = get_apy_id()
    """Main controller"""
    try:
        city = get_weather(city, apy_id)
    except RuntimeError:
        return 'not'
    else:
        weather_condition = determine_temperature(city)
        return weather_condition
