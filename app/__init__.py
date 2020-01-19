from flask import Flask
# from flask_bootstrap import Bootstrap
# from flask_migrate import Migrate
from app import routes, models
# from app.db import db


# bootstrap = Bootstrap()
# migrate = Migrate()


def create_app(config):
    # create application with specified config
    app = Flask(__name__)
    app.config.from_object(config)

    # register extensions
    # bootstrap.init_app(app)
    # db.init_app(app)
    # migrate.init_app(app)

    # register routes
    routes.register(app)

    return app
