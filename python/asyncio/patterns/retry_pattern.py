"""
비동기 재시도 패턴
- 지수 백오프를 가진 비동기 retry 데코레이터
- jitter(무작위 지연)로 thundering herd 방지
"""

import asyncio
import functools
import random
import time


# ============================================================
# 1. 기본 재시도 패턴
# ============================================================
async def basic_retry():
    """단순한 재시도 루프."""
    attempt = 0
    max_retries = 3

    while attempt < max_retries:
        try:
            attempt += 1
            print(f"  시도 {attempt}/{max_retries}")
            # 처음 2번은 실패, 3번째 성공
            if attempt < 3:
                raise ConnectionError(f"연결 실패 (시도 {attempt})")
            return "성공!"
        except ConnectionError as e:
            print(f"  에러: {e}")
            if attempt == max_retries:
                raise
            await asyncio.sleep(0.1)

    return None


# ============================================================
# 2. 지수 백오프 재시도 데코레이터
# ============================================================
def async_retry(
    max_retries: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 10.0,
    exceptions: tuple = (Exception,),
    jitter: bool = True,
):
    """지수 백오프를 가진 비동기 retry 데코레이터.

    Args:
        max_retries: 최대 재시도 횟수
        base_delay: 기본 대기 시간 (초)
        max_delay: 최대 대기 시간 (초)
        exceptions: 재시도할 예외 타입
        jitter: 무작위 지연 추가 여부
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        print(f"  [{func.__name__}] 최대 재시도 횟수 초과")
                        raise

                    # 지수 백오프 계산
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    if jitter:
                        delay = delay * random.uniform(0.5, 1.5)

                    print(
                        f"  [{func.__name__}] 시도 {attempt}/{max_retries} "
                        f"실패: {e}, {delay:.3f}s 후 재시도"
                    )
                    await asyncio.sleep(delay)

            raise last_exception  # type: ignore

        return wrapper

    return decorator


# ============================================================
# 3. 데코레이터 사용 예제
# ============================================================
call_count = 0


@async_retry(max_retries=5, base_delay=0.1, exceptions=(ConnectionError, TimeoutError))
async def flaky_api_call(url: str):
    """불안정한 API 호출 시뮬레이션."""
    global call_count
    call_count += 1
    if call_count < 4:
        raise ConnectionError(f"연결 실패 (시도 {call_count})")
    return f"API 응답: {url}"


async def retry_decorator_example():
    """데코레이터로 재시도하는 예제."""
    global call_count
    call_count = 0
    result = await flaky_api_call("https://api.example.com/data")
    print(f"  결과: {result}")
    return result


# ============================================================
# 4. 재시도 with 콜백
# ============================================================
async def retry_with_callback():
    """재시도 시 콜백 함수를 호출하는 패턴."""
    retry_log = []

    async def on_retry(attempt: int, exception: Exception, delay: float):
        """재시도 시 호출되는 콜백."""
        retry_log.append({
            "attempt": attempt,
            "error": str(exception),
            "delay": delay,
        })
        print(f"  [콜백] 시도 {attempt}, 에러: {exception}, 대기: {delay:.3f}s")

    async def fetch_with_retry(url: str, max_retries: int = 3):
        attempt_count = 0
        for attempt in range(1, max_retries + 1):
            try:
                attempt_count += 1
                if attempt_count < 3:
                    raise TimeoutError(f"타임아웃 (시도 {attempt_count})")
                return f"데이터: {url}"
            except TimeoutError as e:
                if attempt == max_retries:
                    raise
                delay = 0.1 * (2 ** (attempt - 1))
                await on_retry(attempt, e, delay)
                await asyncio.sleep(delay)

    result = await fetch_with_retry("https://api.example.com")
    print(f"  결과: {result}")
    print(f"  재시도 로그: {retry_log}")
    return result, retry_log


# ============================================================
# 5. 지수 백오프 시각화
# ============================================================
async def visualize_backoff():
    """지수 백오프 대기 시간을 시각화한다."""
    base_delay = 0.1
    max_delay = 5.0
    delays = []

    for attempt in range(1, 8):
        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
        jittered = delay * random.uniform(0.5, 1.5)
        delays.append((attempt, delay, jittered))
        bar = "=" * int(delay * 20)
        jbar = "-" * int(jittered * 20)
        print(f"  시도 {attempt}: {delay:.3f}s {bar}")
        print(f"         jitter: {jittered:.3f}s {jbar}")

    return delays


if __name__ == "__main__":
    print("=== 1. 기본 재시도 ===")
    asyncio.run(basic_retry())

    print("\n=== 2. 재시도 데코레이터 ===")
    asyncio.run(retry_decorator_example())

    print("\n=== 3. 재시도 with 콜백 ===")
    asyncio.run(retry_with_callback())

    print("\n=== 4. 지수 백오프 시각화 ===")
    asyncio.run(visualize_backoff())
