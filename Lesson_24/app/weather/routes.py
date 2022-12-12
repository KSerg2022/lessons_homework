from flask import render_template, redirect, url_for, flash
from datetime import datetime

from app.weather import weather
from app.weather.forms import WeatherForm, AddCityForm
from utils.weather.getting_weather import main as getting_weather
from app.weather.models import City
from app.weather.handlers.get_weather_for_cities import get_weather_for_cities


@weather.route('/')
def start():
    """Start page"""
    return render_template(
        'index.html',
        title='Start page',
        current_time=datetime.utcnow(),
    )


@weather.route('/weather', methods=['POST', 'GET'])
def index():
    """Weather page"""
    form = WeatherForm()

    if not form.city.data:
        return render_template(
            'weather/index.html',
            title='Home page',
            current_time=datetime.utcnow(),
            form=form,
            img=False
            )

    city = form.city.data
    temp = getting_weather(city)
    if temp == 'not':
        flash(f'City "{city}" not found.')
        return redirect(url_for('weather.index'))

    flash(f'In city "{city.capitalize()}" is {temp} today.')
    form.city.data = ''
    return render_template(
        'weather/index.html',
        title='Home page',
        current_time=datetime.utcnow(),
        form=form,
        img=temp
        )


@weather.route('/add_city', methods=['POST', 'GET'])
def add_city():
    """Add city."""
    form = AddCityForm()

    if form.validate_on_submit():
        country = form.country.data
        city = form.name.data

        if getting_weather(city) == 'not':
            flash(f'City "{city}" not found.')
            return redirect(url_for('weather.add_city'))

        message = f'City "{city.capitalize()}" already registered'
        if not City.select().where(City.name == city):
            new_city = City.create(country=country, name=city)
            new_city.save()
            message = f'City "{city.capitalize()}" just registered'

        flash(message)
        return redirect(url_for('weather.add_city'))

    return render_template(
        'weather/add_city.html',
        title='Add city',
        form=form
        )


@weather.route('/show_cities')
def show_cities():
    """Show all cities."""
    cities = get_weather_for_cities(City.select())
    if not cities:
        flash('List of cities is empty')
        return redirect(url_for('weather.add_city'))
    return render_template(
        'weather/show_cities.html',
        title='Show cities',
        cities=cities
        )


@weather.route('/delete/<city_id>', methods=['POST', 'GET'])
def delete(city_id):
    """Delete city from database."""
    city = City.get(City.id == city_id)
    city.delete_instance()
    flash(f'City "{city.name.capitalize()}" deleted.')
    return redirect(url_for('weather.show_cities'))
