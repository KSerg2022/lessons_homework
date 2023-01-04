"""Routes for app 'weather'."""
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime

from flask_login import login_required
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
from utils.weather.getting_forecast_5d import main as getting_forecast_5d
from utils.weather.generate_data.generate_cities import get_ua_cities, get_cities_for_5_country
from utils.weather.generate_data.generate_data_capitels import main as generate_capitals


@weather.route('/home', methods=['POST', 'GET'])
@login_required
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
@login_required
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
@login_required
def show_cities(page=1):
    """Show all cities."""
    qty_per_page = get_qty_position_per_page()
    cities = City.select()
    country_name = request.args.get('country_name')
    if country_name:
        country = Country.select().where(Country.name == country_name).first()
        if country:
            cities = country.city
            page = 1
    pagination = Pagination(page=page, per_page=qty_per_page, total=cities.count(), record_name='cities')
    cities = list(get_weather_for_cities(cities.paginate(page, qty_per_page)))

    return render_template(
        'weather/show_cities.html',
        title='Show cities',
        cities=cities,
        pagination=pagination
        )


@weather.route('/delete/city', methods=['POST', 'GET'])
@login_required
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
@login_required
def add_cities():
    """Generate list of capitals."""
    form = GenerateCapitalsForm()

    if form.validate_on_submit():
        if not City.select():
            data_cities = get_cities_for_5_country()
            for city in data_cities:
                country_id = Country.select().where(Country.code == city['country']).first()

                weather_in_city = getting_weather(city['city_name'], city['country'])
                if 'error' in weather_in_city:
                    pass
                else:
                    city = City(country=country_id, name=city['city_name'].capitalize())
                    try:
                        city.save()
                    except IntegrityError:
                        pass

            flash('Database filled with cities')
        else:
            flash('Database is not empty')

    return redirect(url_for('weather.show_cities'))


@weather.route('/show/capitals/<int:page>', methods=['GET'])
@weather.route('/show/capitals')
@login_required
def show_capitals(page=1):
    """Show all capitals."""
    qty_per_page = get_qty_position_per_page()
    capitals = Capital.select()

    country_name = request.args.get('country_name')
    if country_name:
        country = Country.select().where(Country.name == country_name).first()
        if country:
            capitals = country.capital
            page = 1
    pagination = Pagination(page=page, per_page=qty_per_page, total=capitals.count(), record_name='capitals')
    cities = list(get_weather_for_cities(capitals.paginate(page, qty_per_page)))
    return render_template(
        'weather/show_capitals.html',
        title='Show capitals',
        cities=cities,
        pagination=pagination
        )


@weather.route('/delete/capitals', methods=['POST', 'GET'])
@login_required
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
@login_required
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


@weather.route('/show/forecast/5days/<string:city_name>, <string:country_code>')
@login_required
def show_forecast_5days(city_name, country_code):
    """Show weather forecast for five days for the city."""
    forecast_5d = getting_forecast_5d(city_name, country_code=country_code)
    if 'error' in forecast_5d:
        flash(f"{forecast_5d['error']} - ({city_name.capitalize()}).")
        return redirect(url_for('weather.index'))

    country_name = forecast_5d['country_name']
    forecast = forecast_5d['forecast']
    return render_template(
        'weather/show_forecast_5days.html',
        title='Show forecast for 5 days',
        city_name=city_name,
        country_name=country_name,
        forecast=forecast,
    )
