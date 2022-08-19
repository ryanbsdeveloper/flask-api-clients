from flask_restx import Api

from .auth import auth_ns
from .clients import client_ns

authorizations = {
    "Bearer":
        {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
}

api = Api(
    title="API de gerenciamento de clientes. ",
    version="0.0.1",
    description="API for manangent client",
    authorizations=authorizations
)
api.add_namespace(auth_ns, '/auth')
api.add_namespace(client_ns)
