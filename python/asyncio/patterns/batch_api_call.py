"""
실전 예제: API 배치 호출
- 수백 개 API를 동시에 호출하되 rate limit 준수
- Semaphore + TaskGroup 조합
"""

import asyncio
import time


# ============================================================
# 1. Semaphore + TaskGroup으로 배치 API 호출
# ============================================================
async def batch_api_call(
    api_ids: list[int],
    max_concurrent: int = 10,
    rate_per_second: int = 20,
):
    """수백 개 API를 동시에 호출하되 동시 실행 수와 초당 호출 수를 제한한다."""
    sem = asyncio.Semaphore(max_concurrent)
    results: dict[int, dict] = {}
    call_timestamps: list[float] = []

    async def call_api(api_id: int):
        async with sem:
            # rate limiting: 초당 호출 수 체크
            now = time.monotonic()
            call_timestamps.append(now)

            # 최근 1초 내 호출 수 체크
            recent = [t for t in call_timestamps if t > now - 1.0]
            if len(recent) > rate_per_second:
                wait = recent[0] + 1.0 - now
                if wait > 0:
                    await asyncio.sleep(wait)

            # API 호출 시뮬레이션
            await asyncio.sleep(0.05)
            results[api_id] = {
                "id": api_id,
                "data": f"response-{api_id}",
                "timestamp": time.monotonic(),
            }

    async with asyncio.TaskGroup() as tg:
        for api_id in api_ids:
            tg.create_task(call_api(api_id))

    return results


async def batch_example():
    """배치 API 호출 예제."""
    api_ids = list(range(50))
    start = time.monotonic()

    results = await batch_api_call(
        api_ids,
        max_concurrent=10,
        rate_per_second=20,
    )

    elapsed = time.monotonic() - start
    print(f"  총 {len(results)}개 API 호출 완료, {elapsed:.2f}s 소요")

    # 초당 호출 수 통계
    timestamps = sorted(r["timestamp"] for r in results.values())
    if len(timestamps) > 1:
        duration = timestamps[-1] - timestamps[0]
        rps = len(timestamps) / duration if duration > 0 else 0
        print(f"  평균 초당 호출 수: {rps:.1f}")

    return results


# ============================================================
# 2. 청크 단위 배치 처리
# ============================================================
async def chunked_batch(items: list, chunk_size: int = 10, delay: float = 1.0):
    """항목을 청크로 나눠 처리한다. 청크 사이에 대기 시간을 둔다."""
    all_results = []

    for i in range(0, len(items), chunk_size):
        chunk = items[i : i + chunk_size]
        chunk_num = i // chunk_size + 1
        total_chunks = (len(items) + chunk_size - 1) // chunk_size
        print(f"  청크 {chunk_num}/{total_chunks} 처리 중 ({len(chunk)}개)")

        async def process(item):
            await asyncio.sleep(0.05)
            return f"processed-{item}"

        results = await asyncio.gather(*[process(item) for item in chunk])
        all_results.extend(results)

        # 마지막 청크가 아니면 대기
        if i + chunk_size < len(items):
            print(f"  {delay}s 대기...")
            await asyncio.sleep(delay)

    print(f"  총 {len(all_results)}개 처리 완료")
    return all_results


# ============================================================
# 3. 재시도가 포함된 배치 호출
# ============================================================
async def batch_with_retry(
    api_ids: list[int],
    max_concurrent: int = 5,
    max_retries: int = 3,
):
    """실패한 API 호출은 자동으로 재시도한다."""
    sem = asyncio.Semaphore(max_concurrent)
    results: dict[int, str] = {}
    retry_counts: dict[int, int] = {}

    async def call_with_retry(api_id: int):
        async with sem:
            for attempt in range(1, max_retries + 1):
                try:
                    await asyncio.sleep(0.05)
                    # 일부 API는 처음에 실패하도록 시뮬레이션
                    if api_id % 7 == 0 and attempt < 3:
                        raise ConnectionError(f"API-{api_id} 연결 실패")
                    results[api_id] = f"success-{api_id}"
                    retry_counts[api_id] = attempt
                    return
                except ConnectionError:
                    if attempt == max_retries:
                        results[api_id] = f"failed-{api_id}"
                        retry_counts[api_id] = attempt
                    else:
                        await asyncio.sleep(0.1 * attempt)

    async with asyncio.TaskGroup() as tg:
        for api_id in api_ids:
            tg.create_task(call_with_retry(api_id))

    succeeded = sum(1 for v in results.values() if v.startswith("success"))
    failed = sum(1 for v in results.values() if v.startswith("failed"))
    retried = sum(1 for v in retry_counts.values() if v > 1)

    print(f"  성공: {succeeded}, 실패: {failed}, 재시도: {retried}")
    return results, retry_counts


if __name__ == "__main__":
    print("=== 1. 배치 API 호출 ===")
    asyncio.run(batch_example())

    print("\n=== 2. 청크 단위 배치 처리 ===")
    asyncio.run(chunked_batch(list(range(25)), chunk_size=10, delay=0.5))

    print("\n=== 3. 재시도 포함 배치 호출 ===")
    asyncio.run(batch_with_retry(list(range(30)), max_concurrent=5))
