"""Routes for app 'weather'."""
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from flask_paginate import Pagination
from peewee import DoesNotExist, IntegrityError
from random import randint

from app.weather import weather
from app.weather.forms import WeatherForm, AddCityForm, GenerateCapitalsForm
from app.weather.models import Capital, City, Country
from app.weather.handlers.get_weather_for_cities import get_weather_for_cities
from app.handlers.get_qty_position_per_page import get_qty_position_per_page

from utils.weather.getting_weather import main as getting_weather
from utils.weather.getting_weather import main as get_weather
from utils.weather.generate_data.generate_cities import get_ua_cities
from utils.weather.generate_data.generate_data_capitels import main as generate_capitals


@weather.route('/')
def start():
    """Start page."""
    return render_template(
        'index.html',
        title='Start page',
        current_time=datetime.utcnow(),
    )


@weather.route('/weather', methods=['POST', 'GET'])
def index():
    """Weather page."""
    form = WeatherForm()

    if not form.city.data:
        return render_template(
            'weather/index.html',
            title='Home page',
            current_time=datetime.utcnow(),
            form=form
            )

    city = form.city.data
    weather_in_city = get_weather(city)
    if 'error' in weather_in_city:
        flash(f"{weather_in_city['error']} - ({city}).")
        return redirect(url_for('weather.index'))

    form.city.data = ''
    return render_template(
        'weather/index.html',
        title='Home page',
        current_time=datetime.utcnow(),
        form=form,
        weather=weather_in_city
        )


@weather.route('/add/city', methods=['POST', 'GET'])
def add_city():
    """Add city."""
    form = AddCityForm()

    if form.validate_on_submit():
        country = form.country.data
        city = form.city.data

        weather_in_city = get_weather(city)
        if 'error' in weather_in_city:
            flash(f"{weather_in_city['error']} - ({city}).")
            return redirect(url_for('weather.index'))

        message = f'City "{city.capitalize()}" already registered'
        if not City.select().where(City.name == city.capitalize()):
            country_id = Country.select().where(Country.code == country).first()
            new_city = City(country=country_id, name=city.capitalize())
            new_city.save()
            message = f'City "{city.capitalize()}" just registered'

        flash(message)
        return redirect(url_for('weather.index'))
    return redirect(url_for('weather.index'))


@weather.route('/show/cities/<int:page>', methods=['GET'])
@weather.route('/show/cities')
def show_cities(page=1):
    """Show all cities."""
    qty_per_page = get_qty_position_per_page()
    cities = City.select()
    pagination = Pagination(page=page, per_page=qty_per_page, total=cities.count(), record_name='cities')
    cities = list(get_weather_for_cities(cities.paginate(page, qty_per_page)))

    return render_template(
        'weather/show_cities.html',
        title='Show cities',
        cities=cities,
        pagination=pagination
        )


@weather.route('/delete/city', methods=['POST', 'GET'])
def delete_city():
    """Delete city from database."""
    if request.method == 'POST':
        message = 'Deleted: '
        selectors = list(map(int, request.form.getlist('selectors')))

        qty_per_page = get_qty_position_per_page()
        total_pages = int(len(City.select())) // qty_per_page
        if not selectors:
            flash('Nothing to delete')
            return redirect(url_for('weather.show_cities'))

        for selector in selectors:
            try:
                city = City.get(City.id == selector)
            except DoesNotExist:
                pass
            else:
                message += f'{city.name}, '
                city.delete_instance()

        current_page = int(request.form.get('page'))
        if int(len(City.select())) % qty_per_page == 0 and (current_page - total_pages == 1):
            current_page -= 1

        flash(message)
        return redirect(url_for('weather.show_cities', page=current_page))


@weather.route('/add/cities', methods=['POST', 'GET'])
def add_cities():
    """Generate list of capitals."""
    form = GenerateCapitalsForm()

    if form.validate_on_submit():
        if not City.select():
            data_cities = get_ua_cities()
            for country, cities in data_cities.items():
                country_id = Country.select().where(Country.code == country).first()

                qty_cities = 0
                while qty_cities < 25:
                    city = cities.pop(randint(1, len(cities) - 1))

                    weather_in_city = getting_weather(city, country)
                    if 'error' in weather_in_city:
                        pass
                    else:
                        city = City(country=country_id, name=city.capitalize())
                        try:
                            city.save()
                        except IntegrityError:
                            pass
                        qty_cities += 1

                flash('Database filled with cities')
        else:
            flash('Database is not empty')

    return redirect(url_for('weather.show_cities'))


@weather.route('/show/capitals/<int:page>', methods=['GET'])
@weather.route('/show/capitals')
def show_capitals(page=1):
    """Show all capitals."""
    qty_per_page = get_qty_position_per_page()
    capital_s = Capital.select()
    pagination = Pagination(page=page, per_page=qty_per_page, total=capital_s.count(), record_name='capitals')
    cities = list(get_weather_for_cities(capital_s.paginate(page, qty_per_page)))
    return render_template(
        'weather/show_capitals.html',
        title='Show capitals',
        cities=cities,
        pagination=pagination
        )


@weather.route('/delete/capitals', methods=['POST', 'GET'])
def delete_capitals():
    """Delete city from database."""
    if request.method == 'POST':
        message = 'Deleted: '
        selectors = list(map(int, request.form.getlist('selectors')))

        qty_per_page = get_qty_position_per_page()
        total_pages = int(len(Capital.select())) // qty_per_page
        if not selectors:
            flash('Nothing to delete')
            return redirect(url_for('weather.show_capitals'))

        for selector in selectors:
            try:
                city = Capital.get(Capital.id == selector)
            except DoesNotExist:
                pass
            else:
                message += f'{city.name}, '
                city.delete_instance()

        current_page = int(request.form.get('page'))
        if int(len(Capital.select())) % qty_per_page == 0 and (current_page - total_pages == 1):
            current_page -= 1

        flash(message)
        return redirect(url_for('weather.show_capitals', page=current_page))


@weather.route('/add/capitals', methods=['POST', 'GET'])
def add_capitals():
    """Generate list of capitals."""
    form = GenerateCapitalsForm()

    if form.validate_on_submit():
        if not Capital.select():
            data_capitals = generate_capitals()

            qty_cities = 0
            while qty_cities < 25:
                capital = data_capitals.pop(randint(1, len(data_capitals) - 1))
                weather_in_capital = getting_weather(capital['capital'])
                if 'error' in weather_in_capital:
                    pass
                else:
                    country_id = Country.select().where(Country.name == capital['country']).first()
                    city = Capital(country=country_id, name=capital['capital'])
                    try:
                        city.save()
                    except IntegrityError:
                        pass
                    qty_cities += 1
            flash('Database filled with capitals')

        else:
            flash('Database is not empty')

    return redirect(url_for('weather.show_capitals'))
