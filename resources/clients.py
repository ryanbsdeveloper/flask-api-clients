from flask import Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace, fields

from models.clients import ClientModel


client_ns = Namespace("clients", description="Gerenciamento dos clientes", ordered=True)

user_schema = client_ns.model("Clients", dict(
    name=fields.String(required=True, description="Client name."),
    email=fields.String(required=True, description="Email of client."),
    password=fields.String(required=True, description="Password of client."),
    phone=fields.String(required=False, description=" Number phone of client.")
))

@client_ns.route("/")
class Users(Resource):
    @client_ns.doc("List clients", security="Bearer")
    @client_ns.response(code=200, description='', model=user_schema)
    @jwt_required
    def get(self):
        """Possibilita pegar todos clientes criados por você."""

        identity_jwt = get_jwt_identity()
        return dict(clients=[user.as_dict() for user in ClientModel.get_all_jwt_identity(identity_jwt)])

    @client_ns.doc("Create clients", security="Bearer")
    @client_ns.expect(user_schema)
    @client_ns.response(code=201, model=user_schema, description='')
    @jwt_required
    def post(self):
        """Possibilita criar um novo cliente."""

        identity_jwt = get_jwt_identity()

        name = client_ns.payload.get('name')
        email = client_ns.payload.get('email')
        password = client_ns.payload.get('password')
        phone = client_ns.payload.get('phone')
        
        check_client = ClientModel.find_by_email(email)
        if check_client:
            if str(check_client.jwt_identity) == str(identity_jwt):
                print('entrei mesmo')
                return Response('Email já em uso por outro cliente.', 400)

        if not name or not email or not password:
            return Response('Campos incorretos', 400)

        # Check fields
        if len(name) < 3:
            return Response('Nome ínvalido.', 400)
        if "@" not in email or len(email) < 3:
            return Response('Email ínvalido', 400)
        if len(password) < 3:
            return Response('Senha ínvalida.', 400)

        client = ClientModel(
            jwt_identity=identity_jwt,
            name=client_ns.payload.get('name'),
            email=client_ns.payload.get('email'),
            password=client_ns.payload.get('password'),
            phone=client_ns.payload.get('phone')
        )

        client.save()
        return client.as_dict(), 201


@client_ns.route("/<int:id>")
@client_ns.response(404, 'Cliente não encontrado.')
class User(Resource):
    @client_ns.doc("Get user", security="Bearer")
    @client_ns.marshal_with(user_schema, skip_none=True)
    @jwt_required
    def get(self, id):
        """Possibilita pegar dados de um cliente."""

        client = ClientModel.find_by_id(id)
        if not client:
            return Response('Cliente não encontrado.', 404)
            
        return client.as_dict()

    @client_ns.doc("delele_user", security="Bearer")
    @client_ns.response(204, "User removed.")
    @jwt_required
    def delete(self, id):
        """Possibilita deletar um cliente."""

        client = ClientModel.find_by_id(id)
        if client:
            client.delete()
        return '', 204

    @client_ns.doc("delele_user", security="Bearer")
    def put(self):
        """Possibilita atualizar os dados de um cliente."""

        print(":)")

