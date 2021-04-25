from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from fastapi_key_auth.authorizer import AuthorizerMiddleware

app = FastAPI()
router = APIRouter()

app.add_middleware(
    AuthorizerMiddleware, public_paths=["/health", "/docs", "/router", "^/regex"]
)


@router.get("/router")
async def get_router():
    return {"ok": True}


app.include_router(router)


@app.get("/ping")
async def ping():
    return {"ping": "pong!"}


@app.get("/regex/test")
async def regex():
    return {"regex": True}


@app.get("/health")
async def health():
    return {"ok": True}


client = TestClient(app)


def test_unauthorized_no_api_key():
    response = client.get("/ping")
    assert response.status_code == 401
    assert response.json() == {"details": "no api key"}


def test_unauthorized_invalid_api_key():
    response = client.get("/ping", headers={"x-api-key": "baguette"})
    assert response.status_code == 401
    assert response.json() == {"details": "invalid api key"}


def test_authorized():
    response = client.get("/ping", headers={"x-api-key": "test"})

    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_public_path():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_docs_path():
    response = client.get("/docs")
    assert response.status_code == 200


def test_router():
    response = client.get("/router")
    assert response.status_code == 200


def test_regex():
    response = client.get("/regex/test")
    assert response.status_code == 200
