import pytest

from http import HTTPStatus
from paperless_helpers import send_to_paperless
from random import choice

from os import getenv
from dotenv import load_dotenv
from tests.utils import MockResponse

load_dotenv()

PAPERLESS_URL = getenv("PAPERLESS_URL")
PAPERLESS_API_TOKEN = getenv("PAPERLESS_API_TOKEN")


@pytest.mark.asyncio
async def test_send_to_paperless_success(mocker):
    mock_response = MockResponse(
        text="Document uploaded", status=HTTPStatus.OK, headers={}
    )
    mocker.patch("aiohttp.ClientSession.post", return_value=mock_response)
    actual_response = await send_to_paperless("test", b"test")
    assert actual_response == await mock_response.json()


@pytest.mark.asyncio
async def test_send_to_paperless_failure(mocker):
    mock_response = MockResponse(
        text="",
        status=choice([st for st in HTTPStatus if st != HTTPStatus.OK]),
        headers={},
    )
    mocker.patch("aiohttp.ClientSession.post", return_value=mock_response)
    actual_response = await send_to_paperless("test", b"test")
    assert not actual_response
