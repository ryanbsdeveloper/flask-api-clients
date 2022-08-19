from flask import Response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from models.clients import ClientModel
from schemas.schemas import client_ns, user_schema

@client_ns.route("/")
class Users(Resource):
    @client_ns.doc("Listar clientes", security="Bearer")
    @client_ns.response(code=200, description='', model=user_schema)
    @jwt_required
    def get(self):
        """Possibilita pegar todos clientes criados por você."""

        identity_jwt = get_jwt_identity()
        return dict(clients=[user.as_dict() for user in ClientModel.get_all_jwt_identity(identity_jwt)])

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


@client_ns.route("/<string:email>")
@client_ns.response(404, 'Cliente não encontrado.')
class User(Resource):
    @client_ns.doc("Pegar cliente", security="Bearer")
    @client_ns.marshal_with(user_schema, skip_none=True)
    @jwt_required
    def get(self, email):
        """Possibilita pegar dados de um cliente."""
        
        identity_jwt = get_jwt_identity()

        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response('Cliente não encontrado.', 404)
            
        return client.as_dict()

    @client_ns.doc("Deletar cliente", security="Bearer")
    @client_ns.response(204, "User removed.")
    @jwt_required
    def delete(self, email):
        """Possibilita deletar um cliente."""

        identity_jwt = get_jwt_identity()

        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response('Cliente não encontrado.', 404)

        client.delete()
        return Response('Cliente deletado.', 200)

    @client_ns.doc("Atualizar cliente", security="Bearer")
    @client_ns.expect(user_schema, validate=True)
    @client_ns.response(code=201, model=user_schema, description='')
    @jwt_required
    def put(self, email):
        """Possibilita atualizar os dados de um cliente."""

        identity_jwt = get_jwt_identity()
        
        client = ClientModel.find_by_email(email, identity_jwt)
        if not client:
            return Response('Cliente não encontrado.', 404)
        
        name = client_ns.payload.get('name')
        email = client_ns.payload.get('email')
        password = client_ns.payload.get('password')
        phone = client_ns.payload.get('phone')

        if not name or not email or not password:
            return Response('Campos incorretos', 400)

        # Check fields
        if len(name) < 3:
            return Response('Nome ínvalido.', 400)
        if "@" not in email or len(email) < 3:
            return Response('Email ínvalido', 400)
        if len(password) < 3:
            return Response('Senha ínvalida.', 400)
        
        client.name = name
        client.email = email
        client.password = password
        client.phone = phone
        
        return client.as_dict(), 200


