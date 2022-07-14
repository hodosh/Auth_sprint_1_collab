from http import HTTPStatus

from apifairy import authenticate, body, response, other_responses
from flask import abort

from project import database, token_auth, basic_auth
from project.models.models import (
    User,
    # UserRole,
    # Role,
    # RolePermission,
)
from project.schemas import new_user_schema, user_schema, UserSchema, token_schema
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
@body(new_user_schema)
@response(user_schema, 201)
def update_user(user_id: str, kwargs):
    # todo обновлять может только суперюзер, тут надо сделать проверку прав
    # update self
    email = kwargs['email']
    password = kwargs['password']
    password_confirm = kwargs['password_confirm']

    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    if not password:
        abort(HTTPStatus.EXPECTATION_FAILED, 'password is not specified')

    if password != password_confirm:
        abort(HTTPStatus.EXPECTATION_FAILED, 'passwords do not match')

    user.email = email
    user.set_password(password)
    database.session.commit()

    return user


@users_api_blueprint.route('/<user_id>', methods=['DELETE'])
# @jwt_required()
@response(user_schema, 201)
def delete_user(user_id: str):
    # todo удалять может только суперюзер, тут надо сделать проверку прав
    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')
    user_name = user.email

    user.delete()
    database.session.commit()

    # todo удалить сессию и токены
    return dict(head='delete user', body=f'user "{user_name}" removed successfully')


@users_api_blueprint.route('/', methods=['GET'])
# @jwt_required()
@response(UserSchema(many=True), 201)
def get_all_users():
    users = User.query.order_by(User.email).all()
    if not users:
        abort(HTTPStatus.NOT_FOUND, 'users not found')

    return users


@users_api_blueprint.route('/<user_id>', methods=['GET'])
# @jwt_required()
@response(user_schema, 201)
def get_user(user_id: str):
    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    return user

# @users_api_blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
# @jwt_required()
# @response(new_role_schema, 201)
# def get_user_role(user_id: str, role_id: str):
#     user_role = UserRole.query.filter_by(user_id=user_id).first()
#     if not user_role:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no roles')
#     role = Role.query.get(user_role.role_id)
#     role_permissions = RolePermission.filter_by(user_id=role)
#     if not role_permissions:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no role with any permissions')
#     # permissions_list = [Permission(role_permission.name) for role_permission in role_permissions]
#
#     return dict(name=role, permissions=role_permissions)
