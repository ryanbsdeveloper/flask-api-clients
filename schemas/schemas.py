from flask_restx import Namespace, fields


# resources/clients.py
client_ns = Namespace(
    "Clientes", description="Gerenciamento dos clientes", ordered=True, path='/')

user_schema = client_ns.model("Clientes", dict(
    name=fields.String(required=True, description="Nome do cliente"),
    email=fields.String(required=True, description="Email do cliente"),
    password=fields.String(required=True, description="Senha do cliente"),
    phone=fields.String(required=False, description="Número do telefone do cliente")
))

# resources/auth.py
auth_ns = Namespace(
    'JWT', description='Criar autenticação JWT', ordered=True, path='/auth')

auth_schema = auth_ns.model('Criar autenticação', dict(
    username=fields.String(required=True, description='Nome de usuário'),
    password=fields.String(required=True, description='Senha')
))

token_schema = auth_ns.model('Token', dict(
    access_token=fields.String(
        description="Token de acesso para endpoints protegidos."),
))
