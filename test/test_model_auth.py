from models.auth import AuthModel

def test_model_new_auth():
    """
    GIVE modelo AuthModel
    WHEN Cria um novo usuario de autenticação
    THEN Cheque os atributos mostre se foram executados corretamente
    """
    auth = AuthModel(username='testmaster', password='paasswordtest')
    assert auth.username == 'testmaster'
    assert auth.password == 'paasswordtest'


