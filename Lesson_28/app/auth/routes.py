"""User Registration and Authentication."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import auth
from app.auth.models import UserAuth
from app.auth.forms import LoginForm, RegisterForm


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """Website authentication."""
    form = LoginForm()

    form.next.label.text = ''
    if request.method == 'GET':
        next = request.args.get('next')
        form.next.data = next

    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('main.start'))

    if form.validate_on_submit():

        user = UserAuth.select().where(UserAuth.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = form.next.data
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    """Registration on the site."""
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserAuth.select().where(UserAuth.email == form.email.data).first()
        if user:
            flash(f'User with email: "{form.email.data}" already exists.')
            return redirect(url_for('auth.signup'))

        new_user = UserAuth(name=form.username.data.capitalize(),
                            email=form.email.data,
                            password=form.password.data,
                            role=1)
        new_user.save()
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('main.start'))
