import logging
from logging import Formatter, FileHandler
import os
import dateutil.parser
import babel


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from config import Config

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # register error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # register main app
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)



    # define filter and register
    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format="EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format="EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

    # logging if debug is false
    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')


    return app

#from app import models









