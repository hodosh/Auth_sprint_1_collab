from http import HTTPStatus

from apifairy import (
    authenticate,
    body,
    response,
    other_responses,
)
from flask import abort

from project import database, basic_auth
from project.models.models import (
    User,
    UserRole,
    Role,
    RolePermission,
    Permission, UserHistory,
)
from project.schemas import (
    new_user_schema,
    user_schema,
    UserSchema,
    token_schema,
    update_user_schema,
    new_role_schema, history_schema,
)
from . import users_api_blueprint


@users_api_blueprint.route('/get-auth-token', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
def get_auth_token():
    """Get authentication token"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    database.session.add(user)
    database.session.commit()
    return dict(token=token)


@users_api_blueprint.route('/register', methods=['POST'])
@body(new_user_schema)
@response(user_schema, 201)
def register(kwargs):
    """Create a new user"""
    email = kwargs['email']
    password = kwargs['password']
    password_confirm = kwargs['password_confirm']

    user = User.query.filter_by(email=email).first()
    if user:
        abort(HTTPStatus.EXPECTATION_FAILED, f'user with email={email} exists')

    if not password:
        abort(HTTPStatus.EXPECTATION_FAILED, 'password is not specified')

    if password != password_confirm:
        abort(HTTPStatus.EXPECTATION_FAILED, 'passwords do not match')

    new_user = User(email=email, password_plaintext=password)

    database.session.add(new_user)
    database.session.commit()

    return new_user


@users_api_blueprint.route('/<user_id>', methods=['POST'])
# @jwt_required()
@body(update_user_schema)
@response(user_schema, 201)
def update_user(kwargs, user_id: str):
    # todo обновлять может только суперюзер, тут надо сделать проверку прав
    # update self
    email = kwargs['email']
    old_password = kwargs['old_password']
    new_password = kwargs['new_password']
    new_password_confirm = kwargs['new_password_confirm']

    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    if not user.is_password_correct(old_password):
        abort(HTTPStatus.EXPECTATION_FAILED, 'old password is incorrect')

    if not new_password:
        abort(HTTPStatus.EXPECTATION_FAILED, 'new password is not specified')

    if new_password != new_password_confirm:
        abort(HTTPStatus.EXPECTATION_FAILED, 'passwords do not match')

    user.email = email
    user.set_password(new_password)
    database.session.commit()

    return user


@users_api_blueprint.route('/<user_id>', methods=['DELETE'])
# @jwt_required()
@response(user_schema, 200)
def delete_user(user_id: str):
    # todo удалять может только суперюзер, тут надо сделать проверку прав
    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    user.delete()
    database.session.commit()

    # todo удалить сессию и токены
    return dict(head='delete user', body=f'user with user_id={user_id} removed successfully')


@users_api_blueprint.route('/', methods=['GET'])
# @jwt_required()
@response(UserSchema(many=True), 200)
def get_all_users():
    users = User.query.order_by(User.email).all()
    if not users:
        abort(HTTPStatus.NOT_FOUND, 'users not found')

    return users


@users_api_blueprint.route('/<user_id>', methods=['GET'])
# @jwt_required()
@response(user_schema, 200)
def get_user(user_id: str):
    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    return user


@users_api_blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
# @jwt_required()
@response(new_role_schema, 200)
def get_user_role(user_id: str, role_id: str):
    user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
    if not user_role:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} and role_id={role_id} not found')
    role_permissions = RolePermission.query.filter_by(role_id=role_id)
    if not role_permissions:
        abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no role with any permissions')
    permissions_list = [Permission.query.get(role_permission.permission_id) for role_permission in role_permissions]
    role = Role.query.get(role_id)

    return dict(name=role.name, permissions=permissions_list)


@users_api_blueprint.route('/<user_id>/history', methods=['GET'])
# @jwt_required()
@response(history_schema, 200)
async def get_user_session_history(user_id: str):
    user_history = UserHistory.query.get(user_id)
    if not user_history:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} has no history yet!')
    return user_history
