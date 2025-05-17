from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from fastapi_key_auth import AuthorizerMiddleware

app = FastAPI()
router = APIRouter()

app.add_middleware(
    AuthorizerMiddleware, public_paths=["/health", "/docs", "/router", "^/regex"]
)


@router.get("/router")
async def get_router() -> dict[str, bool]:
    return {"ok": True}


app.include_router(router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "pong!"}


@app.get("/regex/test")
async def regex() -> dict[str, bool]:
    return {"regex": True}


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


client = TestClient(app)


def test_unauthorized_no_api_key() -> None:
    response = client.get("/ping")
    assert response.status_code == 401
    assert response.json() == {"detail": "no api key"}


def test_unauthorized_invalid_api_key() -> None:
    response = client.get("/ping", headers={"x-api-key": "baguette"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid api key"}


def test_unauthorized_empty_api_key() -> None:
    response = client.get("/ping", headers={"x-api-key": ""})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid api key"}


def test_authorized() -> None:
    response = client.get("/ping", headers={"x-api-key": "test"})

    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_public_path() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_docs_path() -> None:
    response = client.get("/docs")
    assert response.status_code == 200


def test_router() -> None:
    response = client.get("/router")
    assert response.status_code == 200


def test_regex() -> None:
    response = client.get("/regex/test")
    assert response.status_code == 200
