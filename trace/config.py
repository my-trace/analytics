import os, ConfigParser

config = ConfigParser.ConfigParser()
config.read('trace/config/base.cfg')

if os.environ['APP_SETTINGS'] == 'trace.config.Test':
    config.read('trace/config/test.cfg')


class DefaultConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config.get('db', 'DB_URL')
    APP_ID = os.environ['APP_ID']
    APP_SECRET = os.environ['APP_SECRET']
    APP_TOKEN = os.environ['APP_TOKEN']

class Test(DefaultConfig):
    ENV = 'test'
    ANDY_TOKEN = os.environ.get('ANDY_TOKEN')

class Development(DefaultConfig):
    ENV = 'development'
    DEBUG = True

class Production(DefaultConfig):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ['DB_URL']
    GP_API_KEY = os.environ.get('GP_API_KEY')

