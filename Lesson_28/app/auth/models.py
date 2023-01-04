from peewee import CharField, ForeignKeyField
from app.base_model import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(BaseModel):
    name = CharField(max_length=100, unique=True, index=True)


class UserAuth(UserMixin, BaseModel):
    name = CharField(max_length=100)
    email = CharField(max_length=150, unique=True, index=True)
    password_hash = CharField(max_length=150)
    role = ForeignKeyField(Role, backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

