"""Routes for app 'main'."""
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime

from flask_login import current_user
from flask_paginate import Pagination
from peewee import DoesNotExist


from app.main import main
from app.main.forms import NameForm, GenerateDataForm
from app.main.models import User
from app.handlers.get_qty_position_per_page import get_qty_position_per_page
from utils.generate_data.main import main as generate_data
from utils.generate_data.data import emails_data


@main.route('/')
def start():
    """Start page."""
    try:
        name = current_user.name
    except AttributeError:
        name = None
    return render_template(
        'index.html',
        title='Start page',
        current_time=datetime.utcnow(),
        name=name,
    )


@main.route('/home', methods=['POST', 'GET'])
def index():
    """Home page"""
    form = GenerateDataForm()

    if form.validate_on_submit():
        if not User.select():
            emails = generate_data(emails_data)
            for name, email in emails:
                user = User(name=name, email=email)
                user.save()
            flash('Database filled with test data')
        else:
            flash('Database is not empty')

    return render_template(
        'main/index.html',
        title='Home page',
        current_time=datetime.utcnow(),
        form=form
    )


@main.route('/add/email', methods=['POST', 'GET'])
def add_email():
    """Add name and email form page"""
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = f'User with name {name} already registered'
        if not User.select().where(User.email == email):
            user = User(name=name, email=email)
            user.save()
            message = f'User with name {name} just registered'

        flash(message)
        return redirect(url_for('main.add_email'))

    return render_template(
        'main/email.html',
        title='Register user',
        form=form
    )


@main.route('/show/emails/<int:page>', methods=['GET', 'POSR'])
@main.route('/show/emails')
def show_emails(page=1):
    """Show user information"""
    qty_per_page = get_qty_position_per_page()
    users = User.select()
    pagination = Pagination(page=page, per_page=qty_per_page, total=users.count(), record_name='users')
    users = users.paginate(page, qty_per_page)
    return render_template(
        'main/show_emails.html',
        title='Show users',
        users=users,
        pagination=pagination
        )


@main.route('/delete/emails', methods=['POST'])
def delete_emails():
    """Delete selected users"""
    if request.method == 'POST':
        message = 'Deleted: '
        selectors = list(map(int, request.form.getlist('selectors')))

        if not selectors:
            flash('Nothing to delete')
            return redirect(url_for('main.show_emails'))

        for selector in selectors:
            user = User.get(User.id == selector)
            message += f'{user.email} '
            user.delete_instance()

        page = int(request.form.get('page'))
        qty_per_page = get_qty_position_per_page()
        if int(len(User.select())) % qty_per_page == 0:
            page -= 1

        flash(message)
        return redirect(url_for('main.show_emails', page=page))


@main.route('/update/<user_id>')
def update(user_id):
    """Edit user's data."""
    form = NameForm()
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        flash(f'User with id: {user_id} not found. You can add user in this form.')
        return redirect(url_for('main.add_email'))

    else:
        form.name.label.text = 'Edit this name'
        form.email.label.text = 'Edit this email'
        form.submit.label.text = 'Edit'
        return render_template(
            'main/update.html',
            title='Data update',
            form=form,
            user=user
        )


@main.route('/update/edit/<user_id>', methods=['POST', 'GET'])
def edit(user_id):
    """Update user's data."""
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        user = User.get(User.id == user_id)

        if email == user.email and name == user.name:
            flash('Users name and email did not change.')
            return redirect(url_for('main.update', user_id=user_id))

        elif email == user.email:
            message = f'User\'s name "{user.name.capitalize()}" for user with id: {user.id}' \
                      f' was changed to "{name.capitalize()}".'
            user.name = name
            user.save()
            flash(message)
            return redirect(url_for('main.show_emails'))

        elif not User.select().where(User.email == email):
            user.name = name
            user.email = email
            user.save()
            flash(f"Data for user with id: {user.id} was changed.")
            return redirect(url_for('main.show_emails'))

        message = f'User with email "{email}" already exists.'
        flash(message)
        return redirect(url_for('main.update', user_id=user_id))
