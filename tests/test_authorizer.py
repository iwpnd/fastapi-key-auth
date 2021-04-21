from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_key_auth.authorizer import AuthorizerMiddleware

app = FastAPI()
app.add_middleware(AuthorizerMiddleware)


@app.get("/ping")
async def read_main():
    return {"ping": "pong"}


client = TestClient(app)


def test_unauthorized_no_api_key():
    response = client.get("/ping")
    assert response.status_code == 401
    assert response.text == "no api key"


def test_unauthorized_invalid_api_key():
    response = client.get("/ping", headers={"x-api-key": "baguette"})
    assert response.status_code == 401
    assert response.text == "invalid api key"


def test_authorized():
    response = client.get("/ping", headers={"x-api-key": "test"})

    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
