from flask_restful import Resource, reqparse
from flask import make_response, jsonify

from app.weather.models import Country
from app.handlers.get_apy_id_weather import get_apy_id
from app.api.weather.utils import verify_name_country, get_country_code

# /api/v1/countries/1
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class CountryName(Resource):
    """API for cities /api/v1/countries"""
    def __init__(self):
        self.country = None
        self.request = None
        self.api_key = get_apy_id()
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self, country_id=None):
        """HTTP method GET"""
        city = Country.select().where(Country.id == country_id).first()
        if not city:
            response = {'message': f'city with id {country_id} not found.'}
            return make_response(jsonify(response), 200)

        self.country = Country.select().where(Country.id == country_id).dicts().get()
        return make_response(jsonify(self.country), 200)

    def post(self, country_id=None):
        """HTTP method POST."""
        response = {'message': f'method "POST" is disable.'}
        return make_response(jsonify(response), 200)

    def put(self, country_id=None):
        """HTTP method PUT.
        {"name": "lviv"}
        """
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()

        if not verify_name_country(self.request.name):
            response = {'message': f'country name {self.request.name} is not exist'}
            return make_response(jsonify(response), 200)

        country = Country.select().where(Country.id == country_id).first()
        if not country:
            response = {'message': f'country with id {country_id} not found.'}
            return make_response(jsonify(response), 200)

        country_check = Country.select().where(Country.name == self.request.name).first()
        if country_check:
            response = {'message': f'{self.request.name} already in database.'}
            return make_response(jsonify(response), 200)

        country.name = self.request.name
        country.code = get_country_code(self.request.name)
        country.save()
        return make_response('', 204)

    def delete(self, country_id=None):
        """HTTP method DELETE.  Delete country with id=capital_id."""
        city = Country.select().where(Country.id == country_id).first()
        if not city:
            response = {'message': f'city with id {country_id} not found.'}
            return make_response(jsonify(response), 200)

        Country.delete_by_id(country_id)
        return make_response('', 204)
