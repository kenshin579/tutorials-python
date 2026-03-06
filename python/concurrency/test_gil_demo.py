"""GIL 영향 시연: CPU-bound에서 threading vs multiprocessing 성능 차이"""

import unittest
import threading
import multiprocessing
import time


def cpu_bound_task(n: int) -> int:
    """CPU-bound 작업: 단순 반복 연산"""
    total = 0
    for i in range(n):
        total += i * i
    return total


def io_bound_task(duration: float) -> str:
    """I/O-bound 작업 시뮬레이션: sleep"""
    time.sleep(duration)
    return "done"


class TestGILDemo(unittest.TestCase):
    def test_cpu_bound_sequential(self):
        """CPU-bound 순차 실행 기준 시간 측정"""
        count = 5_000_000
        start = time.perf_counter()
        cpu_bound_task(count)
        cpu_bound_task(count)
        elapsed = time.perf_counter() - start
        assert elapsed > 0
        print(f"\n  [CPU-bound] sequential: {elapsed:.3f}s")

    def test_cpu_bound_threading(self):
        """CPU-bound + threading: GIL로 인해 순차 실행과 비슷하거나 더 느림"""
        count = 5_000_000
        start = time.perf_counter()
        t1 = threading.Thread(target=cpu_bound_task, args=(count,))
        t2 = threading.Thread(target=cpu_bound_task, args=(count,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        elapsed = time.perf_counter() - start
        assert elapsed > 0
        print(f"\n  [CPU-bound] threading: {elapsed:.3f}s")

    def test_cpu_bound_multiprocessing(self):
        """CPU-bound + multiprocessing: GIL 우회로 실제 병렬 실행"""
        count = 5_000_000
        start = time.perf_counter()
        with multiprocessing.Pool(2) as pool:
            pool.map(cpu_bound_task, [count, count])
        elapsed = time.perf_counter() - start
        assert elapsed > 0
        print(f"\n  [CPU-bound] multiprocessing: {elapsed:.3f}s")

    def test_io_bound_sequential(self):
        """I/O-bound 순차 실행"""
        start = time.perf_counter()
        io_bound_task(0.1)
        io_bound_task(0.1)
        elapsed = time.perf_counter() - start
        assert elapsed >= 0.2
        print(f"\n  [I/O-bound] sequential: {elapsed:.3f}s")

    def test_io_bound_threading(self):
        """I/O-bound + threading: GIL이 해제되므로 효과적"""
        start = time.perf_counter()
        t1 = threading.Thread(target=io_bound_task, args=(0.1,))
        t2 = threading.Thread(target=io_bound_task, args=(0.1,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        elapsed = time.perf_counter() - start
        # 두 스레드가 동시에 sleep하므로 ~0.1초
        assert elapsed < 0.2
        print(f"\n  [I/O-bound] threading: {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main()
