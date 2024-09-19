import enum
import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import config


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        enum.Enum: sqlalchemy.Enum(enum.Enum, native_enum=False),
        typing.Literal: sqlalchemy.Enum(enum.Enum, native_enum=False),
    }


engine = create_async_engine(config.async_db_connection_uri, echo=config.db_log_queries)

async_session = async_sessionmaker(engine, expire_on_commit=False)
