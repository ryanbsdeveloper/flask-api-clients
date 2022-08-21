"""
 copyrigth © ryanbsdeveloper
 2022 - brazil
"""

from flask import Response, json
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from models.clients import ClientModel
from schemas.schemas import client_ns, user_schema


@client_ns.route("/clients")
class Users(Resource):
    @client_ns.doc("Listar todos clientes", security="Bearer")
    @client_ns.response(code=200, description='', model=user_schema)
    @jwt_required
    def get(self):
        """Possibilita pegar todos clientes criados por você."""

        identity_jwt = get_jwt_identity()
        return dict(clients=[user.as_dict() for user in ClientModel.get_all_jwt_identity(identity_jwt)])


@client_ns.route("/client")
class Users(Resource):
    @client_ns.doc("Criar clientes", security="Bearer")
    @client_ns.expect(user_schema, validate=True)
    @client_ns.response(code=201, model=user_schema, description='')
    @jwt_required
    def post(self):
        """Possibilita criar um novo cliente."""

        identity_jwt = get_jwt_identity()

        name = client_ns.payload.get('name')
        email = client_ns.payload.get('email')
        password = client_ns.payload.get('password')
        phone = client_ns.payload.get('phone')

        check_client = ClientModel.find_by_email(email, identity_jwt)
        if check_client:
            return Response(
                response=json.dumps({
                    "message": "Email já em uso por outro cliente."
                }),
                status=400,
                mimetype='application/json'
            )

        if not name or not email or not password:
            return Response(
                response=json.dumps({
                    "message": "Campos incorretos."
                }),
                status=400,
                mimetype='application/json'
            )

        # Check fields
        if len(name) < 3:
            return Response(
                response=json.dumps({
                    "message": "Nome ínvalido."
                }),
                status=400,
                mimetype='application/json'
            )
        if "@" not in email or len(email) < 3:
            return Response(
                response=json.dumps({
                    "message": "Email ínvalido."
                }),
                status=400,
                mimetype='application/json'
            )
        if len(password) < 3:
            return Response(
                response=json.dumps({
                    "message": "Senha ínvalida."
                }),
                status=400,
                mimetype='application/json'
            )

        client = ClientModel(
            jwt_identity=identity_jwt,
            name=client_ns.payload.get('name'),
            email=client_ns.payload.get('email'),
            password=client_ns.payload.get('password'),
            phone=client_ns.payload.get('phone')
        )

        client.save()
        return client.as_dict(), 201


@client_ns.route("/client/<string:email>")
@client_ns.response(404, 'Cliente não encontrado.')
class User(Resource):
    @client_ns.doc("Pegar cliente", security="Bearer")
    @client_ns.response(code=201, model=user_schema, description='')
    @jwt_required
    def get(self, email):
        """Possibilita pegar dados de um cliente."""

        identity_jwt = get_jwt_identity()

        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response(
                response=json.dumps({
                    "message": "Cliente não encontrado."
                }),
                status=404,
                mimetype='application/json'
            )

        return client.as_dict()

    @client_ns.doc("Deletar cliente", security="Bearer")
    @client_ns.response(204, "User removed.")
    @jwt_required
    def delete(self, email):
        """Possibilita deletar um cliente."""

        identity_jwt = get_jwt_identity()

        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response(
                response=json.dumps({
                    "message": "Cliente não encontrado."
                }),
                status=404,
                mimetype='application/json'
            )

        client.delete()
        return Response(
            response=json.dumps({
                "message": "Cliente deletado."
            }),
            status=200,
            mimetype='application/json'
        )

    @client_ns.doc("Atualizar cliente", security="Bearer")
    @client_ns.expect(user_schema, validate=True)
    @client_ns.response(code=201, model=user_schema, description='')
    @jwt_required
    def put(self, email):
        """Possibilita atualizar os dados de um cliente."""

        identity_jwt = get_jwt_identity()

        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response(
                response=json.dumps({
                    "message": "Cliente não encontrado."
                }),
                status=404,
                mimetype='application/json'
            )            

        name = client_ns.payload.get('name')
        email = client_ns.payload.get('email')
        password = client_ns.payload.get('password')
        phone = client_ns.payload.get('phone')

        if not name or not email or not password:
            return Response(
                response=json.dumps({
                    "message": "Cliente incorretos."
                }),
                status=400,
                mimetype='application/json'
            )

        # Check fields
        if len(name) < 3:
            return Response(
                response=json.dumps({
                    "message": "Nome ínvalido."
                }),
                status=400,
                mimetype='application/json'
            )
        if "@" not in email or len(email) < 3:
            return Response(
                response=json.dumps({
                    "message": "Email ínvalido."
                }),
                status=400,
                mimetype='application/json'
            )

        if len(password) < 3:
            return Response(
                response=json.dumps({
                    "message": "Senha ínvalida."
                }),
                status=400,
                mimetype='application/json'
            )

        client.name = name
        client.email = email
        client.password = password
        client.phone = phone
        client.save()

        return client.as_dict(), 200
