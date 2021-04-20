## FastAPI-Key-Auth

```python
from fastapi import FastAPI
from fastapi_key_auth import AuthorizerMiddleware

app = FastAPI()

app.add_middleware(AuthorizerMiddleware)
```

An api key in `headers['x-api-key']` is validated against all values in your apps environment variables starting
with `API_KEY_` before passing it on to your `app`. If the api key it will return a `401 Unauthorized`.
