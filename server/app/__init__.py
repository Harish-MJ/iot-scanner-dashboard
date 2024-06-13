from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__, static_folder='../static', static_url_path='/')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    socketio.init_app(app)
    
    # Import models and routes
    with app.app_context():
        from . import routes
        from .models import LaserData
        db.create_all()

    @app.route('/')
    @app.route('/<path:path>')
    def serve_react_app(path=''):
        return send_from_directory(app.static_folder, 'index.html')

    return app
