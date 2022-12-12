from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class WeatherForm(FlaskForm):
    city = StringField(
        'Write city name.',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={'placeholder': 'City name'}
    )

    submit = SubmitField('Get weather')


class AddCityForm(FlaskForm):
    country = StringField(
        'Write country name.',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={'placeholder': 'Country name'}
    )
    name = StringField(
        'Write city name.',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={'placeholder': 'City name'}
    )

    submit = SubmitField('Add city')
