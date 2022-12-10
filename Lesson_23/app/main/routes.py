from flask import render_template, redirect, url_for, flash
from datetime import datetime

from app.main import main
from app.main.forms import NameForm, NameFormEdit
from app.main.models import User
from app.main.models import DoesNotExist


@main.route('/')
def index():
    """Home page"""
    return render_template(
        'index.html',
        title='Home page',
        current_time=datetime.utcnow()
    )


@main.route('/email', methods=['POST', 'GET'])
def add_email():
    """Add name and email form page"""
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = f'User with email "{email}" already registered'
        if not User.select().where(User.email == email):
            user = User(name=name, email=email)
            user.save()
            message = f'User with name "{name.capitalize()}" and email "{email}" just registered'

        flash(message)
        return redirect(url_for('main.add_email'))

    return render_template(
        'main/email.html',
        title='Register user',
        form=form
    )


@main.route('/all_user')
def all_user():
    """Show all registered users."""
    users = User.select()
    return render_template(
        '/main/all_user.html',
        title='All registered users',
        users=users
    )


@main.route('/delete/<user_id>', methods=['POST', 'GET'])
def delete(user_id):
    """Delete user from database."""
    user = User.get(User.id == user_id)
    user.delete_by_id(user_id)
    flash(f'User "{user.name.capitalize()}" with email "{user.email}" deleted.')
    return redirect(url_for('main.all_user'))


@main.route('/update/<user_id>')
def update(user_id):
    """Edit user's data."""
    form = NameFormEdit()
    try:
        user = User.get(User.id == user_id)
    except DoesNotExist:
        flash('User not find')
        return redirect(url_for('main.all_user'))

    else:
        return render_template(
            'main/update.html',
            title='Data update',
            form=form,
            user=user
        )


@main.route('/update/update_record/<user_id>', methods=['POST', 'GET'])
def update_record(user_id):
    """Update user's data."""
    form = NameFormEdit()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        user = User.get(User.id == user_id)

        if email == user.email and name == user.name:
            flash('Users name and email did not change.')
            return redirect(url_for('main.update', user_id=user_id))

        elif email == user.email:
            message = f'User\'s name "{user.name.capitalize()}" was changed to "{name.capitalize()}".'
            user.name = name
            user.save()
            flash(message)
            return redirect(url_for('main.all_user'))

        elif not User.select().where(User.email == email):
            user.name = name
            user.email = email
            user.save()
            flash("User's data was changed.")
            return redirect(url_for('main.all_user'))

        message = f'User with email "{email}" already exists.'
        flash(message)
        return redirect(url_for('main.update', user_id=user_id))
