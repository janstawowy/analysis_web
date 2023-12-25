from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email)<4:
            flash('Email too short', category='error')
        elif len(name)<3:
            flash('Name must be longer than 2 characters', category='error')
        elif len(password1) <6:
            flash('Password must be at least 6 characters long', category='error')
        elif password1 != password2:
            flash('Passwords dont match', category='error')
        else:
            flash('Account created', category='success')


    return render_template('sign-up.html')