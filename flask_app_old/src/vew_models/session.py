from datetime import datetime

from flask_app_old.src.models.base import ORJSONModel


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
