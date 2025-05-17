import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("API_KEY_DEV", "test")
