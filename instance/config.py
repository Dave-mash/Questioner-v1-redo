"""
This module sets up all the necessary configurations for the app
"""

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class Development(Config):
    """Configurations for Development."""
    DEBUG = True
    TESTING = True


class Testing(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


class Production(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}