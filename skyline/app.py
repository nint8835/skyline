from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.sessions import SessionMiddleware

from skyline.config import config
from skyline.routers import auth_router, contributions_router


def generate_unique_id(route: APIRoute) -> str:
    return route.name


app = FastAPI(
    title="Skyline",
    generate_unique_id_function=generate_unique_id,
)

app.add_middleware(SessionMiddleware, secret_key=config.session_secret)

app.include_router(auth_router, prefix="/auth")
app.include_router(contributions_router, prefix="/contributions")

__all__ = ["app"]
