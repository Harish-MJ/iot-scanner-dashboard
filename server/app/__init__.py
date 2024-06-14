from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from config import Config

# Instantiate extension objects
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")


# Function to create the Flask app, initialize extensions, and import routes and models
def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__, static_folder="../static", static_url_path="/")
    app.config.from_object(config_class)

    # Initialize extensions
    initialize_extensions(app)

    # Import models and routes
    import_models_and_routes(app)

    # Setup database
    setup_database(app)

    # Setup static routes
    setup_static_routes(app)

    return app


# Function to initialize extensions
def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    socketio.init_app(app)


# Function to import models and routes
def import_models_and_routes(app):
    with app.app_context():
        from . import routes
        from .models import LaserData


# Function to setup database
def setup_database(app):
    with app.app_context():
        db.create_all()


# Function to setup static routes
def setup_static_routes(app):
    @app.route("/")
    @app.route("/<path:path>")
    def serve_react_app(path=""):
        return send_from_directory(app.static_folder, "index.html")
