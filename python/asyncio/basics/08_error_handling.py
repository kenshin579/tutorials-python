"""에러 핸들링 - 비동기 예외 전파, TaskGroup"""

import asyncio


# 기본 예외 처리
async def risky_task(name: str, should_fail: bool = False) -> str:
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError(f"{name} failed")
    return f"{name} success"


async def basic_error_handling() -> str:
    """try/except 내에서 await 예외를 처리한다."""
    try:
        result = await risky_task("task1", should_fail=True)
        return result
    except ValueError as e:
        return f"caught: {e}"


# gather에서 예외 처리
async def gather_error_demo() -> list:
    """gather에서 예외 발생 시 다른 Task 동작을 확인한다."""
    results = await asyncio.gather(
        risky_task("ok-1"),
        risky_task("fail", should_fail=True),
        risky_task("ok-2"),
        return_exceptions=True,
    )
    return [str(r) for r in results]


# TaskGroup (Python 3.11+)
async def taskgroup_demo() -> list[str]:
    """TaskGroup으로 여러 Task를 관리하고 예외를 그룹으로 처리한다."""
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(risky_task("tg-1"))
        task2 = tg.create_task(risky_task("tg-2"))
        task3 = tg.create_task(risky_task("tg-3"))

    return [task1.result(), task2.result(), task3.result()]


async def taskgroup_error_demo() -> str:
    """TaskGroup에서 예외 발생 시 모든 Task가 취소된다."""
    caught_errors = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(risky_task("ok"))
            tg.create_task(risky_task("fail", should_fail=True))
    except* ValueError as eg:
        caught_errors = [str(e) for e in eg.exceptions]

    if caught_errors:
        return f"caught {len(caught_errors)} error(s): {caught_errors}"
    return "unexpected"


if __name__ == "__main__":
    print("basic:", asyncio.run(basic_error_handling()))
    print("gather:", asyncio.run(gather_error_demo()))
    print("taskgroup:", asyncio.run(taskgroup_demo()))
    print("taskgroup_err:", asyncio.run(taskgroup_error_demo()))
