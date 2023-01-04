from flask_restful import Api
from flask import current_app

from app.api.weather.capitals.capital import CapitalName
from app.api.weather.capitals.capitals import Capitals

# /api/v1/capitals/
# /api/v1/capitals/<city_id>/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(CapitalName, f'/api/v1/capitals/<capital_id>')
        api.add_resource(Capitals, f'/api/v1/capitals/')
