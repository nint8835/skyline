from typing import Any

from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException, Request

from skyline.config import config

oauth = OAuth()
oauth.register(
    "github",
    client_id=config.github_client_id,
    client_secret=config.github_client_secret,
    api_base_url="https://api.github.com/",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    client_kwargs={
        "scope": "read:user",
    },
)


def get_username(request: Request) -> str | None:
    return request.session.get("user")


def require_user(request: Request) -> str:
    username = get_username(request)
    if username is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return username


def get_token(request: Request) -> Any | None:
    return request.session.get("token")


def require_token(request: Request) -> Any:
    token = get_token(request)
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return token


__all__ = ["oauth", "get_username", "require_user", "get_token", "require_token"]
