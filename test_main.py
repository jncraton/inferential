import pytest
from app import *

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    return app.test_client()
