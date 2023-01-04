from flask_restful import Api
from flask import current_app

from app.api.weather.countries.country import CountryName
from app.api.weather.countries.countries import Countries


# /api/v1/countries/
# /api/v1/countries/1
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(CountryName, '/api/v1/countries/<country_id>')
        api.add_resource(Countries, '/api/v1/countries/')