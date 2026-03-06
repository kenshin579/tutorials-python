"""I/O-bound, CPU-bound 벤치마크 비교"""

import unittest
import threading
import multiprocessing
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ============================================================
# 공통 작업 함수
# ============================================================
def cpu_bound_work(n: int) -> int:
    """CPU-bound: 단순 합산"""
    return sum(i * i for i in range(n))


def io_bound_work(duration: float) -> str:
    """I/O-bound 시뮬레이션"""
    time.sleep(duration)
    return "done"


async def async_io_bound_work(duration: float) -> str:
    """비동기 I/O-bound 시뮬레이션"""
    await asyncio.sleep(duration)
    return "done"


# ============================================================
# I/O-bound 벤치마크
# ============================================================
class TestIOBoundBenchmark(unittest.TestCase):
    SLEEP_DURATION = 0.05
    NUM_TASKS = 5

    def test_io_sequential(self):
        """I/O-bound 순차 실행"""
        start = time.perf_counter()
        for _ in range(self.NUM_TASKS):
            io_bound_work(self.SLEEP_DURATION)
        elapsed = time.perf_counter() - start

        # 순차 실행: ~0.25초
        assert elapsed >= self.SLEEP_DURATION * self.NUM_TASKS * 0.9
        print(f"\n  [I/O] sequential:       {elapsed:.3f}s")

    def test_io_threading(self):
        """I/O-bound + threading"""
        start = time.perf_counter()
        threads = []
        for _ in range(self.NUM_TASKS):
            t = threading.Thread(target=io_bound_work, args=(self.SLEEP_DURATION,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        elapsed = time.perf_counter() - start

        # 동시 실행: ~0.05초
        assert elapsed < self.SLEEP_DURATION * self.NUM_TASKS
        print(f"\n  [I/O] threading:        {elapsed:.3f}s")

    def test_io_thread_pool_executor(self):
        """I/O-bound + ThreadPoolExecutor"""
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=self.NUM_TASKS) as executor:
            list(executor.map(io_bound_work, [self.SLEEP_DURATION] * self.NUM_TASKS))
        elapsed = time.perf_counter() - start

        assert elapsed < self.SLEEP_DURATION * self.NUM_TASKS
        print(f"\n  [I/O] ThreadPoolExec:   {elapsed:.3f}s")

    def test_io_asyncio(self):
        """I/O-bound + asyncio"""

        async def main():
            tasks = [async_io_bound_work(self.SLEEP_DURATION) for _ in range(self.NUM_TASKS)]
            return await asyncio.gather(*tasks)

        start = time.perf_counter()
        asyncio.run(main())
        elapsed = time.perf_counter() - start

        # 동시 실행: ~0.05초
        assert elapsed < self.SLEEP_DURATION * self.NUM_TASKS
        print(f"\n  [I/O] asyncio:          {elapsed:.3f}s")


# ============================================================
# CPU-bound 벤치마크
# ============================================================
class TestCPUBoundBenchmark(unittest.TestCase):
    WORK_SIZE = 2_000_000
    NUM_TASKS = 4

    def test_cpu_sequential(self):
        """CPU-bound 순차 실행"""
        start = time.perf_counter()
        for _ in range(self.NUM_TASKS):
            cpu_bound_work(self.WORK_SIZE)
        elapsed = time.perf_counter() - start

        print(f"\n  [CPU] sequential:       {elapsed:.3f}s")

    def test_cpu_threading(self):
        """CPU-bound + threading: GIL로 인해 순차와 비슷"""
        start = time.perf_counter()
        threads = []
        for _ in range(self.NUM_TASKS):
            t = threading.Thread(target=cpu_bound_work, args=(self.WORK_SIZE,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        elapsed = time.perf_counter() - start

        print(f"\n  [CPU] threading:        {elapsed:.3f}s")

    def test_cpu_multiprocessing(self):
        """CPU-bound + multiprocessing: 실제 병렬 실행"""
        start = time.perf_counter()
        with multiprocessing.Pool(self.NUM_TASKS) as pool:
            pool.map(cpu_bound_work, [self.WORK_SIZE] * self.NUM_TASKS)
        elapsed = time.perf_counter() - start

        print(f"\n  [CPU] multiprocessing:  {elapsed:.3f}s")

    def test_cpu_process_pool_executor(self):
        """CPU-bound + ProcessPoolExecutor"""
        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=self.NUM_TASKS) as executor:
            list(executor.map(cpu_bound_work, [self.WORK_SIZE] * self.NUM_TASKS))
        elapsed = time.perf_counter() - start

        print(f"\n  [CPU] ProcessPoolExec:  {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main()
