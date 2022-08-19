from email import message
from flask.json import jsonify
from flask import Response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token, 
    decode_token, jwt_required)
from werkzeug.security import safe_str_cmp
from models.auth import AuthModel
from schemas.schemas import auth_ns, auth_schema, token_schema


@auth_ns.route("/user/register")
class AuthRegister(Resource):
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Autenticação JWT criada.', model=auth_schema)
    def post(self):
        """Registre seu usuario de login"""
        username = auth_ns.payload.get('username')
        password = auth_ns.payload.get('password')

        if not username or not password:
            return Response(response="Campos incorretos", status=400)

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if user:
            return Response(response="Usuário já registrado com este nome. ", status=400)

        auth = AuthModel(username=username, password=password)
        auth.save()
        return jsonify(
            access_token=create_access_token(username),
        )


@auth_ns.route("/user/delete")
class AuthDelete(Resource):
    @auth_ns.doc("Deletar sua autenticação JWT", security="Bearer")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(200, description='Autenticação JWT deletada.', model=auth_schema)
    @jwt_required
    def delete(self):
        """Delete seu usuario de login"""

        username = auth_ns.payload.get('username')
        password = auth_ns.payload.get('password')

        if not username or not password:
            return Response("Campos incorretos")

        user = AuthModel.find_by_username(username)
        if not user:
            return Response('Usuário não registrado', 400)

        if safe_str_cmp(user.password, password):
            user.delete()
            return Response('Deletado', 200)
        else:
            return Response('Senha incorreta', 401)


@auth_ns.route("/user/login")
class AuthLogin(Resource):
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Token de acesso para endpoints protegidos.', model=token_schema)
    def post(self):
        """Logue com seu usuario de login e tenha o acesso ao token."""

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if not user:
            return Response('Usuário de autenticação não registrado.', 404)

        if safe_str_cmp(user.password, auth_ns.payload.get('password')):
            create_refresh_token(user.username)
            return dict(
                access_token=create_access_token(user.username)
            )
        else:
            return Response('Senha incorreta.', 403)
            
