"""Gets the weather for each city."""
from functools import lru_cache
from utils.weather.getting_weather import main as getting_weather, APP_ID


@lru_cache(maxsize=50)
def get_weather_for_cities(cities):
    """Gets the weather for each city."""
    results = []

    for city in cities:
        try:
            result = getting_weather(city.name, APP_ID)
        except RuntimeError:
            result = 0
        if 'error' in result.keys():
            city.delete()
        if 'error' not in result.keys():
            results.append(result)
    return zip(cities, results)
