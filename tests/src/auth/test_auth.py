import pytest
# All test coroutines will be treated as marked.
import requests

from flask_app.src.core import config

pytestmark = pytest.mark.asyncio


class TestAuth:

    async def test_auth(self):
        # Выполнение запроса
        url = f'http://{config.FLASK_HOST}:{config.FLASK_PORT}/v1'
        session = requests.Session()
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "username": "test",
            "password": "test"
        }

        # test login
        with session.post(f'{url}/auth/login', headers=headers, json=payload) as response:
            assert response.ok
            access_token, refresh_token = response.json().values()
            assert access_token and refresh_token

        # test refresh
        headers['Authorization'] = f'Bearer {refresh_token}'
        with session.post(f'{url}/auth/refresh', headers=headers, json=payload) as response:
            assert response.ok
            (access_token,) = response.json().values()
            assert access_token

        # test protected
        headers['Authorization'] = f'Bearer {access_token}'
        with session.get(f'{url}/example/protected', headers=headers, json=payload) as response:
            assert response.ok
            (logged_in_as,) = response.json().values()
            assert logged_in_as == 'example_user'
