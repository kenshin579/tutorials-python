"""Callable, Awaitable 타입"""

import asyncio
from collections.abc import Awaitable, Callable


# 1. Callable — 콜백 함수 타입
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    """함수를 인자로 받아 적용"""
    return func(a, b)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


# 2. Callable[..., ReturnType] — 임의 인자 허용
def log_call(func: Callable[..., str]) -> Callable[..., str]:
    """임의 인자를 받는 함수의 래퍼"""

    def wrapper(*args: object, **kwargs: object) -> str:
        result = func(*args, **kwargs)
        print(f"  [log] {func.__name__} → {result}")
        return result

    return wrapper


@log_call
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


# 3. 고차 함수에서 Callable 활용
def create_multiplier(factor: int) -> Callable[[int], int]:
    """Callable을 반환하는 함수"""

    def multiplier(x: int) -> int:
        return x * factor

    return multiplier


# 4. Awaitable — 비동기 함수 타입
async def fetch_data(url: str) -> str:
    """비동기 함수"""
    await asyncio.sleep(0.01)
    return f"data from {url}"


async def process_async(task: Awaitable[str]) -> str:
    """Awaitable을 인자로 받는 함수"""
    result = await task
    return result.upper()


if __name__ == "__main__":
    # Callable
    print("=== Callable ===")
    print(f"apply(add, 3, 5): {apply(add, 3, 5)}")
    print(f"apply(multiply, 3, 5): {apply(multiply, 3, 5)}")

    # 임의 인자
    print("\n=== Callable[..., str] ===")
    greet("Python")

    # 고차 함수
    print("\n=== 고차 함수 ===")
    double = create_multiplier(2)
    triple = create_multiplier(3)
    print(f"double(5): {double(5)}")
    print(f"triple(5): {triple(5)}")

    # Awaitable
    print("\n=== Awaitable ===")

    async def main() -> None:
        result = await process_async(fetch_data("https://example.com"))
        print(f"result: {result}")

    asyncio.run(main())
