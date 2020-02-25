import os

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

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

#from app import models









