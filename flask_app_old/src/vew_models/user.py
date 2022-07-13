from flask_app_old.src.models.base import ORJSONModel
from flask_app_old.src.models.role import Role


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


class UserID(ORJSONModel):
    user_id: str


class UserDeleteConformationInfo(ORJSONModel):
    email: str
    user_id: str
