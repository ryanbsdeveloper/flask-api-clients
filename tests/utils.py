from flask import url_for

USERNAME = "testeuser"
PASSWORD = "test1234"


def register_user(test_client, username=USERNAME, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_user_register"),
        data=f"username={username}&password={password}",
        content_type="application/json",
    )