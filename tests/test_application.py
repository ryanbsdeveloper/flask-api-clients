from .utils import (
    add_client,
    delete_client,
    get_all_clients,
    get_client,
    put_client
)
from flask_jwt_extended import create_access_token, get_jwt_identity


def test_name_aplication(app):
    """
    Verificar nome da aplicação. Cheque se o nome atual é "application" nome leva a uma boa prática.
    """

    assert app.name == 'application'


def test_request_return_200(client):
    """
    Tentar acessar a rota "/". Cheque se essa rota retorna um status 200 (OK)
    """

    assert client.get("/").status_code == 200


def test_request_not_found(client):
    """
    Tentar acessar a rota inexistente "/test". Cheque se essa rota falsa retorna um status 404 (NOT FOUND)
    """

    assert client.get("/test").status_code == 404


def test_adding_client(app):
    """ 
    Realizar um POST em clientes. Cheque se o response dessa chamada está com atributos corretos
    """

    access_token = create_access_token('test-jwt')
    response = add_client(app.test_client(), access_token, json={
        "jwt_identity": get_jwt_identity(),
        "name": "Teste",
        "email": "teste@teste.com.br",
        "password": "t1e2s3t4e",
        "phone": "(11) 912345678"
    })
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert "email" in response.json
    assert "email" in response.json
    assert "password" in response.json
    assert "phone" in response.json


def test_update_client(app):
    """
    Realize um PUT em clientes. Cheque se o response dessa chamada está com atributos corretos
    """

    access_token = create_access_token('test-jwt')
    response = put_client(app.test_client(), access_token, json={
        "jwt_identity": get_jwt_identity(),
        "name": "Teste",
        "email": "teste@teste.com.br",
        "password": "t1e2s3t4e",
        "phone": "(11) 912345678"
    })
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert "email" in response.json
    assert "email" in response.json
    assert "password" in response.json
    assert "phone" in response.json


def test_get_all_clients(app):
    """
    Realize um GET ALL em clientes. Cheque se o response dessa chamada está com atributos corretos
    """

    access_token = create_access_token('test-jwt')
    response = get_all_clients(app.test_client(), access_token)
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_get_client(app):
    """
    Realize um GET em clientes. Cheque se o response dessa chamada está com atributos corretos
    """

    access_token = create_access_token('test-jwt')
    response = get_client(app.test_client(), access_token)
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_delete_client(app):
    """
    Realize um DELETE em clientes. Cheque se o response dessa chamada está com atributos corretos
    """

    access_token = create_access_token('test-jwt')
    response = delete_client(app.test_client(), access_token)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
