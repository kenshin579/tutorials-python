"""동기 vs 비동기 비교 예제"""

import asyncio
import time


# 동기 방식 - 순차 실행
def sync_task(name: str, delay: float) -> str:
    time.sleep(delay)
    return f"{name} done"


def run_sync(tasks: list[tuple[str, float]]) -> tuple[list[str], float]:
    """동기 방식으로 작업을 순차 실행하고 결과와 소요 시간을 반환한다."""
    start = time.time()
    results = [sync_task(name, delay) for name, delay in tasks]
    elapsed = time.time() - start
    return results, elapsed


# 비동기 방식 - 동시 실행
async def async_task(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def run_async(tasks: list[tuple[str, float]]) -> tuple[list[str], float]:
    """비동기 방식으로 작업을 동시 실행하고 결과와 소요 시간을 반환한다."""
    start = time.time()
    coros = [async_task(name, delay) for name, delay in tasks]
    results = await asyncio.gather(*coros)
    elapsed = time.time() - start
    return list(results), elapsed


if __name__ == "__main__":
    tasks = [("Task-A", 1.0), ("Task-B", 1.0), ("Task-C", 1.0)]

    print("=== 동기 실행 ===")
    results, elapsed = run_sync(tasks)
    print(f"결과: {results}")
    print(f"소요 시간: {elapsed:.2f}초")

    print("\n=== 비동기 실행 ===")
    results, elapsed = asyncio.run(run_async(tasks))
    print(f"결과: {results}")
    print(f"소요 시간: {elapsed:.2f}초")
