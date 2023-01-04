from flask_restful import Resource, reqparse
from flask import make_response, jsonify

from app.weather.models import City, Country
from utils.weather.getting_weather import main as getting_weather
from app.handlers.get_apy_id_weather import get_apy_id

# /api/v1/cities/<city_id>/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class CityName(Resource):
    """API for cities"""
    def __init__(self):
        self.city = None
        self.request = None
        self.api_key = get_apy_id()
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self, city_id=None):
        """HTTP method GET"""
        city = City.select().where(City.id == city_id).first()
        if not city:
            response = {'message': f'city with id {city_id} not found.'}
            return make_response(jsonify(response), 200)

        self.city = City.select().where(City.id == city_id).dicts().get()
        return make_response(jsonify(self.city), 200)

    def post(self, city_id=None):
        """HTTP method POST."""
        response = {'message': f'method "POST" is disable.'}
        return make_response(jsonify(response), 200)

    def put(self, city_id=None):
        """HTTP method PUT. {"name": "lviv"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        if not city_id:
            response = {'message': 'field id is necessary.'}
            return make_response(jsonify(response), 200)

        city = City.select().where(City.id == city_id).first()
        if not city:
            response = {'message': f'city with id {city_id} not found.'}
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

    def delete(self, city_id=None):
        """HTTP method DELETE.  Delete city with id=capital_id."""
        city = City.select().where(City.id == city_id).first()
        if not city:
            response = {'message': f'city with id {city_id} not found.'}
            return make_response(jsonify(response), 200)

        City.delete_by_id(city_id)
        return make_response('', 204)
