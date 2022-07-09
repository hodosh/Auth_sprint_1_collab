from http import HTTPStatus
from typing import Optional, Union

from api.v1.view_models import User, Message, UserInfo, Role, UnauthorizedError, AccessToken, EditRole
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.put(
    '/user/assign_role',
    responses={
        200: {'model': Role},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Assign new role to user"
)
async def user_assign_role(id: EditRole, access_token: AccessToken) -> Role:
    pass
