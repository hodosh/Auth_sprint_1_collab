from http import HTTPStatus
from typing import Optional, Union

from api.v1.view_models import User, Message, UserInfo, Token, Role
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.put(
    '/{user_id}/assign_role',
    response_model=Role,
    summary="🔓 🎩 Assign new role to user"
)
async def user_assign_role(edited_user_id: str, role_id: str, access_token: str) -> Role:
    pass
