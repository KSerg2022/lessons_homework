"""Gets the weather for each city."""
from utils.weather.getting_weather import main as getting_weather


def get_weather_for_cities(cities):
    """Gets the weather for each city."""
    results = []
    for city in cities:
        try:
            result = getting_weather(city.name)
        except RuntimeError:
            result = ''

        results.append(result)
    return zip(cities, results)
