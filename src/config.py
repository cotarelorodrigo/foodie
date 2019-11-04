# /src/config.py
import os
import src.settings

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_LOCAL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER="foodie.taller2@gmail.com"
    MAIL_USERNAME="foodie.taller2@gmail.com"
    MAIL_PASSWORD="foodie123"

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_timeout":240}
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER="foodie.taller2@gmail.com"
    MAIL_USERNAME="foodie.taller2@gmail.com"
    MAIL_PASSWORD="foodie123"

class Testing(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_ENGINE_OPTIONS = {}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER="foodie.taller2@gmail.com"
    MAIL_USERNAME="foodie.taller2@gmail.com"
    MAIL_PASSWORD="foodie123"

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}