from flask_restful import Api
from flask import current_app

from app.api.weather.cities.city import CityName
from app.api.weather.cities.cities import Cities

# /api/v1/cities/
# /api/v1/cities/<city_id>/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(CityName, f'/api/v1/cities/<city_id>')
        api.add_resource(Cities, '/api/v1/cities/')
