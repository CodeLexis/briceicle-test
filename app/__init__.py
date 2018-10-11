from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import get_configuration_class
from .logs import logger
from .errors.handlers import setup_error_handling


config_object = get_configuration_class()


db = SQLAlchemy()
mail = Mail()


def _setup_blueprints(app):
    from blueprints import web_blueprint

    app.register_blueprint(web_blueprint)


def create_app():
    app = Flask(__name__, template_folder='../static/templates',
                static_folder='../static')
    app.config.from_object(config_object)

    _setup_blueprints(app)
    # setup_error_handling(app)

    db.init_app(app)
    mail.init_app(app)

    return app
