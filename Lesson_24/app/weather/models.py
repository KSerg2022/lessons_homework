from peewee import *

from app.main.models import BaseModel


class City(BaseModel):
    country = CharField(max_length=100)
    name = CharField(max_length=150, unique=True, index=True)