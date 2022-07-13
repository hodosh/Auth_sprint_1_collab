from http import HTTPStatus

from apifairy import authenticate, body, response, other_responses
from flask import abort

from project import database, token_auth, basic_auth
from project.models.models import (
    User,
    # UserRole,
    # Role,
    # RolePermission,
    # Permission,
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


@users_api_blueprint.route('/', methods=['POST'])
@authenticate(token_auth)
@body(new_user_schema)
@response(user_schema, 201)
def update_user(kwargs):
    # update self
    email = kwargs['email']
    password = kwargs['password']
    password_confirm = kwargs['password_confirm']

    user = token_auth.current_user()
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with email={email} not found')

    if not password:
        abort(HTTPStatus.EXPECTATION_FAILED, 'password is not specified')

    if password != password_confirm:
        abort(HTTPStatus.EXPECTATION_FAILED, 'passwords do not match')

    user.email = email
    user.set_password(password)
    database.session.commit()

    return user


@users_api_blueprint.route('/', methods=['DELETE'])
@authenticate(token_auth)
@response(user_schema, 201)
def delete_user():
    user = token_auth.current_user()
    user.delete()
    database.session.commit()

    # todo удалить сессию и токены
    return user


@users_api_blueprint.route('/', methods=['GET'])
@authenticate(token_auth)
@response(UserSchema(many=True), 201)
def get_all_users():
    users = User.query.order_by(User.email).all()
    if not users:
        abort(HTTPStatus.NOT_FOUND, f'users not found')

    return users


@users_api_blueprint.route('/<user_id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema, 201)
def get_user(user_id: str):
    user = User.query.get(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'user with user_id={user_id} not found')

    return user

# @users_api_blueprint.route('/<user_id>/permission', methods=['GET'])
# @authenticate(token_auth)
# @response(user_schema, 201)
# def get_user_permissions(user_id: str):
#     user_role = UserRole.query.filter_by(user_id=user_id).first()
#     if not user_role:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no roles')
#     role = Role.query.get(user_role.role_id)
#     role_permissions = RolePermission.filter_by(user_id=role)
#     if not role_permissions:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no role with any permissions')
#     permissions_list = [Permission(role_permission.permission_id for role_permission in role_permissions)]
#
#     return permissions_list
#
#
# @users_api_blueprint.route("/<user_id>/permission/<permission_id>", methods=["GET"])
# @authenticate(token_auth)
# @response(permission_schema, 201)
# def get_user_permissions(kwargs):
#     user_id = kwargs['user_id']
#     permission_id = kwargs['permission_id']
#     user_role = UserRole.query.filter_by(user_id=user_id).first()
#     if not user_role:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no roles')
#     role = Role.query.get(user_role.role_id)
#     role_permission = RolePermission.filter_by(user_id=role, permission_id=permission_id)
#     if not role_permission:
#         abort(HTTPStatus.NOT_FOUND, f'user with id={user_id} have no permission with id={permission_id}')
#     permission = Permission.get(role_permission.permission_id)
#
#     return permission
