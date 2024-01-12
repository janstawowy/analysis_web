from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect user or password, try again', category='error')
        else:
            flash("User not found", category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()


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
            new_user = User(email=email,password=generate_password_hash(password1, method='pbkdf2:sha256'),first_name=name)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')

            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('sign-up.html',user=current_user)