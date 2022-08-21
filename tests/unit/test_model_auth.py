from models.auth import AuthModel

def test_model_new_auth():

    """
    GIVE modeLs AuthModel
    WHEN created a new user of authentication
    THEN Cheque o username, password e mostre os definidos corretamente
    """


    user = AuthModel('testmaster', 'paasswordtest')
    assert user.username == 'testmaster'
    assert user.password == 'paasswordtest'
    
