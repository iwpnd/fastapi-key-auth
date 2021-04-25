from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_key_auth import AuthorizerMiddleware

app = FastAPI()

app.add_middleware(AuthorizerMiddleware, key_pattern="KEY_")


@app.get("/ping")
async def ping():
    return {"ping": "pong!"}


client = TestClient(app)


def test_unauthorized_no_api_key_custom_pattern():
    response = client.get("/ping")
    assert response.status_code == 401
    assert response.json() == {"detail": "no api key"}


def test_unauthorized_invalid_api_key_custom_pattern(monkeypatch):
    monkeypatch.setenv("KEY_TEST", "test")
    response = client.get("/ping", headers={"x-api-key": "baguette"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid api key"}


def test_authorized_custom_pattern(monkeypatch):
    monkeypatch.setenv("KEY_TEST", "test")
    response = client.get("/ping", headers={"x-api-key": "test"})
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
