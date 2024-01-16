from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

post_dashboard_association = db.Table(
    'post_dashboard_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id'))
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    dashboards = db.relationship('Dashboard', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    hashtag = db.Column(db.String(150))
    raw_text = db.Column(db.String(1000))
    text = db.Column(db.String(1000))
    sentiment = db.Column(db.String(150))
    sentiment_transformer = db.Column(db.String(20))
    transformer_score = db.Column(db.Integer)
    sentiment_results_adjusted = db.Column(db.String(50))

class Dashboard(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post', secondary=post_dashboard_association, backref='dashboards', lazy=True)



