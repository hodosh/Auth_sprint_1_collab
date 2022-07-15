# from http import HTTPStatus
#
# from apifairy import authenticate, response, body
# from flask import abort
#
# from project import token_auth, database
# from project.schemas import role_schema, new_role_schema, permission_schema
# from project.schemas.role import ShortRoleSchema
# from . import role_api_blueprint
#
#
# @role_api_blueprint.route('/', methods=['GET'])
# # @jwt_required()
# @response(ShortRoleSchema(many=True), 200)
# def get_all_roles():
#     roles = Role.query.order_by(Role.name).all()
#     if not roles:
#         abort(HTTPStatus.NOT_FOUND, 'roles not found')
#
#     return roles
#
#
# @role_api_blueprint.route('/<role_id>', methods=['GET'])
# # @jwt_required()
# @response(role_schema, 200)
# def get_role(role_id: str):
#     role = Role.query.get(role_id)
#     if not role:
#         abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')
#
#     return role
#
#
# @role_api_blueprint.route('/<role_id>', methods=['POST'])
# # @jwt_required()
# @body(new_role_schema)
# @response(role_schema, 200)
# def update_role(kwargs: dict, role_id: str):
#     name = kwargs['name']
#     role = Role.query.get(role_id)
#     if not role:
#         abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')
#     if name:
#         role.name = name
#     # todo update permission list
#     database.session.commit()
#
#     return role
#
#
# @role_api_blueprint.route('/<role_id>', methods=['DELETE'])
# # @jwt_required()
# @body(new_role_schema)
# @response(role_schema, 200)
# def delete_role(role_id: str):
#     role = Role.query.get(role_id)
#     if not role:
#         abort(HTTPStatus.NOT_FOUND, f'role with role_id={role_id} not found')
#     role.delete()
#     database.session.commit()
#
#     return role
