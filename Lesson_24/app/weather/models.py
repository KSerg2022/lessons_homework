from peewee import *


database_proxy_city = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy_city


class City(BaseModel):
    country = CharField(max_length=100)
    name = CharField(max_length=150, unique=True, index=True)