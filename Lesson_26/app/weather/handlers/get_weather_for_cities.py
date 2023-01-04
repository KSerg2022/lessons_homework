"""Gets the weather for each city."""
from functools import lru_cache
from peewee import DoesNotExist

from app.weather.models import Capital, City
from utils.weather.getting_weather import main as getting_weather


@lru_cache(maxsize=50)
def get_weather_for_cities(cities):
    """Gets the weather for each city."""
    results = []
    for city in cities:
        try:
            result = getting_weather(city.name, city.country.code)
        except RuntimeError:
            result = 0
        if 'error' in result.keys():
            try:
                city_to_dell = City.get(City.id == city)
            except DoesNotExist:
                pass
            else:
                city_to_dell.delete_instance()

            try:
                city_to_dell = Capital.get(Capital.id == city)
            except DoesNotExist:
                pass
            else:
                city_to_dell.delete_instance()

            city.delete()

        results.append(result)
    return zip(cities, results)
