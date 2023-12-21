import pytest
from inferential import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()
