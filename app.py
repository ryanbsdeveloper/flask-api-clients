import os
from flask import Flask
from flask_jwt_extended import JWTManager

from resources import api
from models import db

SETTINGS_FILE = "./settings.py"

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(SETTINGS_FILE)

    @app.before_first_request
    def create_db():
        db.create_all()

    # if not os.getenv('SECRET'):
    #     raise EnvironmentError(
    #         'The secret key is required. Pls add to the environment in the variable "SECRET".'
    #     )

    # if not os.getenv('SQLALCHEMY_DATABASE_URI'):
    #     raise EnvironmentError(
    #         'The environment variable SQLALCHEMY_DATABASE_URI is required.'
    #     )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['JWT_SECRET_KEY'] = 'HS256'
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)
    api.init_app(app)
    JWTManager(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
