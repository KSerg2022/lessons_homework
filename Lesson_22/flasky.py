"""Main modul."""

from flask import Flask, render_template
from jinja2 import TemplateNotFound

from get_data import ALL_DATA, CITIES_NAME

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/index')
@app.route('/')
def index():
    """Return main page."""
    return render_template('index.html', cities=sorted(CITIES_NAME))


@app.route('/<city>')
def cities(city):
    """Return city's page"""
    if city not in CITIES_NAME:
        return render_template('404.html', cities=sorted(CITIES_NAME))

    else:
        try:
            return render_template('city.html', cities=sorted(CITIES_NAME), city=city.lower() + '.jpg',
                                   name=ALL_DATA[city]['name'], slogan=ALL_DATA[city]['slogan'])
        except TemplateNotFound:
            return render_template('404.html', cities=sorted(CITIES_NAME))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
