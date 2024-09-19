from fastapi import FastAPI
from fastapi.routing import APIRoute


def generate_unique_id(route: APIRoute) -> str:
    return route.name


app = FastAPI(
    title="Skyline",
    generate_unique_id_function=generate_unique_id,
)

__all__ = ["app"]
