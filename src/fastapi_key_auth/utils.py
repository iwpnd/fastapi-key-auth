import os
import typing


def get_default_api_key_pattern() -> str:
    return "API_KEY_"


def get_api_keys_in_env(key_pattern: str) -> typing.List[typing.Optional[str]]:
    return [os.getenv(key) for key in os.environ.keys() if key.startswith(key_pattern)]
