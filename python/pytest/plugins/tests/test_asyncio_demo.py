"""pytest-asyncio 데모: 비동기 테스트

실행 방법:
    pytest tests/test_asyncio_demo.py

pyproject.toml에 asyncio_mode = "auto" 설정 시 @pytest.mark.asyncio 생략 가능
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from src.async_service import AsyncService


# === 비동기 fixture ===


@pytest_asyncio.fixture
async def async_service():
    """비동기 fixture: setup + teardown 패턴"""
    service = AsyncService()
    yield service
    await service.close()


# === 기본 비동기 테스트 ===


async def test_basic_async():
    """가장 기본적인 비동기 테스트"""
    await asyncio.sleep(0.01)
    assert True


async def test_async_gather():
    """asyncio.gather를 사용한 동시 실행 테스트"""

    async def delayed_value(value, delay):
        await asyncio.sleep(delay)
        return value

    results = await asyncio.gather(
        delayed_value("a", 0.01),
        delayed_value("b", 0.01),
        delayed_value("c", 0.01),
    )
    assert results == ["a", "b", "c"]


# === AsyncService 테스트 (mock 활용) ===


async def test_fetch_json_with_mock(async_service):
    """외부 API 호출을 mock하여 테스트"""
    mock_response = {"url": "https://httpbin.org/get", "origin": "127.0.0.1"}

    with patch.object(async_service, "fetch_json", new_callable=AsyncMock, return_value=mock_response):
        result = await async_service.fetch_json("/get")
        assert result["url"] == "https://httpbin.org/get"


async def test_post_json_with_mock(async_service):
    """POST 요청을 mock하여 테스트"""
    request_data = {"name": "test", "value": 42}
    mock_response = {"json": request_data}

    with patch.object(async_service, "post_json", new_callable=AsyncMock, return_value=mock_response):
        result = await async_service.post_json("/post", data=request_data)
        assert result["json"] == request_data


# === event loop scope 테스트 ===


@pytest.mark.asyncio(loop_scope="function")
async def test_function_scope_loop():
    """function scope: 각 테스트마다 새로운 event loop 생성"""
    loop = asyncio.get_running_loop()
    assert loop is not None
