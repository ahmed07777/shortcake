'''The application configuration.

There are three configurations provided, for testing, development, and
production, respectively. All configurations inherit from a base configuration,
which tries to provide reasonable defaults.
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''The base configuration class. Attempts to provide reasonable defaults,
    which can be overriden by the more specialized configuration classes.
    '''

    # general options
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    '''Used to secure the form field in the web interface. See
       `the flask docs <https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY>`_ for more details.
    '''
    DOMAIN_NAME = os.environ.get('DOMAIN_NAME') or 'localhost:5000'
    '''Tells the application what domain it is running on, so it can return
       fully-qualified short URLs.
    '''

    # database options
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    '''A specialized configuration for automated unit tests.'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    '''The configuration for the development server.'''
    pass


class ProductionConfig(Config):
    '''The production configuration.'''
    # in actual fact several options are overridden in this configuration,
    # but they are done so via environment variables
    pass
