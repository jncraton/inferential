import yaml
import pytest
from inferential import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()


def pytest_configure(config):
    with open("config.yml", "r") as f:
        pytest.conf = yaml.safe_load(f)

    client = create_app({"TESTING": True}).test_client()
    while not client.get("/api/status").json["loadedAll"]:
        pass
