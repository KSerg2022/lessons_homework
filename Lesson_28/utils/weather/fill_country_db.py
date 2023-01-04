from peewee import SqliteDatabase
from typing import List, Dict


from app.base_model import database_proxy
from app.weather.models import Country
from app.handlers.get_path_to_db import get_path_to_db
from utils.weather.country_codes import read_codes_data_from_json, get_path_to_file_countries_codes


def convert_data_from_json_to_db(countries: List[Dict[str, str]], path_to_db: str):
    """Convert data from json file to db"""
    db = SqliteDatabase(path_to_db)
    database_proxy.initialize(db)
    db.create_tables([Country])
    Country.delete().execute()

    for country in countries:
        country_instance = Country(
            code=country['code'],
            name=country['name']
        )
        country_instance.save()


def check_db_country_is_not_empty():
    """"""
    countries = Country.select().first()
    if countries:
        return True
    return False


def main():
    """Main controller"""
    if not check_db_country_is_not_empty():
        filename = get_path_to_file_countries_codes()
        path_to_db = get_path_to_db()
        countries = read_codes_data_from_json(filename)
        convert_data_from_json_to_db(countries, path_to_db)
        return True
    return True
