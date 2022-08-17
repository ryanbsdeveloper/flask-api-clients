from flask.json import jsonify
from flask import Response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import safe_str_cmp
from models.auth import AuthModel


auth_ns = Namespace('auth', 'Create authorization JWT')

auth_schema = auth_ns.model('Create Auth', dict(
    username=fields.String(required=True, description='username'),
    password=fields.String(required=True, description='password')
))
auth_token = auth_ns.model("User", dict(
    id=fields.Integer(readonly=True, description="User unique id."),
    username=fields.String(required=True, description="User name."),
    password=fields.String(required=True, description="User password.")
))

@auth_ns.route("/user/register")
class AuthRegister(Resource):
    @auth_ns.doc("Create your authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT', model=auth_token)
    def post(self):
        try:
            username = auth_ns.payload.get('username')
            password = auth_ns.payload.get('password')
        except Exception as e:
            return dict(
                message='Preencha os campos corretamente',
                error=e
            )

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if user:
            return jsonify(message="User already registed with it username")

        auth = AuthModel(username=username, password=password)
        auth.save()
        return jsonify(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username)
        )
      
@auth_ns.route("/user/delete")
class AuthDelete(Resource):
    @auth_ns.doc("Delete your authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT', model=auth_token)
    def delete(self):
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

@auth_ns.route("/user/<string:username>")
class AuthOnlyOne(Resource):
    @auth_ns.doc("Check your authorization JWT")
    @auth_ns.response(200, description='Return response token JWT', model=auth_token)
    # @auth_ns.param('email', 'You best email',required=True,)
    def get(self):
        return [auth.as_dict() for auth in AuthModel.get_all()]


@auth_ns.route("/user/login")
class AuthLogin(Resource):
    @auth_ns.doc("Create authorization JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Createad token JWT')
    def post(self):
        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if not user:
            auth_ns.abort(404)

        if safe_str_cmp(user.password, auth_ns.payload.get('password')):
            return dict(
                access_token=create_access_token(user.id),
                refresh_token=create_refresh_token(user.id)
            )
        else:
            auth_ns.abort(403)

