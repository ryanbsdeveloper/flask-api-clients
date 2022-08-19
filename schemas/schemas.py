from flask_restx import Namespace, fields


# resources/clients.py
client_ns = Namespace("clients", description="Gerenciamento dos clientes", ordered=True)

user_schema = client_ns.model("Clients", dict(
    name=fields.String(required=True, description="Client name."),
    email=fields.String(required=True, description="Email of client."),
    password=fields.String(required=True, description="Password of client."),
    phone=fields.String(required=False, description=" Number phone of client.")
))

# resources/auth.py
auth_ns = Namespace(
    'auth', description='Criar autenticação JWT', ordered=True)

auth_schema = auth_ns.model('Create Auth', dict(
    username=fields.String(required=True, description='username'),
    password=fields.String(required=True, description='password')
))

token_schema = auth_ns.model('Token', dict(
    access_token=fields.String(description="Token de acesso para endpoints protegidos."),
))
