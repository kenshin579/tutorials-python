"""Future 객체 - 저수준 API"""

import asyncio


async def future_basic_demo() -> str:
    """Future 객체의 기본 사용법을 보여준다."""
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    # 0.1초 후 결과를 설정하는 콜백
    async def set_result_later():
        await asyncio.sleep(0.1)
        future.set_result("future result")

    asyncio.create_task(set_result_later())

    # future가 완료될 때까지 대기
    result = await future
    return result


async def future_exception_demo() -> str:
    """Future에 예외를 설정하는 예제"""
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    async def set_exception_later():
        await asyncio.sleep(0.1)
        future.set_exception(ValueError("something went wrong"))

    asyncio.create_task(set_exception_later())

    try:
        await future
    except ValueError as e:
        return f"caught: {e}"

    return "unexpected"


async def task_is_future_demo() -> bool:
    """Task는 Future의 서브클래스이다."""
    async def dummy():
        return 42

    task = asyncio.create_task(dummy())
    is_future = isinstance(task, asyncio.Future)
    await task
    return is_future


if __name__ == "__main__":
    print(asyncio.run(future_basic_demo()))
    print(asyncio.run(future_exception_demo()))
    print(asyncio.run(task_is_future_demo()))
