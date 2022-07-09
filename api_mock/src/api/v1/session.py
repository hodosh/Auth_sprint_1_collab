from http import HTTPStatus
from typing import Optional, Union

from api.v1.view_models import User, Message, UserInfo, Token, Session
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post(
    '/login',
    response_model=Union[Message, Token],
    summary="Login by user credit",
    description="Provide 2 tokens - access and refresh"
)
async def login_user(email: str, password: str) -> Union[Message, list[Token]]:
    pass


@router.post(
    '/logout',
    response_model=Message,
    summary="Logout user, by default at all device(all session)."
)
async def logout_current_session_user(token: str, logout_all_device:bool = True) -> Message:
    pass


@router.post(
    '/logout_others',
    response_model=Message,
    summary="Logout at all device but current"
)
async def logout_others_session_user(token: str) -> Message:
    pass


@router.post(
    '/refresh',
    response_model=Union[Message, Token],
    summary="Get refresh token"
)
async def refresh_token_user(token: str) -> Token:
    pass


@router.post(
    '/history',
    response_model=list[Session],
    summary="Get user history"
)
async def get_user_session_history(token: str, user_id: str = None, page: int = 1, page_size: int = 50) -> list[
    Session]:
    pass
