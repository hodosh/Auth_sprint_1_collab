from http import HTTPStatus

import pytest

from tests.functional.testdata.users_data import (
    register_data, passwords_mismatch_data, register_base_data,
)

pytestmark = pytest.mark.asyncio


class TestUsers:

    async def test_register_success(self, make_post_request):
        response = await make_post_request('/users/register',
                                           data=register_data)

        assert response.status == HTTPStatus.CREATED
        assert response.body['disabled'] is False
        assert response.body['email'] == register_data['email']
        assert response.headers is not None

    async def test_register_no_data_fail(self, make_post_request):
        response = await make_post_request('/users/register',
                                           data={})

        assert response.status == HTTPStatus.EXPECTATION_FAILED
        assert response.body['description'] == 'cannot find email, password and password_confirm in data!'
        assert response.headers is not None

    async def test_register_passwords_mismatch_fail(self, make_post_request):
        response = await make_post_request('/users/register',
                                           data=passwords_mismatch_data)

        assert response.status == HTTPStatus.EXPECTATION_FAILED
        assert response.body['description'] == 'passwords do not match'
        assert response.headers is not None

    async def test_register_user_exists_fail(self, make_post_request, actual_super_user_token):
        await make_post_request('/users/register',
                                data=register_base_data)
        response = await make_post_request('/users/register',
                                           data=register_base_data)
        assert response.status == HTTPStatus.EXPECTATION_FAILED
        assert response.body['description'] == f'user with email={register_base_data["email"]} exists'
        assert response.headers is not None

    async def test_get_users_fail(self, make_get_request, actual_user_token):
        response = await make_get_request('/users/', headers={'Authorization': f'Bearer {actual_user_token}'})

        assert response.status == HTTPStatus.FORBIDDEN
        assert 'user with id=' in response.body['description']
        assert 'has no access for action' in response.body['description']
        assert response.headers is not None

    async def test_get_users_success(self, make_get_request, actual_super_user_token):
        response = await make_get_request('/users/', headers={'Authorization': f'Bearer {actual_super_user_token}'})

        assert response.status == HTTPStatus.OK

        assert isinstance(response.body, list)
        assert list(response.body.pop().keys()) == ['disabled', 'email', 'id']
        assert response.headers is not None
