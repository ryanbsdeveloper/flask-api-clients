"""Unit tests for api.auth_register API endpoint."""
from http import HTTPStatus

from models.auth import AuthModel
from utils import USERNAME, PASSWORD, register_user

SUCCESS = "successfully registered"
USERNAME_ALREADY_EXISTS = f"{USERNAME} is already registered"
BAD_REQUEST = "Input payload validation failed"

def test_auth_register(client):
    response = register_user(client)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    result = AuthModel.decode_access_token(access_token)
    assert result.success
    user_dict = result.value
    assert not user_dict["admin"]
    user = AuthModel.find_by_public_id(user_dict["public_id"])
    assert user and user.username == USERNAME

def test_auth_register_email_already_registered(client, db):
    user = AuthModel(username=USERNAME, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    response = register_user(client)
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json and response.json["message"] == USERNAME_ALREADY_EXISTS
    )
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json

def test_auth_register_invalid_email(client):
    invalid_email = 8
    response = register_user(client, username=invalid_email)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json
    assert "errors" in response.json
    assert "password" not in response.json["errors"]
    assert "email" in response.json["errors"]
    assert response.json["errors"]["username"] == f"{invalid_email} is not a valid email"