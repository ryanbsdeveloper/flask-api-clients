import os
from datetime import timedelta
from flask import Flask, Response, json
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
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)
    api.init_app(app)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        return Response(
            response=json.dumps({
                "message": "JWT token expirado"
            }),
            status=401,
            mimetype='application/json'
        )

    @jwt.invalid_token_loader
    def my_invalid_token_callback(invalid_token):
        return Response(
            response=json.dumps({
                "message": "JWT token ínvalido"
            }),
            status=401,
            mimetype='application/json'
        )
    @jwt.unauthorized_loader
    def my_unauthorized_loader_token_callback(invalid_token):
        return Response(
            response=json.dumps({
                "message": "Este endpoint requer JWT token"
            }),
            status=401,
            mimetype='application/json'
        )
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
