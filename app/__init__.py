from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .utils import fetch_valid_countries


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configuration from the global config.py
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "../config.py"))

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    fetch_valid_countries()

    # Register Blueprints
    from .routes import routes
    app.register_blueprint(routes)

    return app
