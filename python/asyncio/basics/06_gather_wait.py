"""여러 코루틴 동시 실행 - gather, wait, as_completed"""

import asyncio


async def delayed_result(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name}({delay}s)"


# gather - 결과 순서 보장
async def gather_demo() -> list[str]:
    """gather는 인자 순서대로 결과를 반환한다."""
    results = await asyncio.gather(
        delayed_result("A", 0.3),
        delayed_result("B", 0.1),
        delayed_result("C", 0.2),
    )
    return list(results)  # ["A(0.3s)", "B(0.1s)", "C(0.2s)"] 순서 보장


async def gather_with_exception() -> list:
    """gather에서 return_exceptions=True로 예외를 결과로 수집한다."""
    async def failing_task():
        raise ValueError("task failed")

    results = await asyncio.gather(
        delayed_result("OK", 0.1),
        failing_task(),
        delayed_result("Also OK", 0.1),
        return_exceptions=True,
    )
    # 결과를 문자열로 변환 (예외 객체도 포함됨)
    return [str(r) for r in results]


# wait - 세밀한 완료 조건 제어
async def wait_first_completed() -> str:
    """FIRST_COMPLETED로 가장 먼저 완료된 Task를 처리한다."""
    tasks = [
        asyncio.create_task(delayed_result("slow", 0.3), name="slow"),
        asyncio.create_task(delayed_result("fast", 0.1), name="fast"),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    first_done = done.pop()
    result = first_done.result()

    # 남은 Task 정리
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    return result


# as_completed - 완료된 순서대로 처리
async def as_completed_demo() -> list[str]:
    """완료된 순서대로 결과를 수집한다."""
    coros = [
        delayed_result("slow", 0.3),
        delayed_result("fast", 0.1),
        delayed_result("medium", 0.2),
    ]

    results = []
    for coro in asyncio.as_completed(coros):
        result = await coro
        results.append(result)
    return results  # fast → medium → slow 순서


if __name__ == "__main__":
    print("gather:", asyncio.run(gather_demo()))
    print("gather_exc:", asyncio.run(gather_with_exception()))
    print("wait_first:", asyncio.run(wait_first_completed()))
    print("as_completed:", asyncio.run(as_completed_demo()))
