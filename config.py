import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(32)

    # Enable debug mode.
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/fyyur'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
