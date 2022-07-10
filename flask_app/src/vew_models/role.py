from flask_app.src.models.base import ORJSONModel


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
