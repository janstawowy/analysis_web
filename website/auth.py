from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import User

# Create a Flask Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    """
        Handle user login.

        If a valid login attempt is made, log in the user and redirect to the home page.

        Returns:
        - render_template: Render the login template with current user information.
        - redirect: Redirect to the home page if login is successful.
    """
    if request.method == 'POST':

        # Get data from login form
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()

        # If user exists in the database try to authenticate him
        if user:
            # Check if the provided password matches the hashed password in the database
            if check_password_hash(user.password,password):
                flash('Logged in successfully')
                login_user(user,remember=True)

                # redirect user to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect user or password, try again', category='error')
        else:
            flash("User not found", category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    """
    Handle user logout.

    Log out the currently logged-in user and redirect to the login page.

    Returns:
    - redirect: Redirect to the login page after logging out.
    """
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    """
        Handle user sign-up.

        If a valid sign-up attempt is made, create a new user account, log in the user, and redirect to the home page.

        Returns:
        - render_template: Render the sign-up template with current user information.
        - redirect: Redirect to the home page if sign-up is successful.
    """
    # Get data from signup form
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()

        # Perform data validation
        if user:
            flash('User already exists', category='error')
        elif len(email)<4:
            flash('Email too short', category='error')
        elif len(name)<3:
            flash('Name must be longer than 2 characters', category='error')
        elif len(password1) <6:
            flash('Password must be at least 6 characters long', category='error')
        elif password1 != password2:
            flash('Passwords dont match', category='error')
        else:
            # Create a new user and add it to the database
            new_user = User(email=email,password=generate_password_hash(password1, method='pbkdf2:sha256'),first_name=name)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')

            # Log in the new user and redirect to the home page
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('sign-up.html',user=current_user)