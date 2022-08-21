from models.auth import AuthModel

def test_model_new_auth():

    """
    GIVE modelo AuthModel
    WHEN Cria um novo usuario de autenticação
    THEN Cheque o username, password e mostre os definidos corretamente
    """

    user = AuthModel('testmaster', 'paasswordtest')
    assert user.username == 'testmaster'
    assert user.password == 'paasswordtest'
    
