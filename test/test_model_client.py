from models.clients import ClientModel

def test_model_new_client():
    """
    GIVE modelo ClientModel
    WHEN Cria um novo cliente
    THEN Cheque os atributos mostre se foram executados corretamente
    """

    auth = ClientModel(jwt_identity='test', name='testname', email='test@test.com', password='passwordtest', phone='1100000000')
    assert auth.jwt_identity == 'test'
    assert auth.name == 'testname'
    assert auth.email == 'test@test.com'
    assert auth.password == 'passwordtest'
    assert auth.phone == '1100000000'
    
    