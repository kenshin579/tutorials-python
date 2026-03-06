"""ThreadPoolExecutor, ProcessPoolExecutor, submit, map, as_completed"""

import unittest
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
)


def io_task(name: str) -> str:
    time.sleep(0.05)
    return f"{name} done"


def cpu_task(n: int) -> int:
    return sum(i * i for i in range(n))


class TestThreadPoolExecutor(unittest.TestCase):
    def test_submit_and_result(self):
        """submit()으로 작업 제출, Future.result()로 결과 획득"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(io_task, "task-1")
            result = future.result(timeout=5)
        assert result == "task-1 done"

    def test_map(self):
        """map()으로 여러 작업 병렬 실행 (결과 순서 보장)"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            names = ["a", "b", "c"]
            results = list(executor.map(io_task, names))
        assert results == ["a done", "b done", "c done"]

    def test_concurrent_execution(self):
        """ThreadPoolExecutor로 I/O-bound 동시 실행"""
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(io_task, f"t-{i}") for i in range(3)]
            results = [f.result() for f in futures]
        elapsed = time.perf_counter() - start

        assert len(results) == 3
        # 3개 동시 실행이므로 ~0.05초
        assert elapsed < 0.15


class TestProcessPoolExecutor(unittest.TestCase):
    def test_submit_and_result(self):
        """ProcessPoolExecutor로 CPU-bound 작업 병렬 실행"""
        with ProcessPoolExecutor(max_workers=2) as executor:
            future = executor.submit(cpu_task, 1_000_000)
            result = future.result(timeout=10)
        assert result == sum(i * i for i in range(1_000_000))

    def test_map(self):
        """map()으로 CPU-bound 작업 분산"""
        with ProcessPoolExecutor(max_workers=2) as executor:
            inputs = [100, 200, 300]
            results = list(executor.map(cpu_task, inputs))
        expected = [cpu_task(n) for n in inputs]
        assert results == expected


class TestAsCompleted(unittest.TestCase):
    def test_as_completed(self):
        """as_completed(): 완료 순서대로 결과 처리"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(io_task, "slow"): "slow",
                executor.submit(io_task, "fast"): "fast",
            }
            completed = []
            for future in as_completed(futures):
                completed.append(future.result())

        assert len(completed) == 2
        assert set(completed) == {"slow done", "fast done"}

    def test_as_completed_with_different_durations(self):
        """완료 시간이 다른 작업을 완료 순서대로 처리"""

        def timed_task(name: str, duration: float) -> str:
            time.sleep(duration)
            return name

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(timed_task, "slow", 0.1),
                executor.submit(timed_task, "fast", 0.01),
                executor.submit(timed_task, "medium", 0.05),
            ]
            order = []
            for future in as_completed(futures):
                order.append(future.result())

        # 빠른 것부터 완료
        assert order[0] == "fast"

    def test_future_exception_handling(self):
        """Future에서 예외 처리"""

        def failing_task():
            raise ValueError("something went wrong")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(failing_task)
            with self.assertRaises(ValueError) as ctx:
                future.result()
            assert "something went wrong" in str(ctx.exception)


if __name__ == "__main__":
    unittest.main()
