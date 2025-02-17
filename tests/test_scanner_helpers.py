from random import choice
import pytest
from json import dumps as json_dumps
from scanner_helpers import trigger_scan, get_scanned_document
from http import HTTPStatus
from uuid import uuid4

from base64 import b64encode
from os import getenv
from dotenv import load_dotenv

from tests.utils import MockResponse

load_dotenv()


SCANNER_BASIC_AUTH = b64encode(getenv("SCANNER_BASIC_AUTH").encode("utf-8"))
SCANNER_HOST = getenv("SCANNER_HOST")


@pytest.mark.asyncio
async def test_trigger_scan_success(mocker):
    expected_location = f"http://localhost:8080/scan/{uuid4()}"
    mock_response = MockResponse(
        text=json_dumps({}),
        status=HTTPStatus.CREATED,
        headers={"Location": expected_location},
    )
    mocker.patch("aiohttp.ClientSession.post", return_value=mock_response)
    actual_location = await trigger_scan()
    assert actual_location == expected_location


@pytest.mark.asyncio
async def test_trigger_scan_failed(mocker):
    mock_response = MockResponse(
        text=json_dumps("Request could not be processed"),
        status=choice([st for st in HTTPStatus if st != HTTPStatus.CREATED]),
        headers={},
    )
    mocker.patch("aiohttp.ClientSession.post", return_value=mock_response)
    actual_location = await trigger_scan()
    assert not actual_location


@pytest.mark.asyncio
async def test_get_scanned_document(mocker):
    expected_binary_data = b"Random pdf binary data"
    mock_response = MockResponse(
        text=expected_binary_data.decode(), status=HTTPStatus.OK, headers={}
    )
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_response)
    actual_text = await get_scanned_document("http://localhost:8080/scan/123")
    assert actual_text == expected_binary_data
