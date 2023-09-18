from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required, current_user

from .models import User
from .forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

from . import database


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():

        # Is user already in the database?
        result = database.session.execute(database.select(User).where(User.email == registration_form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            registration_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=registration_form.email.data,
            name=registration_form.name.data,
            password=hash_and_salted_password,
        )
        database.session.add(new_user)
        database.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=registration_form, current_user=current_user)


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        password = login_form.password.data
        result = database.session.execute(database.select(User).where(User.email == login_form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=login_form, current_user=current_user)


# logout user
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))
