def get_all_clients(test_client, access_token):
    return test_client.get(
        "/clients",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


def get_client(test_client, access_token):
    return test_client.get(
        "/client/teste@teste.com.br",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


def add_client(test_client, access_token, json):
    return test_client.post(
        "/client",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=json
    )


def put_client(test_client, access_token, json):
    return test_client.put(
        "/client/teste@teste.com.br",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=json
    )


def delete_client(test_client, access_token):
    return test_client.delete(
        "/client/teste@teste.com.br",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
