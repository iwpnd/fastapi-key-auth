<br />
<p align="center">
  <h3 align="center">FastAPI-key-auth</h3>

  <p align="center">
    Secure your FastAPI endpoints using API keys.
    <br />
    <a href="https://github.com/iwpnd/fastapi-key-auth/issues">Report Bug</a>
    ·
    <a href="https://github.com/iwpnd/fastapi-key-auth/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

On deployment inject API keys authorized to use your service. Every call to a private
endpoint of your service has to include a `header['x-api-key']` attribute that is
validated against the API keys in your environment.
If it is present, a request is authorized. If it is not FastAPI return `401 Unauthorized`.
Use this either as a middleware, or as Dependency.

### Built With

-   [starlette](https://github.com/encode/starlette)
-   [fastapi](https://github.com/tiangolo/fastapi)

<!-- GETTING STARTED -->

## Getting Started

### Installation

1. Clone and install
    ```sh
    git clone https://github.com/iwpnd/fastapi-key-auth.git
    poetry install
    ```
2. Install with pip
    ```sh
    pip install fastapi-key-auth
    ```
3. Install with poetry
    ```sh
    poetry add fastapi-key-auth
    ```

## Usage

As Middleware:

```python
from fastapi import FastAPI
from fastapi_key_auth import AuthorizerMiddleware

app = FastAPI()

app.add_middleware(AuthorizerMiddleware, public_paths=["/ping"], key_pattern="API_KEY_")

# optional use regex startswith
app.add_middleware(AuthorizerMiddleware, public_paths=["/ping", "^/users"])
```

As Dependency

```python
from fastapi import FastAPI, Depends
from fastapi_key_auth import AuthorizerDependency

authorizer = AuthorizerDependency(key_pattern="API_KEY_")

# either globally or in a router
app = FastAPI(dependencies=[Depends(authorizer)])
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Benjamin Ramser - [@imwithpanda](https://twitter.com/imwithpanda) - ahoi@iwpnd.pw  
Project Link: [https://github.com/iwpnd/fastapi-key-auth](https://github.com/iwpnd/fastapi-key-auth)
