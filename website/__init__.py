from common import JsonReader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

secrets_file_path = "./keys/secrets.json"
keys_reader = JsonReader(secrets_file_path)
keys = keys_reader.read_json()

db = SQLAlchemy()
DB_NAME = 'database.db'
def create_app():


    app = Flask(__name__)
    app.config['SECRET_KEY'] = keys['flask_secret']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app