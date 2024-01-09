import typing

from fastapi import Header, HTTPException

from ..utils import get_api_keys_in_env, get_default_api_key_pattern


class AuthorizerDependency:
    def __init__(self, key_pattern=get_default_api_key_pattern()):
        self.key_pattern = key_pattern

    def __call__(self, x_api_key: typing.Optional[str] = Header(...)):
        if x_api_key not in get_api_keys_in_env(self.key_pattern):
            raise HTTPException(status_code=401, detail="unauthorized")

        return x_api_key
