from flask_restful import Resource
from flask import make_response, jsonify, request


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
        self.data_capitals = None

    def get(self):
        """HTTP method GET"""
        self.capitals = Capital.select()
        self.capitals = self.prepare_capitals_to_json()
        return make_response(jsonify(self.capitals), 200)

    def post(self):
        """HTTP method POST.
        [
        {"name": "lviv"}
        ]
        """
        self.data_capitals = request.get_json()
        if not self.data_capitals:
            response = {'message': "you didn't send anything"}
            return make_response(jsonify(response), 200)

        not_capital = []
        weather_error = []
        check_capitals = []
        for capital in self.data_capitals:
            capital_name = capital.get("name").capitalize()

            if not verify_name_capital(capital_name):
                response = {'message': f'city name {capital_name} is not capital'}
                not_capital.append(response)
                continue

            capital_weather = getting_weather(capital_name, self.api_key)
            if 'error' in capital_weather:
                response = {'message': f'Capital {capital_name} is {capital_weather}'}
                weather_error.append(response)
                continue

            country = Country.select().where(Country.code == capital_weather['country_code']).first()
            check_capital = Capital.select().where(Capital.name == capital_name).first()
            if check_capital:
                response = {'message': f'{capital_name} already in database.'}
                check_capitals.append(response)
                continue

            capital = Capital(
                name=capital_name,
                country=country.id
            )
            capital.save()

        if not_capital or weather_error or check_capitals:
            return make_response(jsonify(not_capital, weather_error, check_capitals), 200)

        return make_response('', 201)

    def put(self):
        """HTTP method PUT.
        [
        {"id": 3, "name": "lviv"}
        ]
        """
        self.data_capitals = request.get_json()
        if not self.data_capitals:
            response = {'message': "you didn't send anything"}
            return make_response(jsonify(response), 200)

        not_id = []
        not_capital = []
        capital_not_found = []
        weather_error = []
        check_capitals = []

        for capital in self.data_capitals:
            capital_name = capital.get('name').capitalize()
            capital_id = capital.get('id')

            if not capital_id:
                response = {'message': f'city name {capital_name} have not "id"!'}
                not_id.append(response)
                continue

            if not verify_name_capital(capital_name):
                response = {'message': f'city name {capital_name} is not capital'}
                not_capital.append(response)
                continue

            capital = Capital.select().where(Capital.id == capital.get("id")).first()
            if not capital:
                response = {'message': f'capital with id {capital_id} not found in db.'}
                capital_not_found.append(response)
                continue

            capital_weather = getting_weather(capital_name, self.api_key)
            if 'error' in capital_weather:
                response = {'message': f'Capital {capital_name} is {capital_weather}'}
                weather_error.append(response)
                continue

            country = Country.select().where(Country.code == capital_weather['country_code']).first()
            check_city = Capital.select().where(Capital.name == capital_name).first()
            if check_city:
                response = {'message': f'{capital_name} already in database.'}
                check_capitals.append(response)
                continue

            capital.name = capital_name
            capital.country = country
            capital.save()

        if not_id or not_capital or capital_not_found or weather_error or check_capitals:
            return make_response(jsonify(not_id, not_capital, capital_not_found, weather_error, check_capitals), 200)

        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE. Delete all capitals."""
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
