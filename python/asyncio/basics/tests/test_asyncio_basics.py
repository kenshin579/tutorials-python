"""Python asyncio 기초 예제 테스트"""

import asyncio
import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod01 = importlib.import_module("01_sync_vs_async")
mod02 = importlib.import_module("02_event_loop")
mod03 = importlib.import_module("03_coroutine")
mod04 = importlib.import_module("04_task")
mod05 = importlib.import_module("05_future")
mod06 = importlib.import_module("06_gather_wait")
mod07 = importlib.import_module("07_async_syntax")
mod08 = importlib.import_module("08_error_handling")


class TestSyncVsAsync:
    def test_sync_runs_sequentially(self):
        tasks = [("A", 0.1), ("B", 0.1)]
        results, elapsed = mod01.run_sync(tasks)
        assert results == ["A done", "B done"]
        assert elapsed >= 0.2  # 순차 실행이므로 0.2초 이상

    @pytest.mark.asyncio
    async def test_async_runs_concurrently(self):
        tasks = [("A", 0.1), ("B", 0.1)]
        results, elapsed = await mod01.run_async(tasks)
        assert results == ["A done", "B done"]
        assert elapsed < 0.2  # 동시 실행이므로 0.2초 미만


class TestEventLoop:
    @pytest.mark.asyncio
    async def test_greet(self):
        result = await mod02.greet("Python")
        assert result == "Hello, Python!"

    @pytest.mark.asyncio
    async def test_get_loop_info(self):
        info = await mod02.get_loop_info()
        assert info["is_running"] is True
        assert info["time"] > 0

    @pytest.mark.asyncio
    async def test_schedule_callbacks(self):
        results = await mod02.schedule_callbacks()
        assert results == ["first", "second"]


class TestCoroutine:
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        data = await mod03.fetch_data("https://test.com", delay=0.01)
        assert data == {"url": "https://test.com", "status": 200}

    @pytest.mark.asyncio
    async def test_process_data(self):
        result = await mod03.process_data()
        assert "Processed" in result
        assert "api.example.com" in result

    def test_is_coroutine_demo(self):
        assert mod03.is_coroutine_demo() is True


class TestTask:
    @pytest.mark.asyncio
    async def test_create_tasks(self):
        results = await mod04.create_tasks_demo()
        assert "A completed" in results
        assert "B completed" in results
        assert "C completed" in results

    @pytest.mark.asyncio
    async def test_task_status(self):
        status = await mod04.task_status_demo()
        assert status["done"] is True
        assert status["result"] == "status-check completed"
        assert status["name"] is not None

    @pytest.mark.asyncio
    async def test_task_cancel(self):
        result = await mod04.task_cancel_demo()
        assert result == "task was cancelled"


class TestFuture:
    @pytest.mark.asyncio
    async def test_future_basic(self):
        result = await mod05.future_basic_demo()
        assert result == "future result"

    @pytest.mark.asyncio
    async def test_future_exception(self):
        result = await mod05.future_exception_demo()
        assert "caught" in result
        assert "something went wrong" in result

    @pytest.mark.asyncio
    async def test_task_is_future(self):
        assert await mod05.task_is_future_demo() is True


class TestGatherWait:
    @pytest.mark.asyncio
    async def test_gather_preserves_order(self):
        results = await mod06.gather_demo()
        assert results[0] == "A(0.3s)"
        assert results[1] == "B(0.1s)"
        assert results[2] == "C(0.2s)"

    @pytest.mark.asyncio
    async def test_gather_with_exception(self):
        results = await mod06.gather_with_exception()
        assert "OK" in results[0]
        assert "failed" in results[1]

    @pytest.mark.asyncio
    async def test_wait_first_completed(self):
        result = await mod06.wait_first_completed()
        assert "fast" in result

    @pytest.mark.asyncio
    async def test_as_completed_order(self):
        results = await mod06.as_completed_demo()
        assert results[0] == "fast(0.1s)"  # 가장 빨리 완료


class TestAsyncSyntax:
    @pytest.mark.asyncio
    async def test_async_for(self):
        results = await mod07.async_for_demo()
        assert results == [0, 1, 2, 3, 4]

    @pytest.mark.asyncio
    async def test_async_with(self):
        during, after = await mod07.async_with_demo()
        assert during is True
        assert after is False

    @pytest.mark.asyncio
    async def test_async_generator(self):
        results = await mod07.async_generator_demo()
        assert results == [0, 1, 2, 3, 4]

    @pytest.mark.asyncio
    async def test_async_comprehension(self):
        results = await mod07.async_comprehension_demo()
        assert results == [0, 2, 4, 6, 8]


class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_basic_error_handling(self):
        result = await mod08.basic_error_handling()
        assert "caught" in result
        assert "task1 failed" in result

    @pytest.mark.asyncio
    async def test_gather_error(self):
        results = await mod08.gather_error_demo()
        assert "ok-1 success" in results[0]
        assert "failed" in results[1]
        assert "ok-2 success" in results[2]

    @pytest.mark.asyncio
    async def test_taskgroup_success(self):
        results = await mod08.taskgroup_demo()
        assert len(results) == 3
        assert all("success" in r for r in results)

    @pytest.mark.asyncio
    async def test_taskgroup_error(self):
        result = await mod08.taskgroup_error_demo()
        assert "caught" in result
        assert "error" in result
