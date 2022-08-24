def test_name_aplication(app):
    assert app.name == 'application'

def test_request_return_200(client):
    client.get("/").status_code == 200