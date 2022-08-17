from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_jwt_extended import jwt_required

from flask_restx import Resource, Namespace, fields

from models.user import UserModel


user_ns = Namespace("clients", description="Customer management", ordered=True)

user_schema = user_ns.model("User", dict(
    id=fields.Integer(readonly=True, description="User unique id."),
    username=fields.String(required=True, description="User name."),
    password=fields.String(required=True, description="User password.")
))


@user_ns.route("/")
class Users(Resource):
    @user_ns.doc(shortcut="Listar clientes")
    @user_ns.marshal_list_with(user_schema, skip_none=True)
    @jwt_required
    def get(self):
        return [user.as_dict() for user in UserModel.get_all()]

    @user_ns.doc("create_user")
    @user_ns.expect(user_schema)
    @user_ns.marshal_with(user_schema, skip_none=True)
    @jwt_required
    def post(self):
        user = UserModel(
            username=user_ns.payload.get('username'),
            password=user_ns.payload.get('password')
        )
        user.save()
        return user.as_dict(), 201


@user_ns.route("/<int:id>")
@user_ns.response(404, 'User not found.')
class User(Resource):
    @user_ns.doc("get_user")
    @user_ns.marshal_with(user_schema, skip_none=True)
    @jwt_required
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            user_ns.abort(404)
        return user.as_dict()

    @user_ns.doc("delele_user")
    @user_ns.response(204, "User removed.")
    @jwt_required
    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete()
        return '', 204

token_schema = user_ns.model('Token', dict(
    access_token=fields.String(description="Access token for protected endpoints"),
))

@user_ns.route("/login")
class Login(Resource):
    @user_ns.doc("post_user_login")
    @user_ns.expect(user_schema)
    @user_ns.response(404, "User not found.")
    @user_ns.response(403, "Authentication failed.")
    @user_ns.marshal_with(token_schema)
    def post(self):
        user = UserModel.find_by_username(user_ns.payload.get('username'))
        if not user:
            user_ns.abort(404)

        if safe_str_cmp(user.password, user_ns.payload.get('password')):
            return dict(
                access_token=create_access_token(user.id),
                refresh_token=create_refresh_token(user.id)
            )
        else:
            user_ns.abort(403)
