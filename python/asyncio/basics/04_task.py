"""Task 생성 및 관리 (asyncio.create_task)"""

import asyncio


async def worker(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} completed"


async def create_tasks_demo() -> list[str]:
    """create_task로 여러 작업을 동시에 실행한다."""
    task1 = asyncio.create_task(worker("A", 0.2), name="worker-A")
    task2 = asyncio.create_task(worker("B", 0.1), name="worker-B")
    task3 = asyncio.create_task(worker("C", 0.15), name="worker-C")

    # 모든 Task 완료 대기
    results = await asyncio.gather(task1, task2, task3)
    return list(results)


async def task_status_demo() -> dict:
    """Task의 상태(done, result)를 확인한다."""
    task = asyncio.create_task(worker("status-check", 0.1))

    assert not task.done()

    result = await task

    return {
        "done": task.done(),
        "result": task.result(),
        "name": task.get_name(),
    }


async def task_cancel_demo() -> str:
    """Task 취소와 CancelledError 처리"""
    async def long_running():
        await asyncio.sleep(10)
        return "finished"

    task = asyncio.create_task(long_running())
    await asyncio.sleep(0.05)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        return "task was cancelled"

    return "unexpected"


if __name__ == "__main__":
    print(asyncio.run(create_tasks_demo()))
    print(asyncio.run(task_status_demo()))
    print(asyncio.run(task_cancel_demo()))
