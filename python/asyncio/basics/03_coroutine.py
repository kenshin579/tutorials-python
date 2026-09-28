"""Coroutine 기본 예제 (async def, await)"""

import asyncio
import inspect
from collections.abc import Coroutine


async def fetch_data(url: str, delay: float = 0.1) -> dict:
    """데이터를 비동기로 가져오는 시뮬레이션"""
    await asyncio.sleep(delay)
    return {"url": url, "status": 200}


async def process_data() -> str:
    """코루틴 체이닝 - await로 다른 코루틴 호출"""
    data = await fetch_data("https://api.example.com")
    return f"Processed: {data['url']} (status={data['status']})"


def is_coroutine_demo():
    """코루틴 함수 vs 코루틴 객체 차이를 보여준다."""
    # fetch_data는 코루틴 함수
    assert inspect.iscoroutinefunction(fetch_data)

    # fetch_data()를 호출하면 코루틴 객체가 반환됨
    coro = fetch_data("test")
    assert isinstance(coro, Coroutine)

    # 코루틴 객체는 await 해야 실행됨
    # 여기서는 정리를 위해 close
    coro.close()
    return True


if __name__ == "__main__":
    result = asyncio.run(process_data())
    print(result)

    print(f"is_coroutine_demo: {is_coroutine_demo()}")
