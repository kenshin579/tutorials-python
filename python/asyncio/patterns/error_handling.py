"""
비동기 에러 핸들링 패턴
- ExceptionGroup (Python 3.11+): except* 문법으로 부분 처리
- Task 취소 전파: CancelledError 처리 모범 사례
- 에러 격리: 하나의 실패가 전체에 영향 안 주는 구조
"""

import asyncio


# ============================================================
# 1. ExceptionGroup과 except* 문법
# ============================================================
async def exception_group_basic():
    """ExceptionGroup으로 여러 예외를 한번에 처리한다."""

    async def task_a():
        await asyncio.sleep(0.1)
        raise ValueError("값이 잘못됨")

    async def task_b():
        await asyncio.sleep(0.1)
        raise TypeError("타입이 잘못됨")

    async def task_c():
        await asyncio.sleep(0.1)
        return "성공"

    caught_errors = []

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_a())
            tg.create_task(task_b())
            tg.create_task(task_c())
    except* ValueError as eg:
        for exc in eg.exceptions:
            caught_errors.append(("ValueError", str(exc)))
            print(f"  ValueError 처리: {exc}")
    except* TypeError as eg:
        for exc in eg.exceptions:
            caught_errors.append(("TypeError", str(exc)))
            print(f"  TypeError 처리: {exc}")

    return caught_errors


# ============================================================
# 2. CancelledError 처리 모범 사례
# ============================================================
async def cancellation_handling():
    """Task 취소 시 정리 작업을 수행하는 패턴."""
    cleanup_done = False

    async def long_running_task():
        nonlocal cleanup_done
        try:
            print("  작업 시작")
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            print("  취소 감지 - 정리 작업 수행 중...")
            # cleanup 로직 (DB 연결 해제, 파일 닫기 등)
            await asyncio.sleep(0.1)  # 정리 작업 시뮬레이션
            cleanup_done = True
            print("  정리 완료")
            raise  # CancelledError는 반드시 다시 raise

    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(0.1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print(f"  Task 취소 확인, cleanup 완료: {cleanup_done}")

    return cleanup_done


async def cancel_with_message():
    """Python 3.9+ 취소 메시지 전달."""

    async def worker():
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError as e:
            print(f"  취소 사유: {e}")
            raise

    task = asyncio.create_task(worker())
    await asyncio.sleep(0.1)
    task.cancel(msg="타임아웃으로 인한 취소")

    try:
        await task
    except asyncio.CancelledError:
        pass

    return True


# ============================================================
# 3. 에러 격리 - 실패가 전체에 영향 안 주는 구조
# ============================================================
async def error_isolation_with_gather():
    """return_exceptions=True로 실패를 격리한다."""
    results = await asyncio.gather(
        simulate_api_call("users", success=True),
        simulate_api_call("orders", success=False),
        simulate_api_call("products", success=True),
        return_exceptions=True,
    )

    successes = []
    failures = []
    for endpoint, result in zip(["users", "orders", "products"], results):
        if isinstance(result, Exception):
            failures.append((endpoint, str(result)))
            print(f"  [실패] {endpoint}: {result}")
        else:
            successes.append((endpoint, result))
            print(f"  [성공] {endpoint}: {result}")

    return successes, failures


async def simulate_api_call(endpoint: str, success: bool = True):
    """API 호출 시뮬레이션."""
    await asyncio.sleep(0.1)
    if not success:
        raise ConnectionError(f"{endpoint} API 연결 실패")
    return f"{endpoint} 데이터"


async def error_isolation_with_wrapper():
    """래퍼 함수로 개별 Task의 에러를 격리한다."""

    async def safe_execute(coro, default=None):
        """코루틴을 실행하고, 실패 시 기본값을 반환한다."""
        try:
            return await coro
        except Exception as e:
            print(f"  에러 격리: {e}")
            return default

    results = await asyncio.gather(
        safe_execute(simulate_api_call("users", success=True)),
        safe_execute(simulate_api_call("orders", success=False), default={}),
        safe_execute(simulate_api_call("products", success=True)),
    )
    print(f"  결과 (실패는 기본값): {results}")
    return results


# ============================================================
# 4. TaskGroup에서 부분 실패 허용 패턴
# ============================================================
async def taskgroup_partial_failure():
    """TaskGroup은 기본적으로 하나라도 실패하면 전체 취소된다.
    부분 실패를 허용하려면 내부에서 예외를 잡아야 한다."""
    results = {}

    async def safe_task(name: str, should_fail: bool):
        try:
            await asyncio.sleep(0.1)
            if should_fail:
                raise ValueError(f"{name} 실패")
            results[name] = f"{name} 성공"
        except ValueError as e:
            results[name] = f"에러: {e}"

    async with asyncio.TaskGroup() as tg:
        tg.create_task(safe_task("API-1", should_fail=False))
        tg.create_task(safe_task("API-2", should_fail=True))
        tg.create_task(safe_task("API-3", should_fail=False))

    print(f"  결과: {results}")
    return results


if __name__ == "__main__":
    print("=== 1. ExceptionGroup과 except* ===")
    asyncio.run(exception_group_basic())

    print("\n=== 2. CancelledError 처리 ===")
    asyncio.run(cancellation_handling())

    print("\n=== 3. 취소 메시지 전달 ===")
    asyncio.run(cancel_with_message())

    print("\n=== 4. 에러 격리 (gather) ===")
    asyncio.run(error_isolation_with_gather())

    print("\n=== 5. 에러 격리 (래퍼) ===")
    asyncio.run(error_isolation_with_wrapper())

    print("\n=== 6. TaskGroup 부분 실패 허용 ===")
    asyncio.run(taskgroup_partial_failure())
