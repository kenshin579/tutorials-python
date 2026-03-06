"""
Graceful Shutdown (signal 처리)
- loop.add_signal_handler(SIGTERM, handler) 등록
- 실행 중인 Task 목록 수집 -> 취소 -> 완료 대기
- asyncio.shield(): 특정 코루틴을 취소로부터 보호
"""

import asyncio
import signal
import sys


# ============================================================
# 1. 기본 signal handler 등록
# ============================================================
async def basic_signal_handler():
    """signal handler를 등록하고 graceful shutdown을 수행한다."""
    shutdown_event = asyncio.Event()

    def signal_handler():
        print("  SIGTERM 수신 - shutdown 시작")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    # macOS/Linux에서만 동작 (Windows는 signal.signal 사용)
    if sys.platform != "win32":
        loop.add_signal_handler(signal.SIGTERM, signal_handler)
        loop.add_signal_handler(signal.SIGINT, signal_handler)

    print("  서버 실행 중... (데모에서는 0.2초 후 자동 종료)")

    # 데모: 0.2초 후 자동 shutdown 시뮬레이션
    async def auto_shutdown():
        await asyncio.sleep(0.2)
        shutdown_event.set()

    asyncio.create_task(auto_shutdown())
    await shutdown_event.wait()
    print("  Graceful shutdown 완료")
    return True


# ============================================================
# 2. 실행 중인 Task 수집 -> 취소 -> 완료 대기
# ============================================================
async def shutdown_all_tasks():
    """실행 중인 모든 Task를 수집하고 취소한다."""
    cancelled_tasks = []

    async def worker(name: str, duration: float):
        try:
            print(f"  [{name}] 작업 시작 (예상 {duration}s)")
            await asyncio.sleep(duration)
            print(f"  [{name}] 작업 완료")
        except asyncio.CancelledError:
            print(f"  [{name}] 취소됨")
            cancelled_tasks.append(name)
            raise

    # 여러 Task 생성
    tasks = [
        asyncio.create_task(worker("DB-sync", 5.0)),
        asyncio.create_task(worker("API-poll", 3.0)),
        asyncio.create_task(worker("Cache-update", 2.0)),
    ]

    await asyncio.sleep(0.1)  # Task들이 시작될 시간

    # shutdown: 현재 Task를 제외한 모든 Task 취소
    print("  --- Shutdown 시작 ---")
    current = asyncio.current_task()
    all_tasks = [t for t in asyncio.all_tasks() if t is not current and not t.done()]
    print(f"  실행 중인 Task 수: {len(all_tasks)}")

    for task in all_tasks:
        task.cancel()

    # 모든 Task가 완료될 때까지 대기
    results = await asyncio.gather(*all_tasks, return_exceptions=True)
    print(f"  취소된 Task: {cancelled_tasks}")
    return cancelled_tasks


# ============================================================
# 3. asyncio.shield() - 특정 코루틴을 취소로부터 보호
# ============================================================
async def shield_example():
    """shield()로 중요한 작업을 취소로부터 보호한다."""
    important_completed = False

    async def important_cleanup():
        """절대 취소되면 안 되는 중요한 정리 작업."""
        nonlocal important_completed
        print("  [중요] 정리 작업 시작")
        await asyncio.sleep(0.2)
        important_completed = True
        print("  [중요] 정리 작업 완료")
        return "cleanup done"

    async def main_task():
        try:
            print("  메인 작업 실행 중...")
            # shield()로 보호된 코루틴은 외부 취소에 영향 받지 않음
            result = await asyncio.shield(important_cleanup())
            return result
        except asyncio.CancelledError:
            print("  메인 작업 취소됨 (하지만 shield 내부 작업은 계속 진행)")
            raise

    task = asyncio.create_task(main_task())
    await asyncio.sleep(0.05)

    # Task를 취소해도 shield 안의 작업은 보호됨
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    # shield 내부 작업이 완료될 시간을 줌
    await asyncio.sleep(0.3)
    print(f"  중요 작업 완료 여부: {important_completed}")
    return important_completed


# ============================================================
# 4. 타임아웃이 있는 Graceful Shutdown
# ============================================================
async def graceful_shutdown_with_timeout():
    """타임아웃 내에 종료되지 않으면 강제 취소한다."""
    graceful_results = []

    async def slow_worker(name: str, duration: float):
        try:
            print(f"  [{name}] 작업 시작")
            await asyncio.sleep(duration)
            graceful_results.append(f"{name} 완료")
            print(f"  [{name}] 작업 완료")
        except asyncio.CancelledError:
            graceful_results.append(f"{name} 취소됨")
            print(f"  [{name}] 강제 취소됨")
            raise

    tasks = [
        asyncio.create_task(slow_worker("빠른작업", 0.1)),
        asyncio.create_task(slow_worker("느린작업", 5.0)),
    ]

    # 0.3초 타임아웃으로 graceful shutdown
    shutdown_timeout = 0.3
    print(f"  Graceful shutdown (타임아웃: {shutdown_timeout}s)")

    done, pending = await asyncio.wait(tasks, timeout=shutdown_timeout)

    if pending:
        print(f"  타임아웃 초과 - {len(pending)}개 Task 강제 취소")
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)

    print(f"  결과: {graceful_results}")
    return graceful_results


if __name__ == "__main__":
    print("=== 1. 기본 signal handler ===")
    asyncio.run(basic_signal_handler())

    print("\n=== 2. 모든 Task 취소 ===")
    asyncio.run(shutdown_all_tasks())

    print("\n=== 3. asyncio.shield() ===")
    asyncio.run(shield_example())

    print("\n=== 4. 타임아웃 있는 Graceful Shutdown ===")
    asyncio.run(graceful_shutdown_with_timeout())
