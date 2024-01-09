from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    raw_text = db.Column(db.String(1000))
    clean_text = db.Column(db.String(1000))
    sentiment = db.Column(db.String(150))


