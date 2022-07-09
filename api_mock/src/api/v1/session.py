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
    summary="🔓 Logout user, by default at all device(all session)."
)
async def logout_current_session_user(aceess_token: str, logout_all_device:bool = True) -> Message:
    pass


@router.post(
    '/logout_others',
    response_model=Message,
    summary="🔓 Logout at all device but current"
)
async def logout_others_session_user(aceess_token: str) -> Message:
    pass


@router.post(
    '/update_access',
    response_model=Token,
    summary="🔓 Get new acceess token"
)
async def refresh_token_user(refresh_token: str) -> Token:
    pass


@router.post(
    '/update_refresh',
    response_model=Token,
    summary="🔓 Get new refresh token"
)
async def refresh_token_user(refresh_token: str) -> Token:
    pass



@router.post(
    '/history',
    response_model=list[Session],
    summary="🔓 Get user history"
)
async def get_user_session_history(aceess_token: str, user_id: str = None, page: int = 1, page_size: int = 50) -> list[
    Session]:
    pass
