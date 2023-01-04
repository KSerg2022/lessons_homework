from flask_restful import Resource, reqparse
from flask import make_response, jsonify


from app.weather.models import Capital, Country
from utils.weather.getting_weather import main as getting_weather
from app.handlers.get_apy_id_weather import get_apy_id
from app.api.weather.utils import verify_name_capital

# /api/v1/capitals/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class Capitals(Resource):
    """API for cities"""
    def __init__(self):
        self.capitals = None
        self.request = None
        self.api_key = get_apy_id()
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self):
        """HTTP method GET"""
        self.capitals = Capital.select()
        self.capitals = self.prepare_capitals_to_json()
        return make_response(jsonify(self.capitals), 200)

    def post(self):
        """HTTP method POST. {"name": "lviv"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()

        if not verify_name_capital(self.request.name):
            response = {'message': f'city name {self.request.name} is not capital'}
            return make_response(jsonify(response), 200)

        city_weather = getting_weather(self.request.name, self.api_key)
        if 'error' in city_weather:
            return make_response(jsonify(city_weather), 500)
        country = Country.select().where(Country.code == city_weather['country_code']).first()
        city_check = Capital.select().where(Capital.name == self.request.name).first()
        if city_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)

        capital = Capital(
            name=self.request.name,
            country=country.id
        )
        capital.save()
        return make_response('', 201)

    def put(self):
        """HTTP method PUT. {"id": 3, "name": "lviv"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        if not self.request.id:
            response = {'message': 'field id is necessary.'}
            return make_response(jsonify(response), 200)

        if not verify_name_capital(self.request.name):
            response = {'message': f'city name {self.request.name} is not capital'}
            return make_response(jsonify(response), 200)

        capital = Capital.select().where(Capital.id == self.request.id).first()
        if not capital:
            response = {'message': f'capital with id {self.request.id} not found.'}
            return make_response(jsonify(response), 200)

        city_weather = getting_weather(self.request.name, self.api_key)
        if 'error' in city_weather:
            return make_response(jsonify(city_weather), 500)
        country = Country.select().where(Country.code == city_weather['country_code']).first()
        city_check = Capital.select().where(Capital.name == self.request.name).first()
        if city_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)

        capital.name = self.request.name
        capital.country = country
        capital.save()
        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE"""
        Capital.delete().execute()
        return make_response('', 204)

    def prepare_capitals_to_json(self):
        """Prepare cities for json format"""
        capitals = []
        for capital in self.capitals:
            capital_temp = {
                'id': capital.id,
                'name': capital.name,
                'country_id': capital.country.id
            }
            capitals.append(capital_temp)
        return capitals
