import os
import typing

from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send


def api_keys_in_env() -> typing.Sequence[str]:
    api_keys = []

    for i in os.environ.keys():
        if i.startswith("API_KEY_"):
            api_keys.append(os.getenv(i))

    return api_keys


def authenticate(conn: HTTPConnection) -> None:
    if "x-api-key" not in conn.headers:
        raise AuthenticationError("no api key")

    api_key = conn.headers["x-api-key"]

    if api_key and not any(api_key == key for key in api_keys_in_env()):
        raise AuthenticationError("invalid api key")

    return


class AuthorizerMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        public_paths: typing.Optional[typing.List[str]] = [],
        on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = None,
    ) -> None:
        self.app = app
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = (on_error if on_error is not None else self.default_on_error)
        self.public_path = public_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        if scope["path"] in self.public_path:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)

        try:
            result = authenticate(conn)
        except AuthenticationError as e:
            response = self.on_error(conn, e)
            await response(scope, receive, send)
            return

        if result is None:
            await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, e: Exception) -> Response:
        return PlainTextResponse(str(e), status_code=401)
