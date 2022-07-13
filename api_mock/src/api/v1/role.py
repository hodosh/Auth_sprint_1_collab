from http import HTTPStatus
from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer

from api.v1.view_models import User, Message, UserInfo, Role, RoleShort, Permission, \
    AccessToken, UnauthorizedError, RoleID, RoleName
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refresh")


@router.get(
    '/',
    response_model=list[RoleShort],
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Get All roles"
)
async def all_role(access_token: str = Depends(oauth2_scheme)) -> list[RoleShort]:
    pass


@router.get(
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
    '/',
    response_model=Role,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Create new role"
)
async def create_role(role_name: str, access_token: str = Depends(oauth2_scheme)) -> Role:
    pass


@router.put(
    '/{role_id}/',
    response_model=Role,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Update role"
)
async def update_role(role_id: str, role_name: str, access_token: str = Depends(oauth2_scheme)) -> Role:
    pass


@router.delete(
    '/{role_id}/',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Delete role by ID"
)
async def delete_role(role_id: str, access_token: str = Depends(oauth2_scheme)) -> Message:
    pass


# ------------------------- PERMISSIONS ---------------------------

@router.post(
    '/{role_id}/permission/{permission_id}',
    response_model=Permission,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Add permission to role"
)
async def create_permission(role_id: str, permission_id:str, access_token: str = Depends(oauth2_scheme)) -> Permission:
    pass


@router.delete(
    '/{role_id}/permission/{permission_id}',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Delete permission from role"
)
async def delete_permission(role_id: str, permission_id:str,  access_token: str = Depends(oauth2_scheme)) -> Message:
    pass
