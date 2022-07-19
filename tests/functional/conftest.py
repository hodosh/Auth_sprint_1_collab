import asyncio
import json
import typing as t
from dataclasses import dataclass

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from tests.functional.settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: t.Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.api_host.rstrip("/")}:{settings.api_port}/api/v1{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_put_request(session):
    async def inner(method: str, params: t.Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.api_host.rstrip("/")}:{settings.api_port}/api/v1{method}'
        async with session.put(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope='function')
def make_post_request():
    async def inner(method: str, data: t.Optional[dict] = None, headers: t.Optional[dict] = None) -> HTTPResponse:
        headers = headers or {}
        data = data or {}
        if data:
            headers = {'Content-Type': 'application/json'}
        url = f'{settings.api_host.rstrip("/")}:{settings.api_port}/api/v1{method}'
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=json.dumps(data)) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner


@pytest.fixture
def make_delete_request(session):
    async def inner(method: str, params: t.Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.api_host.rstrip("/")}:{settings.api_port}/api/v1{method}'
        async with session.delete(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope='function')
def data_loader(es_client):
    async def inner(index_name: str, data: t.Union[t.List[t.Dict], t.Dict]):
        res_data = ''

        if not isinstance(data, list):
            data = [data]

        for item in data:
            entity_id = item['id']
            load = {'index': {'_index': index_name, '_id': entity_id}}
            res_data += f'{json.dumps(load)}\n{json.dumps(item)}\n'

        res = await es_client.bulk(res_data)

        if res['errors'] is True:
            raise RuntimeError(f'Something went wrong: {res}')
        # wait for data appears
        await asyncio.sleep(0.1)

    return inner
