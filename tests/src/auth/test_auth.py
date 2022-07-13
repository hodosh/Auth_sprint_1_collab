import pytest
import requests
from flask_jwt_extended import decode_token

from extensions import check_if_token_is_revoked
from flask_app.src.core import config

pytestmark = pytest.mark.asyncio


class TestAuth:

    async def test_tokens_created(self, test_client):
        url = f'{config.get_api_url()}'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "username": "test",
            "password": "test"
        }

        # test login
        with test_client.post(f'{url}/auth/login', headers=headers, json=payload) as response:
            assert response.status_code == 200
            access_token, refresh_token = response.get_json().values()
            assert access_token and refresh_token

        # test refresh
        headers['Authorization'] = f'Bearer {refresh_token}'
        with test_client.post(f'{url}/auth/refresh', headers=headers, json=payload) as response:
            assert response.status_code == 200
            (access_token,) = response.get_json().values()
            assert access_token

        # test protected
        headers['Authorization'] = f'Bearer {access_token}'
        with test_client.get(f'{url}/example/protected', headers=headers, json=payload) as response:
            assert response.status_code == 200
            assert response.get_json() == {"logged_in_as": "example_user"}

    async def test_logout_is_token_blocked(self, test_client):
        # Выполнение запроса
        url = f'{config.get_api_url()}'
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "username": "test",
            "password": "test"
        }

        # test login
        with test_client.post(f'{url}/auth/login', headers=headers, json=payload) as response:
            assert response.status_code == 200
            access_token, refresh_token = response.get_json().values()
            assert access_token and refresh_token

        # test logout
        headers['Authorization'] = f'Bearer {access_token}'
        with test_client.delete(f'{url}/auth/logout', headers=headers, json=payload) as response:
            assert response.status_code == 200
            assert response.get_json() == {"msg": "Access token revoked"}
        jwt_token = decode_token(access_token)
        assert check_if_token_is_revoked(None, jwt_token)

        # test must be logout
        headers['Authorization'] = f'Bearer {access_token}'
        with test_client.get(f'{url}/example/protected', headers=headers, json=payload) as response:
            assert response.status_code == 401
            assert response.get_json() == {'msg': 'Token has been revoked'}
