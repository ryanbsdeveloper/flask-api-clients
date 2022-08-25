def test_name_aplication(app):
    """
    GIVE Aplicação
    WHEN Verificar nome da aplicação
    THEN Cheque se o nome atual é "application" nome leva a uma boa prática.
    """

    assert app.name == 'application'

def test_request_return_200(client):
    """
    GIVE Situação cliente
    WHEN Tentar acessar a rota "/"
    THEN Cheque se essa rota retorna um status 200 (OK)
    """

    assert client.get("/").status_code == 200

def test_request_not_found(client):
    """
    GIVE Situação cliente
    WHEN Tentar acessar a rota inexistente "/test"
    THEN Cheque se essa rota falas retorna um status 404 (NOT FOUND)
    """

    assert client.get("/test").status_code == 404

