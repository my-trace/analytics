import os

def get(key):
    try:
        from flask import current_app
        return current_app.config.get(key)
    except RuntimeError:
        return getattr(Test, key)

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_DB_URL']
    APP_ID = os.environ['APP_ID']
    APP_SECRET = os.environ['APP_SECRET']
    APP_TOKEN = os.environ['APP_TOKEN']

class Test(Config):
    ENV = 'test'
    ANDY_TOKEN = os.environ.get('ANDY_TOKEN')
    GP_API_KEY = 'TEST_GP_API_KEY'

class Development(Config):
    ENV = 'development'
    DEBUG = True

class Production(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ['PROD_DB_URL']
    GP_API_KEY = os.environ['GP_API_KEY']

