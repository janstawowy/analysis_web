from common import JsonReader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

secrets_file_path = "./keys/secrets.json"
keys_reader = JsonReader(secrets_file_path)
keys = keys_reader.read_json()

db = SQLAlchemy()
DB_NAME = 'analysisdb.db'

def create_app():
    abs_instance_path = path.abspath(
        path.join(path.dirname(__file__), '..', 'instance'))  # <--- this will be the instance directory
    app = Flask(__name__, instance_path=abs_instance_path)
    app.config['SECRET_KEY'] = keys['flask_secret']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    from .models import User, Post
    db.init_app(app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')







    return app


def create_database(app):
    if not path.exists('instance/'+DB_NAME):
        from .models import User, Post
        with app.app_context():
            db.create_all()
        print('Setting up a database')