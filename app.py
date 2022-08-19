import os
from flask import Flask
from flask_jwt_extended import JWTManager

from resources.config import api
from models.db import db

SETTINGS_FILE = "./settings.py"

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(SETTINGS_FILE)

    @app.before_first_request
    def create_db():
        db.create_all()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/data.db'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-ryanbs'
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)
    api.init_app(app)
    JWTManager(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
