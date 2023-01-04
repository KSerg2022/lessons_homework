from peewee import *
from app.base_model import BaseModel


class Country(BaseModel):
    code = CharField(max_length=2, unique=True, index=True)
    name = CharField(max_length=100, unique=True, index=True)


class Capital(BaseModel):
    name = CharField(max_length=150, unique=True, index=True)
    country = ForeignKeyField(Country, backref='capital')


class City(BaseModel):
    name = CharField(max_length=100, unique=True, index=True)
    country = ForeignKeyField(Country, backref='city')
