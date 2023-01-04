from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request

from app.weather.models import Country
from app.handlers.get_apy_id_weather import get_apy_id
from app.api.weather.utils import verify_name_country, get_country_code

# /api/v1/countries/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class Countries(Resource):
    """API for cities /api/v1/countries"""
    def __init__(self):
        self.countries = None
        self.request = None
        self.api_key = get_apy_id()
        self.data_countries = None

    def get(self):
        """HTTP method GET"""
        self.countries = Country.select()
        self.countries = self.prepare_countries_to_json()
        return make_response(jsonify(self.countries), 200)

    def post(self):
        """HTTP method POST."""
        response = {'message': f'method "POST" is disable.'}
        return make_response(jsonify(response), 200)

    def put(self):
        """HTTP method PUT. {"id": 3, "name": "lviv"}."""
        self.data_countries = request.get_json()
        if not self.data_countries:
            response = {'message': "you didn't send anything"}
            return make_response(jsonify(response), 200)

        not_id = []
        not_country = []
        country_not_found = []
        check_countries = []
        for country in self.data_countries:
            country_name = country.get('name').capitalize()
            country_id = country.get('id')

            if not country_id:
                response = {'message': f'City name {country_name} have not "id"!'}
                not_id.append(response)
                continue

            if not verify_name_country(country_name):
                response = {'message': f'Country name {country_name} is not exist'}
                not_country.append(response)
                continue

            country = Country.select().where(Country.id == country_id).first()
            if not country:
                response = {'message': f'country with id {country_id} not found.'}
                country_not_found.append(response)
                continue

            check_country = Country.select().where(Country.name == country_name).first()
            if check_country:
                response = {'message': f'{country_name} already in database.'}
                check_countries.append(response)
                continue

            country.name = country_name
            country.code = get_country_code(country_name)
            country.save()

        if not_id or not_country or country_not_found or check_countries:
            return make_response(jsonify(not_id, not_country, country_not_found, check_countries), 200)

        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE. Delete all data."""
        countries = Country.select()
        not_delete_countries = []
        for country in countries:
            try:
                country.delete().execute()
            except Exception:
                not_delete_countries.append(country)
        if not not_delete_countries:
            return make_response('', 204)
        response = {'message': 'Countries can not delete.'}
        return make_response(jsonify(not_delete_countries), jsonify(response), 200)

    def prepare_countries_to_json(self):
        """Prepare cities for json format"""
        countries = []
        for country in self.countries:
            country_temp = {
                'id': country.id,
                'name': country.name,
                'code': country.code,
            }
            countries.append(country_temp)
        return countries
