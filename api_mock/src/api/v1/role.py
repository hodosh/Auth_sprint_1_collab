from http import HTTPStatus
from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer

from api.v1.view_models import User, Message, UserInfo, Role, RoleShort, Permission, AccessToken, UnauthorizedError
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refresh")


@router.post(
    '/',
    response_model=list[RoleShort],
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Get All roles"
)
async def all_role(access_token: str = Depends(oauth2_scheme)) -> list[RoleShort]:
    pass


@router.post(
    '/{role_id}',
    response_model=Role,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Get detail about single role by ID"
)
async def get_role(role_id: str, access_token: str = Depends(oauth2_scheme)) -> Role:
    pass


@router.post(
    '/create',
    response_model=Role,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Create new role from permission list"
)
async def create_role(role_name: str, permissions: list[Permission], access_token: str = Depends(oauth2_scheme)) -> Role:
    pass


@router.put(
    '/{role_id}/update',
    response_model=Role,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Update role from permission list"
)
async def update_role(role_id: str, permission: list[Permission], access_token: str = Depends(oauth2_scheme)) -> Role:
    pass


@router.delete(
    '/{role_id}/delete',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Delete role by ID"
)
async def delete_role(role_id: str, access_token: str = Depends(oauth2_scheme)) -> Message:
    pass


