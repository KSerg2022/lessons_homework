""""""
from flask_restful import Api, Resource, reqparse
from flask import make_response, jsonify
from flask import current_app

from app.auth.models import UserAuth
from app.handlers.get_apy_id_weather import get_apy_id


# /api/v1/users/
# GET = all_cities 200
# POST = add city 201
# PUT = update_cities 204
# DELETE = delete_all_cities 204


class Users(Resource):
    """API for cities"""

    def __init__(self):
        self.users = None
        self.request = None
        self.api_key = get_apy_id()
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('email', type=str, required=True, location='json')
        self.regparse.add_argument('password', type=str, required=True, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self):
        """HTTP method GET"""
        self.users = UserAuth.select()
        self.users = self.prepare_users_to_json()
        return make_response(jsonify(self.users), 200)

    def post(self):
        """HTTP method POST.
        {"email": "lusy2@gmail.com", "name": "lusyy", "password": "1qa2ws3ed"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        self.request.email = self.request.email
        self.request.password = self.request.password
        self.request.id = self.request.id

        user_check_name = UserAuth.select().where(UserAuth.name == self.request.name).first()
        if user_check_name:
            response = {'message': f'User {self.request.name} already in database.'}
            return make_response(jsonify(response), 200)
        user_check_email = UserAuth.select().where(UserAuth.email == self.request.email).first()
        if user_check_email:
            response = {'message': f'User with email - {self.request.email} already in database.'}
            return make_response(jsonify(response), 200)

        new_user = UserAuth(name=self.request.name,
                            email=self.request.email,
                            password=self.request.password,
                            role=1)
        new_user.save()
        return make_response('', 201)

    def put(self):
        """HTTP method PUT.
        {"id": 3, "email": "lusy2@gmail.com", "name": "lusyy"}."""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        self.request.email = self.request.email
        self.request.password = self.request.password
        self.request.id = self.request.id

        if not self.request.id:
            response = {'message': 'field id is necessary.'}
            return make_response(jsonify(response), 200)

        user_check_name = UserAuth.select().where(UserAuth.name == self.request.name).first()
        if user_check_name:
            response = {'message': f'User {self.request.name} already in database.'}
            return make_response(jsonify(response), 200)
        user_check_email = UserAuth.select().where(UserAuth.email == self.request.email).first()
        if user_check_email:
            response = {'message': f'User with email - {self.request.email} already in database.'}
            return make_response(jsonify(response), 200)

        user = UserAuth.select().where(UserAuth.id == self.request.id).first()
        if not user.verify_password(self.request.password):
            response = {'message': f'User password is not correct'}
            return make_response(jsonify(response), 200)

        user.name = self.request.name
        user.email = self.request.email
        user.save()
        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE. Delete all data"""
        UserAuth.delete().execute()
        return make_response('', 204)

    def prepare_users_to_json(self):
        """Prepare cities for json format"""
        users = []
        for user in self.users:
            user_temp = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role.name
            }
            users.append(user_temp)
        return users


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(Users, '/api/v1/users/')
