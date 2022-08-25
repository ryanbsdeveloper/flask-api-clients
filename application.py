"""
 copyrigth © ryanbsdeveloper
 2022 - brazil
"""

from werkzeug.routing import *
from werkzeug.security import *

from flask import Flask, Response, json
from flask_jwt_extended import JWTManager

from models.db import db
from resources.config import api

SETTINGS_FILE = "./settings.py"

application = Flask(__name__)
application.config.from_pyfile(SETTINGS_FILE)

@application.before_first_request
def create_db():
    db.create_all()

db.init_app(application)
api.init_app(application)
jwt = JWTManager(application)

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


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
