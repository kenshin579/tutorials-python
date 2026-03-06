"""
asyncio Semaphore 예제
- asyncio.Semaphore(n): 동시 실행 코루틴 수 제한
- async with sem: 패턴으로 리소스 보호
- BoundedSemaphore: release 초과 방지
- API rate limit 준수 예시
"""

import asyncio
import time


# ============================================================
# 1. 기본 Semaphore 사용법
# ============================================================
async def basic_semaphore():
    """Semaphore로 동시 실행 코루틴 수를 3개로 제한한다."""
    sem = asyncio.Semaphore(3)
    results = []

    async def worker(name: str, duration: float):
        async with sem:
            start = time.monotonic()
            print(f"  [{name}] 시작 (동시 실행 중)")
            await asyncio.sleep(duration)
            elapsed = time.monotonic() - start
            results.append((name, elapsed))
            print(f"  [{name}] 완료 ({elapsed:.2f}s)")

    tasks = [
        worker("A", 0.3),
        worker("B", 0.3),
        worker("C", 0.3),
        worker("D", 0.3),
        worker("E", 0.3),
    ]

    start = time.monotonic()
    await asyncio.gather(*tasks)
    total = time.monotonic() - start
    print(f"  총 소요 시간: {total:.2f}s (3개씩 실행되므로 ~0.6s)")
    return total


# ============================================================
# 2. BoundedSemaphore - release 초과 방지
# ============================================================
async def bounded_semaphore_example():
    """BoundedSemaphore는 acquire 없이 release하면 ValueError를 발생시킨다."""
    sem = asyncio.Semaphore(2)
    bsem = asyncio.BoundedSemaphore(2)

    # 일반 Semaphore: release 초과해도 에러 없음 (카운터만 증가)
    sem.release()
    print(f"  Semaphore 카운터: {sem._value}")  # 3이 됨

    # BoundedSemaphore: release 초과하면 ValueError
    try:
        bsem.release()
    except ValueError as e:
        print(f"  BoundedSemaphore ValueError: {e}")
        return True

    return False


# ============================================================
# 3. API Rate Limit 준수 예시
# ============================================================
async def api_rate_limit_example():
    """Semaphore로 동시 API 호출을 N개로 제한한다."""
    max_concurrent = 5
    sem = asyncio.Semaphore(max_concurrent)
    call_count = 0

    async def call_api(api_id: int):
        nonlocal call_count
        async with sem:
            call_count += 1
            current = call_count
            print(f"  API #{api_id} 호출 중 (현재 동시 호출: {current})")
            await asyncio.sleep(0.1)  # API 응답 시뮬레이션
            call_count -= 1
            return f"result-{api_id}"

    tasks = [call_api(i) for i in range(20)]
    results = await asyncio.gather(*tasks)
    print(f"  총 {len(results)}개 API 호출 완료")
    return results


# ============================================================
# 4. Semaphore를 데코레이터로 활용하기
# ============================================================
def limit_concurrency(sem: asyncio.Semaphore):
    """동시 실행을 제한하는 데코레이터."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with sem:
                return await func(*args, **kwargs)
        return wrapper
    return decorator


async def decorator_example():
    """데코레이터로 동시 실행을 제한하는 예제."""
    sem = asyncio.Semaphore(2)

    @limit_concurrency(sem)
    async def fetch_data(item_id: int):
        print(f"  fetching item {item_id}")
        await asyncio.sleep(0.2)
        return f"data-{item_id}"

    results = await asyncio.gather(*[fetch_data(i) for i in range(6)])
    print(f"  결과: {results}")
    return results


if __name__ == "__main__":
    print("=== 1. 기본 Semaphore ===")
    asyncio.run(basic_semaphore())

    print("\n=== 2. BoundedSemaphore ===")
    asyncio.run(bounded_semaphore_example())

    print("\n=== 3. API Rate Limit ===")
    asyncio.run(api_rate_limit_example())

    print("\n=== 4. Semaphore 데코레이터 ===")
    asyncio.run(decorator_example())
