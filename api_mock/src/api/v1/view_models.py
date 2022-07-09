from typing import Optional

from typing import Any
from typing import Optional
from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Permission(ORJSONModel):
    id: str
    key: str
    value: str


class Role(ORJSONModel):
    id:str
    name: str
    permissions: list[Permission]


class RoleShort(ORJSONModel):
    id:str
    name: str


class User(ORJSONModel):
    id: str
    email: str
    password: str
    created: datetime
    modified: datetime


class UserInfo(ORJSONModel):
    id: str
    email: str
    password: str
    created: datetime
    modified: datetime
    role: Role


class Message(ORJSONModel):
    head: str
    body: str


class Token(ORJSONModel):
    jwt: str


class Session(ORJSONModel):
    id:str
    user_agent: str
    ip: str
    refresh_token: str
    logout: bool

