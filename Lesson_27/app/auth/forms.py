from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.auth.models import UserAuth


class LoginForm(FlaskForm):
    next = HiddenField()
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(2, 100),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, numbers, dots or '
                   'underscores')])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(), Length(8,),
            EqualTo('password_repeat', message='Passwords must match.')
        ])
    password_repeat = PasswordField(
        'Confirm password',
        validators=[DataRequired(), Length(8,)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if UserAuth.select().where(UserAuth.email == field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if UserAuth.select().where(UserAuth.name == field.data).first():
            raise ValidationError('Username already in use.')
