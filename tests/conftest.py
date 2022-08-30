import pytest
from application import application
from models.clients import ClientModel
from models.auth import AuthModel
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='module')
def app():
    """
    Aplicação Flask 
    """

    app = application
    return app

@pytest.fixture(scope='function')
def app_with_token(app):
    """A Webtest app."""
    testapp = app.test_client()
    
    access_token = create_access_token(identity='test', expires_delta=False, fresh=True)
    testapp.header = ('Authorization', f'Bearer {access_token}')

    return testapp


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
