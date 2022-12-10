"""Gets the weather for each city."""
from weather.getting_weather import main, APP_ID


def get_weather_for_cities(cities):
    """Gets the weather for each city."""
    results = []
    for city in cities:
        try:
            result = main(city.name, APP_ID)
        except RuntimeError:
            result = ''

        results.append(result)
    return zip(cities, results)
