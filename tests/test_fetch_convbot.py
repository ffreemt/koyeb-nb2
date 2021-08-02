"""test fetch_convbot."""
import json
import pytest
import httpx
from httpx import Response
import respx

from koyeb_nb2.fetch_convbot import fetch_convbot


@pytest.mark.asyncio
async def test_fetch_convbot():
    """Test test_fetch_convbot."""
    res = await fetch_convbot("Hello")
    assert len(res) > 2


# @pytest.mark.xfail  # OK
@pytest.mark.xfail(
    raises=json.decoder.JSONDecodeError, reason="Mocking httpx.post failure"
)
@respx.mock
@pytest.mark.asyncio
async def test_fetch_convbot_with_exc():
    """Test fetch_convbot_with_exc."""
    my_route = respx.post("https://convbot-yucongo.koyeb.app/text/").mock(
        return_value=Response(204)
    )

    await fetch_convbot("Hello")

    assert my_route.called


@respx.mock
@pytest.mark.asyncio
async def test_fetch_convbot_mock_hello():
    """Test fetch_convbot_mock_hello."""
    response = Response(status_code=200, json={"result": {"resp": "Hello yourself"}})
    my_route = respx.post("https://convbot-yucongo.koyeb.app/text/").mock(
        return_value=response
    )

    res = await fetch_convbot("Hello")
    assert res == "Hello yourself"

    assert my_route.called


@respx.mock
def test_example():
    my_route = respx.get("https://example.org/").mock(return_value=Response(204))
    response = httpx.get("https://example.org/")
    assert my_route.called
    assert response.status_code == 204
    # assert 0
