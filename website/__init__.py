from common import JsonReader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Read the Flask application secret key and database URI from a JSON file
secrets_file_path = "./keys/secrets.json"
keys_reader = JsonReader(secrets_file_path)
keys = keys_reader.read_json()

# Initialize SQLAlchemy database and set the database name
db = SQLAlchemy()
DB_NAME = 'analysisdb.db'

def create_app():
    """
    Create and configure the Flask application.

    Returns:
    - Flask: The configured Flask application.
    """

    # Calculate the absolute path to the 'instance' directory
    abs_instance_path = path.abspath(
        path.join(path.dirname(__file__), '..', 'instance'))  # <--- this will be the instance directory

    # Create a Flask application instance with the given name and instance path
    app = Flask(__name__, instance_path=abs_instance_path)

    # Configure the Flask application with the secret key and database URI
    app.config['SECRET_KEY'] = keys['flask_secret']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Import models and initialize the database with the Flask application
    from .models import User, Dashboard, Post
    db.init_app(app)

    # Create the database if it does not exist using create_database function
    create_database(app)

    # Initialize and configure the Flask LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    # Register blueprints for views and authentication
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    """
        Create the database if it does not exist.

        Parameters:
        - app (Flask): The Flask application instance.
    """

    # Check if the database file does not exist in the app directory
    if not path.exists('instance/'+DB_NAME):

        # Create the database tables within the Flask application context
        with app.app_context():
            db.create_all()
        print('Setting up a database')