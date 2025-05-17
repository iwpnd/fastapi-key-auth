import os


def get_default_api_key_pattern() -> str:
    return "API_KEY_"


def get_api_keys_in_env(key_pattern: str) -> list[str | None]:
    return [os.getenv(key) for key in os.environ if key.startswith(key_pattern)]
