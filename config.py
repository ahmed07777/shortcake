import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ''' Provides defaults for all configuration options. As such, also acts as
    an exhaustive list of all options. '''

    # general options
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    DOMAIN_NAME = os.environ.get('DOMAIN_NAME') or 'localhost:5000'

    # database options
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
