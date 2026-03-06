"""
비동기 Rate Limiting 구현
- Token Bucket 알고리즘 직접 구현
- Sliding Window 방식 구현
- aiolimiter 라이브러리 활용
"""

import asyncio
import time
from collections import deque


# ============================================================
# 1. Token Bucket 알고리즘
# ============================================================
class TokenBucket:
    """Token Bucket Rate Limiter.

    일정 속도로 토큰이 채워지고, 요청 시 토큰을 소비한다.
    버킷이 비면 토큰이 채워질 때까지 대기한다.
    """

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: 초당 토큰 생성 속도
            capacity: 버킷 최대 용량
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self):
        """경과 시간에 따라 토큰을 보충한다."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

    async def acquire(self):
        """토큰 1개를 소비한다. 토큰이 없으면 대기한다."""
        async with self._lock:
            while True:
                self._refill()
                if self.tokens >= 1:
                    self.tokens -= 1
                    return
                # 토큰 1개가 생성될 때까지 대기
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        pass


async def token_bucket_example():
    """Token Bucket으로 초당 5개 요청을 제한한다."""
    bucket = TokenBucket(rate=5, capacity=5)
    timestamps = []

    async def make_request(request_id: int):
        async with bucket:
            ts = time.monotonic()
            timestamps.append(ts)
            print(f"  요청 #{request_id} 처리 (t={ts - timestamps[0]:.3f}s)")
            return request_id

    tasks = [make_request(i) for i in range(15)]
    await asyncio.gather(*tasks)
    return timestamps


# ============================================================
# 2. Sliding Window 방식
# ============================================================
class SlidingWindowLimiter:
    """Sliding Window Rate Limiter.

    최근 window_size 초 동안의 요청 수를 추적한다.
    """

    def __init__(self, max_requests: int, window_size: float = 1.0):
        """
        Args:
            max_requests: window 내 최대 요청 수
            window_size: 윈도우 크기 (초)
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self):
        """요청 허용 여부를 확인하고, 초과 시 대기한다."""
        async with self._lock:
            while True:
                now = time.monotonic()
                # 윈도우 밖의 오래된 요청 제거
                while self.requests and self.requests[0] <= now - self.window_size:
                    self.requests.popleft()

                if len(self.requests) < self.max_requests:
                    self.requests.append(now)
                    return

                # 가장 오래된 요청이 윈도우 밖으로 나갈 때까지 대기
                wait_time = self.requests[0] + self.window_size - now
                await asyncio.sleep(wait_time)

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        pass


async def sliding_window_example():
    """Sliding Window로 1초당 5개 요청을 제한한다."""
    limiter = SlidingWindowLimiter(max_requests=5, window_size=1.0)
    start = time.monotonic()

    async def make_request(request_id: int):
        async with limiter:
            elapsed = time.monotonic() - start
            print(f"  요청 #{request_id} 처리 (t={elapsed:.3f}s)")
            return request_id

    tasks = [make_request(i) for i in range(12)]
    await asyncio.gather(*tasks)
    total = time.monotonic() - start
    print(f"  총 소요 시간: {total:.2f}s")
    return total


# ============================================================
# 3. aiolimiter 라이브러리 활용
# ============================================================
async def aiolimiter_example():
    """aiolimiter의 AsyncLimiter를 사용한 rate limiting 예제."""
    try:
        from aiolimiter import AsyncLimiter
    except ImportError:
        print("  aiolimiter가 설치되지 않았습니다: pip install aiolimiter")
        return None

    # 1초당 최대 5개 요청
    limiter = AsyncLimiter(max_rate=5, time_period=1)
    start = time.monotonic()

    async def make_request(request_id: int):
        async with limiter:
            elapsed = time.monotonic() - start
            print(f"  요청 #{request_id} 처리 (t={elapsed:.3f}s)")
            return request_id

    tasks = [make_request(i) for i in range(12)]
    results = await asyncio.gather(*tasks)
    total = time.monotonic() - start
    print(f"  총 소요 시간: {total:.2f}s")
    return results


if __name__ == "__main__":
    print("=== 1. Token Bucket ===")
    asyncio.run(token_bucket_example())

    print("\n=== 2. Sliding Window ===")
    asyncio.run(sliding_window_example())

    print("\n=== 3. aiolimiter ===")
    asyncio.run(aiolimiter_example())
