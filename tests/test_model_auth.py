def test_model_new_auth(db_auth):
    """
    Cria um novo usuario de autenticação
    """
    assert db_auth.username == 'testmaster'
    assert db_auth.password == 'paasswordtest'


