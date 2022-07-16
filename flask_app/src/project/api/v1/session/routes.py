from http import HTTPStatus

from apifairy import authenticate, body, other_responses, response
from flask import abort

from project import database, basic_auth
from project.schemas import token_schema

from . import session_api_blueprint


@session_api_blueprint.route('/get-auth-token', methods=['POST'])
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


@session_api_blueprint.route('/refresh', methods=['POST'])
# @jwt_required()
@response(token_schema, 200)
async def refresh_token_user():
    pass
