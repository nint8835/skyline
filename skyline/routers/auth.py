from typing import cast

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse

from skyline.dependencies.auth import get_username, oauth

auth_router = APIRouter(tags=["Auth"])


@auth_router.get("/login", include_in_schema=False)
async def login(request: Request) -> Response:
    redirect_uri = request.url_for("oauth_callback")
    return cast(Response, await oauth.github.authorize_redirect(request, redirect_uri))


@auth_router.get("/callback", include_in_schema=False)
async def oauth_callback(request: Request) -> Response:
    token = await oauth.github.authorize_access_token(request)

    user = (await oauth.github.get("user", token=token)).json()

    request.session["user"] = user["login"]
    request.session["token"] = token

    return RedirectResponse(url="/")


@auth_router.route("/logout", include_in_schema=False)
async def logout(request: Request) -> Response:
    request.session.pop("user", None)
    request.session.pop("token", None)
    return RedirectResponse(url="/")


@auth_router.get("/me")
async def get_current_user(
    user: str | None = Depends(get_username),
) -> str | None:
    """Retrieve the details of the current user."""
    return user


__all__ = ["auth_router"]
