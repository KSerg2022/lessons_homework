"""Get weather for city from openweathermap.org"""
import requests


def get_weather(city: str, api_id: str):
    """Get weather to city name"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_id}&units=metric'
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


def main(city: str, app_id: str):
    """Main controller"""
    city = get_weather(city, app_id)
    weather_condition = determine_temperature(city)
    return weather_condition


APP_ID = '402d150cc39854f9d464c714a56dcf36'

if __name__ == '__main__':
    city_name = 'Tolkyo'
    print(main(city_name, APP_ID))
