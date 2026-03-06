"""async/await 기본, 간단한 비동기 I/O 예제"""

import unittest
import asyncio
import time


async def async_sleep_task(name: str, duration: float) -> str:
    await asyncio.sleep(duration)
    return f"{name} done"


async def fetch_simulated(url: str) -> dict:
    """네트워크 요청 시뮬레이션"""
    await asyncio.sleep(0.05)
    return {"url": url, "status": 200}


class TestAsyncioBasic(unittest.TestCase):
    def test_single_coroutine(self):
        """단일 코루틴 실행"""
        result = asyncio.run(async_sleep_task("task-1", 0.01))
        assert result == "task-1 done"

    def test_gather_concurrent(self):
        """gather로 여러 코루틴 동시 실행"""

        async def main():
            results = await asyncio.gather(
                async_sleep_task("a", 0.05),
                async_sleep_task("b", 0.05),
                async_sleep_task("c", 0.05),
            )
            return results

        start = time.perf_counter()
        results = asyncio.run(main())
        elapsed = time.perf_counter() - start

        assert results == ["a done", "b done", "c done"]
        # 동시 실행이므로 ~0.05초 (0.15초가 아님)
        assert elapsed < 0.15

    def test_create_task(self):
        """create_task로 동시 실행"""

        async def main():
            task1 = asyncio.create_task(async_sleep_task("x", 0.05))
            task2 = asyncio.create_task(async_sleep_task("y", 0.05))
            result1 = await task1
            result2 = await task2
            return [result1, result2]

        results = asyncio.run(main())
        assert results == ["x done", "y done"]


class TestAsyncioIOBound(unittest.TestCase):
    def test_concurrent_fetch(self):
        """여러 비동기 I/O 작업을 동시에 실행"""

        async def main():
            urls = ["https://example.com/1", "https://example.com/2", "https://example.com/3"]
            results = await asyncio.gather(*[fetch_simulated(url) for url in urls])
            return results

        start = time.perf_counter()
        results = asyncio.run(main())
        elapsed = time.perf_counter() - start

        assert len(results) == 3
        assert all(r["status"] == 200 for r in results)
        # 3개 동시 실행이므로 ~0.05초
        assert elapsed < 0.15

    def test_sequential_vs_concurrent(self):
        """순차 vs 동시 실행 시간 비교"""

        async def sequential():
            r1 = await fetch_simulated("url1")
            r2 = await fetch_simulated("url2")
            r3 = await fetch_simulated("url3")
            return [r1, r2, r3]

        async def concurrent():
            return await asyncio.gather(
                fetch_simulated("url1"),
                fetch_simulated("url2"),
                fetch_simulated("url3"),
            )

        start = time.perf_counter()
        asyncio.run(sequential())
        seq_time = time.perf_counter() - start

        start = time.perf_counter()
        asyncio.run(concurrent())
        conc_time = time.perf_counter() - start

        # 동시 실행이 순차 실행보다 빠름
        assert conc_time < seq_time


if __name__ == "__main__":
    unittest.main()
