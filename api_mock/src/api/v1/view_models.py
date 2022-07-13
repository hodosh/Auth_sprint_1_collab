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


class PermissionID(ORJSONModel):
    id: str


class Permission(ORJSONModel):
    id: str
    key: str
    value: str


class Role(ORJSONModel):
    id: str
    name: str
    permissions: list[Permission]


class RoleShort(ORJSONModel):
    id: str
    name: str


class RoleName(ORJSONModel):
    name: str


class RoleID(ORJSONModel):
    id: str


class EditRole(ORJSONModel):
    user_id: str
    role_id: str


class User(ORJSONModel):
    id: str
    email: str


class UserInfo(ORJSONModel):
    id: str
    email: str
    role: Role


class UserEdit(ORJSONModel):
    email: str
    old_password: str
    new_password: str
    new_password2: str


class Message(ORJSONModel):
    head: str
    body: str


class AccessToken(ORJSONModel):
    access_token: str


class RefreshToken(ORJSONModel):
    refresh_token: str


class TokenPair(AccessToken, RefreshToken):
    pass


class Session(ORJSONModel):
    id: str
    user_agent: str
    ip: str
    logout: bool
    created: datetime
    modified: datetime


class Credentials(ORJSONModel):
    email: str
    password: str


class Credentials4Register(ORJSONModel):
    email: str
    password: str
    password2: str


class UnauthorizedError(ORJSONModel):
    value: str


class UserID(ORJSONModel):
    user_id: str


class UserDeleteConformationInfo(ORJSONModel):
    email: str
    user_id: str
