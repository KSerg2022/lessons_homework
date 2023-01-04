from flask_restful import Resource, reqparse
from flask import make_response, jsonify

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
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self):
        """HTTP method GET"""
        self.cities = City.select()
        self.cities = self.prepare_cities_to_json()
        return make_response(jsonify(self.cities), 200)

    def post(self):
        """HTTP method POST. {"name": "lviv"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()

        city_weather = getting_weather(self.request.name, self.api_key)
        if 'error' in city_weather:
            return make_response(jsonify(city_weather), 500)
        country = Country.select().where(Country.code == city_weather['country_code']).first()
        city_check = City.select().where(City.name == self.request.name).first()
        if city_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)
        city = City(
            name=self.request.name,
            country=country.id
        )
        city.save()
        return make_response('', 201)

    def put(self):
        """HTTP method PUT. {"id": 3, "name": "lviv"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        if not self.request.id:
            response = {'message': 'field id is necessary.'}
            return make_response(jsonify(response), 200)

        city = City.select().where(City.id == self.request.id).first()
        if not city:
            response = {'message': f'city with id {self.request.id} not found.'}
            return make_response(jsonify(response), 200)

        city_weather = getting_weather(self.request.name, self.api_key)
        if 'error' in city_weather:
            return make_response(jsonify(city_weather), 500)
        country = Country.select().where(Country.code == city_weather['country_code']).first()
        city_check = City.select().where(City.name == self.request.name).first()
        if city_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)

        city.name = self.request.name
        city.country = country
        city.save()
        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE"""
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
