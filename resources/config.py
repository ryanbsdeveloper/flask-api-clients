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
    title="API de gerenciamento de clientes.",
    version="0.1.0",
    description="API para gerenciar dados de clientes para sua aplicação.",
    authorizations=authorizations,
    contact_url="http://portryan-env-1.eba-r3mjces3.us-east-1.elasticbeanstalk.com/",
    contact_email="ryanbsdeveloper@gmail.com",
    contact='Desenvolvedor',

)
api.add_namespace(auth_ns, '/auth')
api.add_namespace(client_ns)
