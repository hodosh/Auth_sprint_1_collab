import asyncio
import json
import typing as t
from dataclasses import dataclass

import aiohttp
import psycopg2
import pytest
from multidict import CIMultiDictProxy
from psycopg2.extras import DictCursor

from tests.functional.settings import settings
from tests.functional.testdata.auth_data import login_data

DSL = {
    'dbname': settings.db_name,
    'user': settings.db_user,
    'password': settings.db_pass,
    'host': settings.db_host,
    'port': settings.db_port,
}


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


@pytest.fixture(scope='session')
async def session():
    connector = aiohttp.TCPConnector(force_close=True)
    session = aiohttp.ClientSession(connector=connector)
    yield session
    await session.close()


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


@pytest.fixture(scope='session')
def db_connection():
    conn = psycopg2.connect(**DSL, cursor_factory=DictCursor)
    yield conn
    conn.close()


@pytest.fixture(scope='function')
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


@pytest.fixture(scope='session')
def actual_token(make_post_request):
    async def inner():
        response = await make_post_request('/auth/login',
                                           data=login_data)
        yield response.body['token']
    return inner
