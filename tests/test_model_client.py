from models.clients import ClientModel

# def test_model_check():
#     """
#     GIVE função save (ClientModel)
#     WHEN Tentar salvar o banco de dados
#     THEN Verificar se a requisição está sendo bem concluida
#     """
#     client = ClientModel()
#     assert client.save() is True

def test_model_new_client():
    """
    GIVE modelo ClientModel
    WHEN Cria um novo cliente
    THEN Cheque os atributos mostre se foram executados corretamente
    """

    client = ClientModel(jwt_identity='test', name='testname', email='test@test.com', password='passwordtest', phone='1100000000')
    assert client.jwt_identity == 'test'
    assert client.name == 'testname'
    assert client.email == 'test@test.com'
    assert client.password == 'passwordtest'
    assert client.phone == '1100000000'

    