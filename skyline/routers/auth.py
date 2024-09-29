from typing import cast

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

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

auth_router = APIRouter(tags=["Auth"])


@auth_router.get("/login", include_in_schema=False)
async def login(request: Request) -> Response:
    redirect_uri = request.url_for("oauth_callback")
    return cast(Response, await oauth.github.authorize_redirect(request, redirect_uri))


@auth_router.get("/callback", include_in_schema=False)
async def oauth_callback(request: Request) -> Response:
    token = await oauth.github.authorize_access_token(request)

    user = await oauth.github.get("user", token=token)

    print(user.json())
    return RedirectResponse(url="/")


__all__ = ["auth_router"]
