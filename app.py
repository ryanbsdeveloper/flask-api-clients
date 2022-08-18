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

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-ryanbs'
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)
    api.init_app(app)
    JWTManager(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
