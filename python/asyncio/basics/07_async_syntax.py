"""비동기 문법 - async for, async with, 비동기 제네레이터"""

import asyncio


# async for - 비동기 이터레이터
class AsyncCounter:
    """비동기 이터레이터 예제"""

    def __init__(self, stop: int):
        self.stop = stop
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(0.01)
        value = self.current
        self.current += 1
        return value


async def async_for_demo() -> list[int]:
    """async for로 비동기 이터레이터를 순회한다."""
    results = []
    async for value in AsyncCounter(5):
        results.append(value)
    return results


# async with - 비동기 컨텍스트 매니저
class AsyncResource:
    """비동기 컨텍스트 매니저 예제"""

    def __init__(self, name: str):
        self.name = name
        self.connected = False

    async def __aenter__(self):
        await asyncio.sleep(0.01)
        self.connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.01)
        self.connected = False
        return False


async def async_with_demo() -> tuple[bool, bool]:
    """async with로 리소스 생명주기를 관리한다."""
    resource = AsyncResource("db")
    async with resource as r:
        during = r.connected
    after = resource.connected
    return during, after


# 비동기 제네레이터
async def async_range(start: int, stop: int, delay: float = 0.01):
    """비동기 제네레이터 - yield 사이에 비동기 작업 수행"""
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


async def async_generator_demo() -> list[int]:
    """비동기 제네레이터를 async for로 소비한다."""
    results = []
    async for value in async_range(0, 5):
        results.append(value)
    return results


# 비동기 컴프리헨션
async def async_comprehension_demo() -> list[int]:
    """비동기 컴프리헨션으로 리스트를 생성한다."""
    return [x * 2 async for x in async_range(0, 5)]


if __name__ == "__main__":
    print("async for:", asyncio.run(async_for_demo()))
    print("async with:", asyncio.run(async_with_demo()))
    print("async gen:", asyncio.run(async_generator_demo()))
    print("async comp:", asyncio.run(async_comprehension_demo()))
