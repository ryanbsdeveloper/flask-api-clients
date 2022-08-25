def test_model_new_auth(db_auth):
    """
    GIVE modelo AuthModel
    WHEN Cria um novo usuario de autenticação
    THEN Cheque os atributos mostre se foram executados corretamente
    """
    assert db_auth.username == 'testmaster'
    assert db_auth.password == 'paasswordtest'


