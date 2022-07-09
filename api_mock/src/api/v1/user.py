from http import HTTPStatus
from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer

from api.v1.view_models import User, Message, UserInfo, Role, Permission, \
    UnauthorizedError, TokenPair, AccessToken, UserID, UserEdit, Credentials4Register
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refresh")


@router.post(
    '/',
    response_model=list[User],
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩  Get All users"
)
async def all_user(access_token: str = Depends(oauth2_scheme)) -> list[User]:
    pass


@router.post(
    '/get_user',
    response_model=UserInfo,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Get detail about single user by ID"
)
async def get_user(user_id: UserID, access_token: str = Depends(oauth2_scheme)) -> UserInfo:
    pass


@router.post(
    '/me',
    response_model=UserInfo,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Get detail about myself"
)
async def get_myself_info(access_token: str = Depends(oauth2_scheme)) -> UserInfo:
    pass


@router.post(
    '/me/permission/{permission_id}',
    response_model=Permission,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Get single permission value"
)
async def get_user_permission(permission_id: str, access_token: str = Depends(oauth2_scheme)) -> Permission:
    pass


@router.post(
    '/register',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="Create new user"
)
async def register_user(euserInfo: Credentials4Register) -> Union[Message, TokenPair]:
    pass


@router.put(
    '/user/update',
    response_model=UserInfo,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩 Update user info"
)
async def update_user(user_info: UserEdit, user_id: UserID, access_token: str = Depends(oauth2_scheme)) -> UserInfo:
    pass


@router.delete(
    '/user/delete',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 🎩  Delete user by ID, provide email for insurance"
)
async def delete_user(user_id: UserID, access_token: str = Depends(oauth2_scheme)) -> Message:
    pass


@router.put(
    '/me/update',
    response_model=UserInfo,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Update Myself user info"
)
async def update_me_user(user_info: UserEdit, access_token: str = Depends(oauth2_scheme)) -> UserInfo:
    pass


@router.delete(
    '/me/delete',
    response_model=Message,
    responses={
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Delete Myself user info, provide email for insurance"
)
async def delete_me_user(access_token: str = Depends(oauth2_scheme)) -> Message:
    pass
