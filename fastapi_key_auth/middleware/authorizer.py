import re
import typing

from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from ..utils import get_api_keys_in_env, get_default_api_key_pattern


class Authenticator:
    key_pattern: str

    def authenticate(self, conn: HTTPConnection) -> bool:
        if "x-api-key" not in conn.headers:
            raise AuthenticationError("no api key")

        api_key = conn.headers["x-api-key"]
        for key in get_api_keys_in_env(self.key_pattern):
            if api_key == key:
                return True

        raise AuthenticationError("invalid api key")


class AuthorizerMiddleware(Authenticator):
    def __init__(
        self,
        app: ASGIApp,
        key_pattern: str = get_default_api_key_pattern(),
        public_paths: typing.List[str] = [],
        on_error: typing.Optional[
            typing.Callable[[HTTPConnection, AuthenticationError], Response]
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
        self.public_paths_regex: typing.List[str] = [
            path for path in public_paths if path.startswith("^")
        ]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        if len(self.public_paths) > 0:
            for path in self.public_paths:
                if re.match(path, scope["path"]):
                    await self.app(scope, receive, send)
                    return

        if len(self.public_paths_regex) > 0:
            for path in self.public_paths_regex:
                if re.match(path, scope["path"]):
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
