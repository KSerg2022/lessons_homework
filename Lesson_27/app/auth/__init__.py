"""https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-ru"""
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from app.auth import routes
