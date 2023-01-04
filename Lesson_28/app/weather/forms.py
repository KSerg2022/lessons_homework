from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class GenerateCapitalsForm(FlaskForm):
    submit = SubmitField('Generate')


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
        validators=[Optional(), Length(2, 100)],
        render_kw={'placeholder': 'Country name'},
    )
    city = StringField(
        'Write city name.',
        validators=[DataRequired(), Length(2, 100)],
        render_kw={'placeholder': 'City name'}
    )

    submit = SubmitField('Add city')
