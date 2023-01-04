from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request

from app.weather.models import City, Country
from utils.weather.getting_weather import main as getting_weather
from app.handlers.get_apy_id_weather import get_apy_id

# /api/v1/cities/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class Cities(Resource):
    """API for cities"""
    def __init__(self):
        self.cities = None
        self.request = None
        self.api_key = get_apy_id()
        self.data_cities = None

    def get(self):
        """HTTP method GET"""
        self.cities = City.select()
        self.cities = self.prepare_cities_to_json()
        return make_response(jsonify(self.cities), 200)

    def post(self):
        """HTTP method POST.
        [
        {"name": "lviv"},
        ]
        """
        self.data_cities = request.get_json()
        if not self.data_cities:
            response = {'message': "you didn't send anything"}
            return make_response(jsonify(response), 200)

        weather_error = []
        check_cities = []
        for city in self.data_cities:
            city_name = city.get('name').capitalize()

            check_city = City.select().where(City.name == city_name).first()
            if check_city:
                response = {'message': f'"{city_name}" already in database.'}
                check_cities.append(response)
                continue

            city_weather = getting_weather(city_name, self.api_key)
            if 'error' in city_weather:
                response = {'message': f'City "{city_name}" is {city_weather}'}
                weather_error.append(response)
                continue
            country = Country.select().where(Country.code == city_weather['country_code']).first()

            city = City(
                name=city_name,
                country=country.id
            )
            city.save()

        if weather_error or check_cities:
            return make_response(jsonify(weather_error, check_cities), 200)

        return make_response('', 201)

    def put(self):
        """HTTP method PUT.
        [
        {"id": 3, "name": "lviv"},
        ]
        """
        self.data_cities = request.get_json()
        if not self.data_cities:
            response = {'message': "you didn't send anything"}
            return make_response(jsonify(response), 200)

        not_id = []
        city_not_found = []
        weather_error = []
        check_cities = []
        for city in self.data_cities:
            city_name = city.get('name').capitalize()
            city_id = city.get("id")

            if not city_id:
                response = {'message': f'City name {city_name} have not "id"!'}
                not_id.append(response)
                continue

            city = City.select().where(City.id == city_id).first()
            if not city:
                response = {'message': f'City with id {city_id} not found in db.'}
                city_not_found.append(response)
                continue

            check_city = City.select().where(City.name == city_name).first()
            if check_city:
                response = {'message': f'"{city_name}" already in database.'}
                check_cities.append(response)
                continue

            city_weather = getting_weather(city_name, self.api_key)
            if 'error' in city_weather:
                response = {'message': f'City "{city_name}" is {city_weather}'}
                weather_error.append(response)
                continue
            country = Country.select().where(Country.code == city_weather['country_code']).first()

            city.name = city_name
            city.country = country
            city.save()

        if not_id or city_not_found or weather_error or check_cities:
            return make_response(jsonify(not_id, city_not_found, weather_error, check_cities), 200)

        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE. Delete all cities."""
        City.delete().execute()
        return make_response('', 204)

    def prepare_cities_to_json(self):
        """Prepare cities for json format"""
        cities = []
        for city in self.cities:
            city_temp = {
                'id': city.id,
                'name': city.name,
                'country_id': city.country.id
            }
            cities.append(city_temp)
        return cities
