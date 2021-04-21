import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("API_KEY_DEV", "test")
