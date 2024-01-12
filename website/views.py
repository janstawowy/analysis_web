from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    if request.method == 'POST':
        hashtag = request.form.get('hashtag')
        if len(hashtag) < 3:
            flash('hashtag is too short!', category='error')
        else:
            pass

    return render_template('home.html', user=current_user)

