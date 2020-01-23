'''This module contains all application initialization.'''

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from app.db import db
from app.api import bp as api_bp
from app.webapp import bp as webapp_bp


bootstrap = Bootstrap()
migrate = Migrate()


def create_app(config):
    """Create the application.

    This function is the application factory, which creates an instance of
    the application with the specified configuration class. This includes
    initializing all flask extensions and registering blueprints and routes.
    """

    # create application with specified config
    app = Flask(__name__)
    app.config.from_object(config)

    # register extensions
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(webapp_bp)

    return app
