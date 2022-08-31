def test_model_new_client(db_client):
    """
    Cria um novo cliente
    """

    assert db_client.jwt_identity == 'test'
    assert db_client.name == 'testname'
    assert db_client.email == 'test@test.com'
    assert db_client.password == 'passwordtest'
    assert db_client.phone == '1100000000'
