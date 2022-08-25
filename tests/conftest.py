import pytest
from application import application
from models.clients import ClientModel
from models.auth import AuthModel


@pytest.fixture(scope='function')
def app():
    """
    Aplicação Flask
    """

    app = application
    return app


@pytest.fixture(scope='module')
def db_auth():
    """
    Modelo dos dados dos usuários de autenticação
    """

    auth = AuthModel(username='testmaster', password='paasswordtest')
    return auth


@pytest.fixture(scope='module')
def db_client():
    """
    Modelo dos dados dos clientes
    """

    client = ClientModel(jwt_identity='test', name='testname',
                         email='test@test.com', password='passwordtest', phone='1100000000')
    return client
