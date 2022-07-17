import typing as t
from http import HTTPStatus

import redis
from flask import abort
from flask_jwt_extended import JWTManager

from project import token_auth, database
from project.core import config
from project.models.models import (
    UserHistory,
    User,
    RolePermission,
    Permission,
)

jwt = JWTManager()

jwt_redis_blocklist = redis.StrictRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def log_activity(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        user: User = token_auth.current_user()
        user_history = UserHistory(user_id=user.id, activity=func.__name__)

        database.session.add(user_history)
        database.session.commit()
        return result

    return wrapper


def check_access(permission: t.Union[t.Any, t.List[t.Any]]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user: User = token_auth.current_user()
            role_id = user.role_id
            if not role_id:
                abort(HTTPStatus.FORBIDDEN, f'user with id={user.id} has no access for action')

            permission_list = [permission] if not isinstance(permission, list) else permission

            access = any([_check_permission(role_id, permission_single) for permission_single in permission_list])
            if not access:
                abort(HTTPStatus.FORBIDDEN, f'user with id={user.id} has no access for action')

            return func(*args, **kwargs)

        return wrapper

    return decorator


def _check_permission(role_id, permission) -> bool:
    permission_obj = Permission.query.filter_by(name=permission.value).first()
    if not permission_obj:
        return False

    role_permission = RolePermission.query.filter_by(role_id=role_id, permission_id=permission_obj.id).first()
    if not role_permission:
        return False

    return role_permission.value.lower() == 'true'
