import os
import pytest

from fastapi.testclient import TestClient

from frontend_app.main import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    if os.path.exists("frontend_app.db"):
        os.remove("frontend_app.db")


def test_empty_db(client):
    response = client.get('/kvpairs/ab')
    assert response.status_code == 404


def test_create_and_read(client):
    # create an item with key='ab', value='yz'
    response = client.post('/kvpairs/', json={"key": "ab", "value": "yz"})
    assert response.status_code == 200

    response = client.get('/kvpairs/ab')
    assert response.status_code == 200
