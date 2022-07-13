from http import HTTPStatus
from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer
from api.v1.view_models import User, Message, UserInfo, Role, UnauthorizedError, AccessToken, EditRole
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refresh")

@router.put(
    '/{user_id}/role/{role_id}',
    responses={
        200: {'model': Role},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Assign new role to user"
)
async def user_assign_role(user_id: str, role_id: str,access_token = Depends(oauth2_scheme)) -> Role:
    pass
