from flask_restful import Resource, reqparse
from flask import make_response, jsonify

from app.weather.models import Capital, Country
from utils.weather.getting_weather import main as getting_weather
from app.handlers.get_apy_id_weather import get_apy_id
from app.api.weather.utils import verify_name_capital

# /api/v1/capitals/<city_id>/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class CapitalName(Resource):
    """API for cities"""
    def __init__(self):
        self.capital = None
        self.request = None
        self.api_key = get_apy_id()
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self, capital_id):
        """HTTP method GET"""
        capital = Capital.select().where(Capital.id == capital_id).first()
        if not capital:
            response = {'message': f'capital with id {capital_id} not found.'}
            return make_response(jsonify(response), 200)

        self.capital = Capital.select().where(Capital.id == capital_id).dicts().get()
        return make_response(jsonify(self.capital), 200)

    def post(self, capital_id=None):
        """HTTP method POST."""
        response = {'message': f'method "POST" is disable.'}
        return make_response(jsonify(response), 200)

    def put(self, capital_id=None):
        """HTTP method PUT. {"name": "Kiev"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        
        if not verify_name_capital(self.request.name):
            response = {'message': f'capital name {self.request.name} is not capital'}
            return make_response(jsonify(response), 200)

        if not capital_id:
            response = {'message': 'field id is necessary.'}
            return make_response(jsonify(response), 200)

        capital = Capital.select().where(Capital.id == capital_id).first()
        if not capital:
            response = {'message': f'capital with id {capital_id} not found.'}
            return make_response(jsonify(response), 200)

        capital_weather = getting_weather(self.request.name, self.api_key)
        if 'error' in capital_weather:
            return make_response(jsonify(capital_weather), 500)

        country = Country.select().where(Country.code == capital_weather['country_code']).first()
        city_check = Capital.select().where(Capital.name == self.request.name).first()
        if city_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)

        capital.name = self.request.name
        capital.country = country
        capital.save()
        return make_response('', 204)

    def delete(self, capital_id=None):
        """HTTP method DELETE. Delete capital with id=capital_id."""
        capital = Capital.select().where(Capital.id == capital_id).first()
        if not capital:
            response = {'message': f'capital with id {capital_id} not found.'}
            return make_response(jsonify(response), 200)

        Capital.delete_by_id(capital_id)
        return make_response('', 204)
