from http import HTTPStatus

from apifairy import response, body
from flask import abort

from project import database
from project.models.models import Role, Permission, RolePermission
from project.schemas import role_schema, new_role_schema
from project.schemas.role import ShortRoleSchema
from . import role_api_blueprint


@role_api_blueprint.route('/create', methods=['POST'])
# @jwt_required()
@body(new_role_schema)
@response(role_schema, 200)
def create_role(kwargs: dict):
    name = kwargs['name']
    permission_list = kwargs['permissions']
    role = Role.query.filter_by(name=name).first()
    if role:
        abort(HTTPStatus.EXPECTATION_FAILED, f'role with name={name} exists')
    role = Role(name=name)

    database.session.add(role)

    for name in permission_list.split(';'):
        permission = Permission.query.filter_by(name=name).first()
        role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
        database.session.add(role_permission)

    database.session.commit()

    return role


@role_api_blueprint.route('/<role_id>', methods=['POST'])
# @jwt_required()
@body(new_role_schema)
@response(role_schema, 200)
def update_role(kwargs: dict, role_id: str):
    name = kwargs['name']
    role = Role.query.get(role_id)
    permission_list = kwargs['permissions']
    if not role:
        abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')
    if name:
        role.name = name

    if permission_list:
        for name in permission_list.split(';'):
            permission = Permission.query.filter_by(name=name).first()
            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            database.session.add(role_permission)

    database.session.commit()

    return role


@role_api_blueprint.route('/', methods=['GET'])
# @jwt_required()
@response(ShortRoleSchema(many=True), 200)
def get_all_roles():
    roles = Role.query.order_by(Role.name).all()
    if not roles:
        abort(HTTPStatus.NOT_FOUND, 'roles not found')

    return roles


@role_api_blueprint.route('/<role_id>', methods=['GET'])
# @jwt_required()
@response(role_schema, 200)
def get_role(role_id: str):
    role = Role.query.get(role_id)
    if not role:
        abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')

    return role


@role_api_blueprint.route('/<role_id>', methods=['DELETE'])
# @jwt_required()
@body(new_role_schema)
@response(role_schema, 200)
def delete_role(role_id: str):
    role = Role.query.get(role_id)
    if not role:
        abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')

    role.delete()
    database.session.commit()

    return role
