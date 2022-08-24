import pytest
from application import application

@pytest.fixture()
def app():
    app = application
    app.config.update({
        "TESTING": True,
    })
    return app

