'''The application entry point.

This module is responsible for creating the application and database.
It also contains a function to generate the application shell context,
which is used for development purposes. For application initialization,
see the app module.
'''

import os
from app import create_app
from app.db import db
from app.models import ShortURL


app = create_app()
with app.app_context():
    db.create_all()


@app.shell_context_processor
def make_shell_context():
    '''Generate the application shell context.

    This is used for development purposes. See
    `the flask documentation <https://flask.palletsprojects.com/en/1.1.x/cli/#open-a-shell>`_ for details.
    '''
    return {
        'db': db,
        'ShortURL': ShortURL
    }
