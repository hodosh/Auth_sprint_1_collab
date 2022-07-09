from http import HTTPStatus
from typing import Optional, Union

from api.v1.view_models import User, Message, UserInfo, Token, Role, RoleShort, Permission
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post(
    '/',
    response_model=list[RoleShort],
    summary="Get All roles"
)
async def all_role(token: str) -> list[RoleShort]:
    pass


@router.post(
    '/{role_id}',
    response_model=Role,
    summary="Get detail about single role by ID"
)
async def get_role(role_id: str, token: str) -> Role:
    pass


@router.post(
    '/create',
    response_model=Role,
    summary="Create new role from permission list   !!!TODO - make Permission list conventions"
)
async def create_role(role_id: str, token: str, permission: list[Permission]) -> Role:
    pass


@router.put(
    '/{role_id}/update',
    response_model=Role,
    summary="Update role from permission list   !!!TODO - make Permission list conventions"
)
async def update_role(role_id: str, token: str, permission: list[Permission]) -> Message:
    pass


@router.delete(
    '/{role_id}/delete',
    response_model=Role,
    summary="Delete role by ID"
)
async def delete_role(role_id: str, token: str) -> Message:
    pass


