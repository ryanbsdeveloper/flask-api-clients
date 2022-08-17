from flask.json import jsonify
from flask import Response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_refresh_token, create_access_token, decode_token
from werkzeug.security import safe_str_cmp
from models.auth import AuthModel


auth_ns = Namespace('auth', description='Create authorization JWT', ordered=True)

auth_schema = auth_ns.model('Create Auth', dict(
    username=fields.String(required=True, description='username'),
    password=fields.String(required=True, description='password')
))

auth_token = auth_ns.model('Token', dict(
    access_token=fields.String(description='JWT authorization token'),
))

@auth_ns.route("/user/register")
class AuthRegister(Resource):
    @auth_ns.doc("Create your authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT', model=auth_schema)
    def post(self):
        """Register your login user"""
        username = auth_ns.payload.get('username')
        password = auth_ns.payload.get('password')

        if not username or not password:
            return Response(response="Fields incorrets", status=400)

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if user:
            return Response(response="User already registed with it username", status=400)

        auth = AuthModel(username=username, password=password)
        auth.save()
        return jsonify(
            access_token=create_access_token(username),
        )
      
@auth_ns.route("/user/delete")
class AuthDelete(Resource):
    @auth_ns.doc("Delete your authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT', model=auth_schema)
    def delete(self):
        """Delete your login user."""

        username = auth_ns.payload.get('username')
        password = auth_ns.payload.get('password')

        if not username or not password:
            return Response("Fields incorrets")

        user = AuthModel.find_by_username(username)
        if safe_str_cmp(user.password, password):
            user.delete()
            return Response('Deleted', 200)
        else:
            return Response('Password incorret', 401)

@auth_ns.route("/user/login")
class AuthLogin(Resource):
    @auth_ns.doc("Create authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT', model=auth_token)
    def post(self):
        """Log in with your user and get access to the token."""

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if not user:
            auth_ns.abort(404)

        if safe_str_cmp(user.password, auth_ns.payload.get('password')):
            return dict(
                access_token=create_access_token(user.id),
            )
        else:
            auth_ns.abort(403)

