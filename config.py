import os

from app.constants import APP_NAME


class DevelopmentConfig(object):
    DEBUG = True

    SECRET_KEY = b'SUPER_SECRET'
    SERVER_NAME = 'localhost:5008'

    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://tomisin:tomisin10@localhost/{}'.format(
            APP_NAME.lower())
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(object):

    SECRET_KEY = b'SUPER_SECRET'
    SQLALCHEMY_DATABASE_URI = (
        'postgres://pqvstpivxijtyd:c04893d87de8ebb015d532e01f2206466dd84b81be56'
        '7cc528a1965e4709f2e8@ec2-174-129-35-61.compute-1.amazonaws.com:5432/d1'
        'n449g3p8f1ka')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_objects = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


def get_configuration_class():
    return config_objects[os.environ['RUNNING_MODE']]
