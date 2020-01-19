import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ''' Provides defaults for all configuration options. As such, also acts as
    an exhaustive list of all options. '''
    pass


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
