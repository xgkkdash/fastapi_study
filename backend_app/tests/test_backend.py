import os
import pytest

from fastapi.testclient import TestClient

from backend_app.main import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
    if os.path.exists("backend_app.db"):
        os.remove("backend_app.db")


def test_empty_db(client):
    response = client.get('/details/5')
    assert response.status_code == 404


def test_create_and_read(client):
    # create an item with id=5, description='test_back'
    response = client.post('/details/', json={"id": 5, "description": "test_back"})
    assert response.status_code == 200

    response = client.get('/details/5')
    assert response.status_code == 200
