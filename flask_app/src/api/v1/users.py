from http import HTTPStatus
import hashlib

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required

from src.db.db import db
from src.models.models import User, UserRole, Role, RolePermission, Permission

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_users():
    users = User.query.order_by(User.email).all()
    if not users:
        return jsonify({'error': f'users not found'}), HTTPStatus.NOT_FOUND

    return jsonify(users), HTTPStatus.OK


@user_blueprint.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: str):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': f'user with id={user_id} not found'}), HTTPStatus.NOT_FOUND

    return jsonify(user), HTTPStatus.OK


@user_blueprint.route("/<user_id>/permission", methods=["GET"])
@jwt_required()
def get_user_permissions(user_id: str):
    user_role = UserRole.query.filter_by(user_id=user_id).first()
    if not user_role:
        return jsonify({'error': f'user with id={user_id} have no roles'}), HTTPStatus.NOT_FOUND
    role = Role.query.get(user_role.role_id)
    role_permissions = RolePermission.filter_by(user_id=role)
    if not role_permissions:
        return (jsonify({'error': f'user with id={user_id} have no role with any permissions'}),
                HTTPStatus.NOT_FOUND)
    permissions_list = [Permission(role_permission.permission_id for role_permission in role_permissions)]

    return jsonify(permissions_list), HTTPStatus.OK


@user_blueprint.route("/<user_id>/permission/<permission_id>", methods=["GET"])
@jwt_required()
def get_user_permissions(user_id: str, permission_id: str):
    user_role = UserRole.query.filter_by(user_id=user_id).first()
    if not user_role:
        return jsonify({'error': f'user with id={user_id} have no roles'}), HTTPStatus.NOT_FOUND
    role = Role.query.get(user_role.role_id)
    role_permission = RolePermission.filter_by(user_id=role, permission_id=permission_id)
    if not role_permission:
        return (jsonify({'error': f'user with id={user_id} have no permission with id={permission_id}'}),
                HTTPStatus.NOT_FOUND)
    permission = Permission.get(role_permission.permission_id)

    return jsonify(permission), HTTPStatus.OK


@user_blueprint.route("/register", methods=["POST"])
def register():
    args = request.args
    email = args["email"]
    password = args["password"]
    password_confirm = args["password_confirm"]
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': f'user with email={email} exists'}), HTTPStatus.EXPECTATION_FAILED

    if not password:
        return jsonify({'error': f'password is not specified'}), HTTPStatus.EXPECTATION_FAILED

    if password != password_confirm:
        return jsonify({'error': f'passwords are not match!'}), HTTPStatus.EXPECTATION_FAILED

    # todo проверить
    user = User(email=email, password=hashlib.sha256(password.encode()).hexdigest())
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': f'user with email={email} was successfully registered'}), HTTPStatus.OK


@user_blueprint.route("/<user_id>", methods=["PUT"])
def update_user():
    args = request.args
    email = args["email"]
    password = args["password"]
    password_confirm = args["password_confirm"]
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': f'user with email={email} not found'}), HTTPStatus.NOT_FOUND

    if password != password_confirm:
        return jsonify({'error': f'passwords are not match!'}), HTTPStatus.EXPECTATION_FAILED

    # todo проверить
    user.email = email
    user.password = hashlib.sha256(password.encode()).hexdigest()
    db.session.commit()

    return jsonify({'msg': f'user with email={email} was successfully registered'}), HTTPStatus.OK


@user_blueprint.route("/<user_id>", methods=["DELETE"])
def update_user():
    args = request.args
    email = args["email"]
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': f'user with email={email} not found'}), HTTPStatus.NOT_FOUND

    # todo проверить
    user.delete()
    db.session.commit()

    # todo удалить сессию и токены
    return jsonify({'msg': f'user with email={email} was deleted'}), HTTPStatus.OK
