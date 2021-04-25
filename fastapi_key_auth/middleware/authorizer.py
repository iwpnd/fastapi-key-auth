import os
import re
import typing

from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send


class Authenticator:
    key_pattern: typing.Optional[str] = None

    def api_keys_in_env(self) -> typing.List[typing.Optional[str]]:
        api_keys = []

        for i in os.environ.keys():
            if i.startswith(self.key_pattern if self.key_pattern else "API_KEY_"):
                api_keys.append(os.getenv(i))

        return api_keys

    def authenticate(self, conn: HTTPConnection) -> bool:

        if "x-api-key" not in conn.headers:
            raise AuthenticationError("no api key")

        api_key = conn.headers["x-api-key"]

        if api_key and not any(api_key == key for key in self.api_keys_in_env()):
            raise AuthenticationError("invalid api key")

        return True


class AuthorizerMiddleware(Authenticator):
    def __init__(
        self,
        app: ASGIApp,
        key_pattern: typing.Optional[str] = None,
        public_paths: typing.List[str] = [],
        on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = None,
    ) -> None:
        self.app = app
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = (on_error if on_error is not None else self.default_on_error)
        self.key_pattern = key_pattern
        self.public_paths: typing.List[str] = [
            path for path in public_paths if path.startswith("/")
        ]
        self.public_path_regex: typing.List[str] = [
            path for path in public_paths if path.startswith("^")
        ]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        if scope["path"] in self.public_paths:
            await self.app(scope, receive, send)
            return

        if any([re.match(path, scope["path"]) for path in self.public_path_regex]):
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)

        try:
            auth_result = self.authenticate(conn)
        except AuthenticationError as e:
            response = self.on_error(conn, e)
            await response(scope, receive, send)
            return

        if auth_result:
            await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, e: Exception) -> Response:
        return JSONResponse({"detail": str(e)}, status_code=401)
