"""
 copyrigth © ryanbsdeveloper
 2022 - brazil
"""

from flask import Response, json
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    jwt_required)
from werkzeug.security import safe_str_cmp
from models.auth import AuthModel
from schemas.schemas import auth_ns, auth_schema, token_schema


@auth_ns.route("/user/register")
class AuthRegister(Resource):
    @auth_ns.doc("Criar sua autenticação JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Autenticação JWT criada.', model=auth_schema)
    def post(self):
        """Registre seu usuario de login"""
        username = auth_ns.payload.get('username')
        password = auth_ns.payload.get('password')

        if not username or not password:
            return Response(
                response=json.dumps({
                    "message": "Campos incorretos."
                }),
                status=400,
                mimetype='application/json'
            )

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))
        if user:
            return Response(
                response=json.dumps({
                    "message": "Usuário já registrado com este nome."
                }),
                status=400,
                mimetype='application/json'
            )

        auth = AuthModel(username=username, password=password)
        auth.save()

        return Response(
            response=json.dumps({
                "acces_token": create_access_token(username)
            }),
            status=200,
            mimetype='application/json'
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
            return Response(
                response=json.dumps({
                    "message": "Campos incorretos."
                }),
                status=404,
                mimetype='application/json'
            )

        user = AuthModel.find_by_username(username)
        if not user:
            return Response(
                response=json.dumps({
                    "message": "Usuário não registrado."
                }),
                status=400,
                mimetype='application/json'
            )

        if safe_str_cmp(user.password, password):
            user.delete()
            return Response(
                response=json.dumps({
                    "message": " Cliente deletado."
                }),
                status=400,
                mimetype='application/json'
            )

        else:
            return Response(
                response=json.dumps({
                    "message": "Senha incorreta."
                }),
                status=401,
                mimetype='application/json'
            )


@auth_ns.route("/user/login")
class AuthLogin(Resource):
    @auth_ns.doc("Consulte sua autenticação JWT")
    @auth_ns.expect(auth_schema)
    @auth_ns.response(201, description='Token de acesso para endpoints protegidos.', model=token_schema)
    def post(self):
        """Logue com seu usuario de login e tenha o acesso ao token."""

        user = AuthModel.find_by_username(auth_ns.payload.get('username'))

        if not user:
            return Response(
                response=json.dumps({
                    "message": "Usuário de autenticação não registrado."
                }),
                status=404,
                mimetype='application/json'
            )

        if safe_str_cmp(user.password, auth_ns.payload.get('password')):
            create_refresh_token(user.username)
            return Response(
                response=json.dumps({
                    "access_token": create_access_token(user.username)
                }),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({
                    "message": "Senha incorreta."
                }),
                status=403,
                mimetype='application/json'
            ) 
