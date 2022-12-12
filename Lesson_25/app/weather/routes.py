"""Routes for app 'weather'."""
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from flask_paginate import Pagination

from app.weather import weather
from app.weather.forms import WeatherForm, AddCityForm, GenerateCapitalsForm
from app.weather.models import City
from app.weather.handlers.get_weather_for_cities import get_weather_for_cities
from app.weather.handlers.verify_country_name import main as verify_country_name
from app.handlers.get_qty_position_per_page import get_qty_position_per_page
from utils.weather.getting_weather import main as get_weather
from utils.weather.generate_data_capitels import main as generate_capitals


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


@weather.route('/add_city', methods=['POST', 'GET'])
def add_city():
    """Add city."""
    form = AddCityForm()

    if form.validate_on_submit():
        country = form.country.data
        city = form.city.data
        if not verify_country_name(country):
            flash(f'Country name "{country}" is not correct.')
            return redirect(url_for('weather.add_city'))

        weather_in_city = get_weather(city)
        if 'error' in weather_in_city:
            flash(f"{weather_in_city['error']} - ({city}).")
            return redirect(url_for('weather.add_city'))

        message = f'City "{city.capitalize()}" already registered'
        if not City.select().where(City.name == city.capitalize()):
            new_city = City(country=country.capitalize(), name=city.capitalize())
            new_city.save()
            message = f'City "{city.capitalize()}" just registered'

        flash(message)
        return redirect(url_for('weather.add_city'))

    return render_template(
        'weather/add_city.html',
        title='Add city',
        form=form
        )


@weather.route('/show_cities/<int:page>', methods=['GET'])
@weather.route('/show_cities')
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


@weather.route('/delete', methods=['POST', 'GET'])
def delete():
    """Delete city from database."""
    if request.method == 'POST':
        message = 'Deleted: '
        selectors = list(map(int, request.form.getlist('selectors')))

        if not selectors:
            flash('Nothing to delete')
            return redirect(url_for('weather.show_cities'))

        for selector in selectors:
            city = City.get(City.id == selector)
            message += f'{city.name} '
            city.delete_instance()

        page = int(request.form.get('page'))
        qty_per_page = get_qty_position_per_page()
        if int(len(City.select())) % qty_per_page == 0:
            page -= 1

        flash(message)
        return redirect(url_for('weather.show_cities', page=page))


@weather.route('/capitals', methods=['POST', 'GET'])
def capitals():
    """Generate list of capitals."""
    form = GenerateCapitalsForm()

    if form.validate_on_submit():
        if not City.select():
            data_capitals = generate_capitals()
            for country, capital in data_capitals:
                city = City(country=country, name=capital)
                city.save()
            flash('Database filled with capitals')
        else:
            flash('Database is not empty')

    return render_template(
        'weather/capitals.html',
        title='Generate capitals',
        form=form
        )
