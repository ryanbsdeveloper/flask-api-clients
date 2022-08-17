from flask_restx import Api

from .cat import ns as cat_ns
from .dog import ns as dog_ns
from .user import ns as user_ns

authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(title="Client API", version="0.0.1", description="API for manangent client",
          authorizations=authorizations)
api.add_namespace(cat_ns)
api.add_namespace(dog_ns)
api.add_namespace(user_ns)
