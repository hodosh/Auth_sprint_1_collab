from http import HTTPStatus
from typing import Optional, Union

from api.v1.view_models import User, Message, UserInfo, Token, Role, Permission
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post(
    '/',
    response_model=list[User],
    summary="🔓 🎩  Get All users"
)
async def all_user(access_token: str) -> list[User]:
    pass


@router.post(
    '/{user_id}',
    response_model=UserInfo,
    summary="🔓 🎩 Get detail about single user by ID"
)
async def get_user(user_id: str, access_token: str) -> UserInfo:
    pass



@router.post(
    '/me',
    response_model=UserInfo,
    summary="🔓 Get detail about myself"
)
async def get_myself_info(access_token: str) -> UserInfo:
    pass

@router.post(
    '/me/permission/{permission_id}',
    response_model=Permission,
    summary="🔓 Get single permission value"
)
async def get_user_permission(permission_id: str, access_token: str) -> Permission:
    pass



@router.post(
    '/register',
    response_model=Message,
    summary="Create new user"
)
async def register_user(email: str, password: str, password2: str) -> Union[Message, Token]:
    pass


@router.put(
    '/{user_id}/update',
    response_model=UserInfo,
    summary="🔓 🎩 Update user info"
)
async def update_user(user_id: str, access_token: str, email: str = None, old_password: str = None, new_password: str = None,
                      new_password2: str = None) -> UserInfo:
    pass


@router.delete(
    '/{user_id}/delete',
    response_model=UserInfo,
    summary="🔓 🎩  Delete user by ID, provide email for insurance"
)
async def delete_user(user_id: str, access_token: str, email: str) -> UserInfo:
    pass




@router.put(
    '/me/update',
    response_model=UserInfo,
    summary="🔓 Update Myself user info"
)
async def update_me_user(access_token: str, email: str = None, old_password: str = None, new_password: str = None,
                      new_password2: str = None) -> UserInfo:
    pass


@router.delete(
    '/me/delete',
    response_model=UserInfo,
    summary="🔓 Delete Myself user info, provide email for insurance"
)
async def delete_me_user(access_token: str, email: str) -> UserInfo:
    pass