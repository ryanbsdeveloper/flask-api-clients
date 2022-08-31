json = {
  "name": "test",
  "email": "test@email.com",
  "password": "123456789",
  "phone": "11999999999"
}

token_expired = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjE0NDAyODYsIm5iZiI6MTY2MTQ0MDI4NiwianRpIjoiMWIzYmUwOGQtNmZmYy00ZjU5LWFkMDUtMWUwZWM3OGQ1MzhhIiwiZXhwIjoxNjYxNDQzODg2LCJpZGVudGl0eSI6InN0cmluZyIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.2wdqZTkZ70ip7U8_pBixEtGedFQiyDU4Rry30WcYyI4"

def test_verification_authorization_jwt(app):
    """
    Tentar GET e POST em "/clients" e "/client". Cheque se essa rota está necessitando de autenticação
    """

    assert app.test_client().get("/clients").status_code == 401
    assert app.test_client().post("/client", json=json).status_code == 401

def test_verification_if_token_expired(app):
    """
    Expiração do token. Cheque se a restrição de tempo do token está correta
    """

    assert app.test_client().get("/clients", headers={"Authorization": token_expired}).status_code == 401

