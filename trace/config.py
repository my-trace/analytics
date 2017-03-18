import os

class Config(object):
    DEBUG = False
    DB_URL = os.environ['DEV_DB_URL'] if os.environ.get('prod') else os.environ['DEV_DB_URL']
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_DB_URL']
    APP_ID = os.environ['APP_ID']
    APP_SECRET = os.environ['APP_SECRET']
    APP_TOKEN = os.environ['APP_TOKEN']

class Test(Config):
    ENV = 'test'
    ANDY_TOKEN = os.environ.get('ANDY_TOKEN')

class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
