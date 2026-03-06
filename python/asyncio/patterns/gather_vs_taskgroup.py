"""
asyncio.gather vs TaskGroup (Python 3.11+)
- gather: 간편하지만 부분 실패 시 나머지 Task 처리 어려움
- TaskGroup: 구조적 동시성, 자동 취소, ExceptionGroup 수집
- 마이그레이션 가이드: gather → TaskGroup 전환
"""

import asyncio


# ============================================================
# 1. asyncio.gather 기본 사용법
# ============================================================
async def fetch_data(name: str, delay: float, should_fail: bool = False):
    """데이터를 가져오는 코루틴 시뮬레이션."""
    await asyncio.sleep(delay)
    if should_fail:
        raise ValueError(f"{name} 실패!")
    return f"{name}: 데이터 로드 완료"


async def gather_basic():
    """gather로 여러 코루틴을 동시에 실행한다."""
    results = await asyncio.gather(
        fetch_data("API-1", 0.1),
        fetch_data("API-2", 0.2),
        fetch_data("API-3", 0.1),
    )
    print(f"  결과: {results}")
    return results


# ============================================================
# 2. gather의 한계 - 부분 실패 처리
# ============================================================
async def gather_with_return_exceptions():
    """return_exceptions=True로 예외를 결과에 포함시킨다."""
    results = await asyncio.gather(
        fetch_data("API-1", 0.1),
        fetch_data("API-2", 0.1, should_fail=True),
        fetch_data("API-3", 0.1),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  실패: {r}")
        else:
            print(f"  성공: {r}")
    return results


async def gather_without_return_exceptions():
    """return_exceptions=False(기본값)이면 첫 번째 예외만 전파되고
    나머지 Task는 취소되지 않고 백그라운드에서 계속 실행된다."""
    try:
        results = await asyncio.gather(
            fetch_data("API-1", 0.3),
            fetch_data("API-2", 0.1, should_fail=True),
            fetch_data("API-3", 0.3),
        )
    except ValueError as e:
        print(f"  첫 번째 예외 발생: {e}")
        print("  나머지 Task는 백그라운드에서 계속 실행 중 (리소스 누수 가능)")
        return None
    return results


# ============================================================
# 3. TaskGroup으로 구조적 동시성 구현하기 (Python 3.11+)
# ============================================================
async def taskgroup_basic():
    """TaskGroup으로 여러 코루틴을 동시에 실행한다."""
    results = []

    async with asyncio.TaskGroup() as tg:
        async def collect(name, delay):
            result = await fetch_data(name, delay)
            results.append(result)

        tg.create_task(collect("API-1", 0.1))
        tg.create_task(collect("API-2", 0.2))
        tg.create_task(collect("API-3", 0.1))

    print(f"  결과: {results}")
    return results


async def taskgroup_error_handling():
    """TaskGroup은 하나의 Task가 실패하면 나머지를 자동으로 취소한다."""
    caught = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_data("API-1", 0.3))
            tg.create_task(fetch_data("API-2", 0.1, should_fail=True))
            tg.create_task(fetch_data("API-3", 0.3))
    except* ValueError as eg:
        for exc in eg.exceptions:
            print(f"  예외 발생: {exc}")
            caught.append(exc)
        print("  나머지 Task는 자동으로 취소됨 (리소스 누수 없음)")
    return caught or None


# ============================================================
# 4. TaskGroup의 여러 예외 수집
# ============================================================
async def taskgroup_multiple_errors():
    """여러 Task가 동시에 실패하면 ExceptionGroup으로 모든 예외를 수집한다."""
    caught = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_data("API-1", 0.1, should_fail=True))
            tg.create_task(fetch_data("API-2", 0.1, should_fail=True))
            tg.create_task(fetch_data("API-3", 0.2))
    except* ValueError as eg:
        print(f"  총 {len(eg.exceptions)}개 예외 수집:")
        for exc in eg.exceptions:
            print(f"    - {exc}")
            caught.append(exc)
    return caught or None


# ============================================================
# 5. 마이그레이션 가이드: gather → TaskGroup
# ============================================================
async def migration_gather():
    """기존 gather 패턴."""
    results = await asyncio.gather(
        fetch_data("A", 0.1),
        fetch_data("B", 0.1),
        fetch_data("C", 0.1),
    )
    return results


async def migration_taskgroup():
    """TaskGroup으로 전환한 패턴."""
    results = {}

    async def run_and_store(key, delay):
        results[key] = await fetch_data(key, delay)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_and_store("A", 0.1))
        tg.create_task(run_and_store("B", 0.1))
        tg.create_task(run_and_store("C", 0.1))

    return results


if __name__ == "__main__":
    print("=== 1. gather 기본 사용법 ===")
    asyncio.run(gather_basic())

    print("\n=== 2. gather return_exceptions=True ===")
    asyncio.run(gather_with_return_exceptions())

    print("\n=== 3. gather 부분 실패 (return_exceptions=False) ===")
    asyncio.run(gather_without_return_exceptions())

    print("\n=== 4. TaskGroup 기본 사용법 ===")
    asyncio.run(taskgroup_basic())

    print("\n=== 5. TaskGroup 에러 핸들링 ===")
    asyncio.run(taskgroup_error_handling())

    print("\n=== 6. TaskGroup 여러 예외 수집 ===")
    asyncio.run(taskgroup_multiple_errors())

    print("\n=== 7. 마이그레이션: gather → TaskGroup ===")
    r1 = asyncio.run(migration_gather())
    r2 = asyncio.run(migration_taskgroup())
    print(f"  gather 결과: {r1}")
    print(f"  TaskGroup 결과: {r2}")
