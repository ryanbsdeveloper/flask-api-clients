from flask_restx import Api

from .auth import auth_ns
from .user import user_ns

authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(title="Client API", version="0.0.1", description="API for manangent client",
          authorizations=authorizations )

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
