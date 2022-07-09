from http import HTTPStatus
from typing import Optional, Union, List

from fastapi.security import OAuth2PasswordBearer
from starlette import status

from api.v1.view_models import User, Message, UserInfo, Session, TokenPair, Credentials, UnauthorizedError, \
    AccessToken, RefreshToken
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="refresh")


@router.post(
    '/login',
    responses={
        200: {'model': TokenPair},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'}
    },
    summary="Login by user credit",
    description="Provide 2 tokens - access and refresh"
)
async def login_user(credentials: Credentials) -> Union[TokenPair, UnauthorizedError]:
    pass


@router.post(
    '/logout',
    responses={
        200: {'model': Message},
    },
    summary="🔓 Logout current user."
)
async def logout_current_session_user(access_token: str = Depends(oauth2_scheme)) -> Message:
    pass


@router.post(
    '/logout_others',
    responses={
        200: {'model': Message},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Logout at all device but current"
)
async def logout_others_session_user(access_token: str = Depends(oauth2_scheme)) -> Message:
    pass


@router.post(
    '/refresh',
    responses={
        200: {'model': UserInfo},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'},
    },
    summary="🔓 Get new access & refresh token"
)
async def refresh_token_user(access_token: str = Depends(oauth2_scheme)) -> TokenPair:
    pass


@router.post(
    '/history',
    responses={
        200: {'model': List[Session]},
        401: {'model': UnauthorizedError, 'description': 'Error: Unauthorized'}
    },
    summary="🔓 Get user history"
)
async def get_user_session_history(access_token: str = Depends(oauth2_scheme), page: int = 1, page_size: int = 50) -> list[Session]:
    pass
