"""Event Loop 기본 사용법"""

import asyncio


async def greet(name: str) -> str:
    """간단한 코루틴 예제"""
    await asyncio.sleep(0.1)
    return f"Hello, {name}!"


async def get_loop_info() -> dict:
    """현재 실행 중인 event loop 정보를 반환한다."""
    loop = asyncio.get_running_loop()
    return {
        "loop_class": type(loop).__name__,
        "is_running": loop.is_running(),
        "time": loop.time(),
    }


async def schedule_callbacks() -> list[str]:
    """event loop에 콜백을 스케줄링하는 예제"""
    results = []
    loop = asyncio.get_running_loop()

    def callback(msg):
        results.append(msg)

    loop.call_soon(callback, "first")
    loop.call_soon(callback, "second")

    # 콜백이 실행될 수 있도록 제어권 양보
    await asyncio.sleep(0)
    return results


if __name__ == "__main__":
    # asyncio.run()이 event loop 생성/실행/종료를 모두 처리
    result = asyncio.run(greet("World"))
    print(result)

    info = asyncio.run(get_loop_info())
    print(f"Loop: {info}")
