from http import HTTPStatus

import pytest

from tests.functional.testdata.auth_data import login_data, login_wrong_email_data, login_wrong_password_data

pytestmark = pytest.mark.asyncio


class TestAuth:

    async def test_login_success(self, make_post_request):
        response = await make_post_request('/auth/login',
                                           data=login_data)

        assert response.status == HTTPStatus.OK
        assert list(response.body.keys()) == ['token']
        assert response.headers is not None

    async def test_login_no_data_fail(self, make_post_request):
        response = await make_post_request('/auth/login',
                                           data={})
        assert response.status == HTTPStatus.EXPECTATION_FAILED
        assert response.body['description'] == 'cannot find email and password in data!'

    async def test_login_wrong_username_fail(self, make_post_request):
        response = await make_post_request('/auth/login',
                                           data=login_wrong_email_data)
        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body['description'] == f'user with email={login_wrong_email_data["email"]} not found'

    async def test_login_wrong_password_fail(self, make_post_request):
        response = await make_post_request('/auth/login',
                                           data=login_wrong_password_data)
        assert response.status == HTTPStatus.EXPECTATION_FAILED
        assert response.body['description'] == 'password is incorrect'

    async def test_logout(self, make_post_request, actual_token):
        response = await make_post_request('/auth/logout',
                                           data=login_data)

        assert response.status == HTTPStatus.OK
        assert list(response.body.keys()) == ['token']
        assert response.headers is not None

    # async def test_tokens_created(self):
    #     url = settings.get_api_url()
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     payload = {
    #         "username": "test",
    #         "password": "test"
    #     }
    #
    #     # test login
    #     with test_client.post(f'{url}/auth/login', headers=headers, json=payload) as response:
    #         assert response.status_code == 200
    #         access_token, refresh_token = response.get_json().values()
    #         assert access_token and refresh_token
    #
    #     # test refresh
    #     headers['Authorization'] = f'Bearer {refresh_token}'
    #     with test_client.post(f'{url}/auth/refresh', headers=headers, json=payload) as response:
    #         assert response.status_code == 200
    #         (access_token,) = response.get_json().values()
    #         assert access_token
    #
    #     # test protected
    #     headers['Authorization'] = f'Bearer {access_token}'
    #     with test_client.get(f'{url}/example/protected', headers=headers, json=payload) as response:
    #         assert response.status_code == 200
    #         assert response.get_json() == {"logged_in_as": "example_user"}
    #
    # async def test_logout_is_token_blocked(self, test_client):
    #     # Выполнение запроса
    #     url = f'{settings.get_api_url()}'
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     payload = {
    #         "username": "test",
    #         "password": "test"
    #     }
    #
    #     # test login
    #     with test_client.post(f'{url}/auth/login', headers=headers, json=payload) as response:
    #         assert response.status_code == 200
    #         access_token, refresh_token = response.get_json().values()
    #         assert access_token and refresh_token
    #
    #     # test logout
    #     headers['Authorization'] = f'Bearer {access_token}'
    #     with test_client.delete(f'{url}/auth/logout', headers=headers, json=payload) as response:
    #         assert response.status_code == 200
    #         assert response.get_json() == {"msg": "Access token revoked"}
    #     jwt_token = decode_token(access_token)
    #     # assert check_if_token_is_revoked(None, jwt_token)
    #
    #     # test must be logout
    #     headers['Authorization'] = f'Bearer {access_token}'
    #     with test_client.get(f'{url}/example/protected', headers=headers, json=payload) as response:
    #         assert response.status_code == 401
    #         assert response.get_json() == {'msg': 'Token has been revoked'}
