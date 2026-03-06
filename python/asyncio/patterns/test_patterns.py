"""
asyncio 패턴 테스트
pytest + pytest-asyncio
"""

import asyncio
import pytest

from semaphore_example import (
    basic_semaphore,
    bounded_semaphore_example,
    api_rate_limit_example,
    decorator_example,
)
from rate_limiter import (
    TokenBucket,
    SlidingWindowLimiter,
    token_bucket_example,
    sliding_window_example,
)
from gather_vs_taskgroup import (
    gather_basic,
    gather_with_return_exceptions,
    gather_without_return_exceptions,
    taskgroup_basic,
    taskgroup_error_handling,
    taskgroup_multiple_errors,
    migration_gather,
    migration_taskgroup,
)
from producer_consumer import (
    basic_queue,
    single_producer_consumer,
    multi_producer_consumer,
    queue_join_example,
    priority_queue_example,
    lifo_queue_example,
)
from error_handling import (
    exception_group_basic,
    cancellation_handling,
    cancel_with_message,
    error_isolation_with_gather,
    error_isolation_with_wrapper,
    taskgroup_partial_failure,
)
from retry_pattern import (
    basic_retry,
    retry_with_callback,
    visualize_backoff,
)
from graceful_shutdown import (
    basic_signal_handler,
    shutdown_all_tasks,
    shield_example,
    graceful_shutdown_with_timeout,
)
from async_context_manager import (
    class_based_example,
    decorator_based_example,
    nested_context_managers,
    exit_stack_example,
    exit_stack_with_callback,
)
from async_crawler import simple_crawler
from batch_api_call import batch_api_call, chunked_batch, batch_with_retry
from async_file_io import executor_file_io, bulk_file_processing, file_watcher_example


# ============================================================
# Semaphore 테스트
# ============================================================
class TestSemaphore:
    @pytest.mark.asyncio
    async def test_basic_semaphore(self):
        total = await basic_semaphore()
        # 5개를 3개씩 실행하므로 최소 0.6s (2 라운드 * 0.3s)
        assert total >= 0.5

    @pytest.mark.asyncio
    async def test_bounded_semaphore(self):
        raised = await bounded_semaphore_example()
        assert raised is True

    @pytest.mark.asyncio
    async def test_api_rate_limit(self):
        results = await api_rate_limit_example()
        assert len(results) == 20

    @pytest.mark.asyncio
    async def test_decorator(self):
        results = await decorator_example()
        assert len(results) == 6
        assert results[0] == "data-0"


# ============================================================
# Rate Limiter 테스트
# ============================================================
class TestRateLimiter:
    @pytest.mark.asyncio
    async def test_token_bucket(self):
        timestamps = await token_bucket_example()
        assert len(timestamps) == 15

    @pytest.mark.asyncio
    async def test_token_bucket_rate(self):
        bucket = TokenBucket(rate=10, capacity=2)
        # 초기 2개는 즉시 사용 가능
        await bucket.acquire()
        await bucket.acquire()
        assert bucket.tokens < 1

    @pytest.mark.asyncio
    async def test_sliding_window(self):
        total = await sliding_window_example()
        assert total > 1.0  # 12개 / 5 per sec = 최소 2초 이상

    @pytest.mark.asyncio
    async def test_sliding_window_limiter(self):
        limiter = SlidingWindowLimiter(max_requests=3, window_size=1.0)
        await limiter.acquire()
        await limiter.acquire()
        await limiter.acquire()
        assert len(limiter.requests) == 3


# ============================================================
# gather vs TaskGroup 테스트
# ============================================================
class TestGatherVsTaskGroup:
    @pytest.mark.asyncio
    async def test_gather_basic(self):
        results = await gather_basic()
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_gather_return_exceptions(self):
        results = await gather_with_return_exceptions()
        assert len(results) == 3
        assert isinstance(results[1], ValueError)

    @pytest.mark.asyncio
    async def test_gather_without_return_exceptions(self):
        result = await gather_without_return_exceptions()
        assert result is None

    @pytest.mark.asyncio
    async def test_taskgroup_basic(self):
        results = await taskgroup_basic()
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_taskgroup_error_handling(self):
        caught = await taskgroup_error_handling()
        assert caught is not None
        assert len(caught) == 1

    @pytest.mark.asyncio
    async def test_taskgroup_multiple_errors(self):
        caught = await taskgroup_multiple_errors()
        assert caught is not None
        assert len(caught) == 2

    @pytest.mark.asyncio
    async def test_migration(self):
        r1 = await migration_gather()
        r2 = await migration_taskgroup()
        assert len(r1) == 3
        assert len(r2) == 3


# ============================================================
# Producer-Consumer 테스트
# ============================================================
class TestProducerConsumer:
    @pytest.mark.asyncio
    async def test_basic_queue(self):
        results = await basic_queue()
        assert results == [f"item-{i}" for i in range(5)]

    @pytest.mark.asyncio
    async def test_single_producer_consumer(self):
        processed = await single_producer_consumer()
        assert processed == list(range(10))

    @pytest.mark.asyncio
    async def test_multi_producer_consumer(self):
        processed = await multi_producer_consumer()
        assert len(processed) == 10

    @pytest.mark.asyncio
    async def test_queue_join(self):
        results = await queue_join_example()
        assert results == list(range(9))

    @pytest.mark.asyncio
    async def test_priority_queue(self):
        results = await priority_queue_example()
        assert results[0] == (1, "높은 우선순위")
        assert results[1] == (2, "중간 우선순위")
        assert results[2] == (3, "낮은 우선순위")

    @pytest.mark.asyncio
    async def test_lifo_queue(self):
        results = await lifo_queue_example()
        assert results == ["third", "second", "first"]


# ============================================================
# Error Handling 테스트
# ============================================================
class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_exception_group(self):
        errors = await exception_group_basic()
        assert len(errors) == 2
        types = [e[0] for e in errors]
        assert "ValueError" in types
        assert "TypeError" in types

    @pytest.mark.asyncio
    async def test_cancellation_handling(self):
        cleanup_done = await cancellation_handling()
        assert cleanup_done is True

    @pytest.mark.asyncio
    async def test_cancel_with_message(self):
        result = await cancel_with_message()
        assert result is True

    @pytest.mark.asyncio
    async def test_error_isolation_gather(self):
        successes, failures = await error_isolation_with_gather()
        assert len(successes) == 2
        assert len(failures) == 1

    @pytest.mark.asyncio
    async def test_error_isolation_wrapper(self):
        results = await error_isolation_with_wrapper()
        assert len(results) == 3
        assert results[1] == {}

    @pytest.mark.asyncio
    async def test_taskgroup_partial_failure(self):
        results = await taskgroup_partial_failure()
        assert "API-1 성공" in results["API-1"]
        assert "에러" in results["API-2"]
        assert "API-3 성공" in results["API-3"]


# ============================================================
# Retry 테스트
# ============================================================
class TestRetry:
    @pytest.mark.asyncio
    async def test_basic_retry(self):
        result = await basic_retry()
        assert result == "성공!"

    @pytest.mark.asyncio
    async def test_retry_with_callback(self):
        result, retry_log = await retry_with_callback()
        assert "데이터" in result
        assert len(retry_log) == 2

    @pytest.mark.asyncio
    async def test_visualize_backoff(self):
        delays = await visualize_backoff()
        assert len(delays) == 7
        # 지수적으로 증가하는지 확인
        assert delays[1][1] > delays[0][1]


# ============================================================
# Graceful Shutdown 테스트
# ============================================================
class TestGracefulShutdown:
    @pytest.mark.asyncio
    async def test_basic_signal_handler(self):
        result = await basic_signal_handler()
        assert result is True

    @pytest.mark.asyncio
    async def test_shutdown_all_tasks(self):
        cancelled = await shutdown_all_tasks()
        assert len(cancelled) == 3

    @pytest.mark.asyncio
    async def test_shield(self):
        completed = await shield_example()
        assert completed is True

    @pytest.mark.asyncio
    async def test_graceful_shutdown_with_timeout(self):
        results = await graceful_shutdown_with_timeout()
        assert "빠른작업 완료" in results
        assert "느린작업 취소됨" in results


# ============================================================
# Context Manager 테스트
# ============================================================
class TestContextManager:
    @pytest.mark.asyncio
    async def test_class_based(self):
        result = await class_based_example()
        assert "결과" in result

    @pytest.mark.asyncio
    async def test_decorator_based(self):
        results = await decorator_based_example()
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_nested(self):
        r1, r2 = await nested_context_managers()
        assert "결과" in r1
        assert "결과" in r2

    @pytest.mark.asyncio
    async def test_exit_stack(self):
        results = await exit_stack_example()
        assert len(results) == 3

    @pytest.mark.asyncio
    async def test_exit_stack_callback(self):
        log = await exit_stack_with_callback()
        assert len(log) == 3


# ============================================================
# 실전 예제 테스트
# ============================================================
class TestPractical:
    @pytest.mark.asyncio
    async def test_simple_crawler(self):
        urls = [f"https://example.com/{i}" for i in range(5)]
        results = await simple_crawler(urls, max_concurrent=2)
        assert len(results) == 5

    @pytest.mark.asyncio
    async def test_batch_api_call(self):
        results = await batch_api_call(list(range(20)), max_concurrent=5)
        assert len(results) == 20

    @pytest.mark.asyncio
    async def test_chunked_batch(self):
        results = await chunked_batch(list(range(15)), chunk_size=5, delay=0.1)
        assert len(results) == 15

    @pytest.mark.asyncio
    async def test_batch_with_retry(self):
        results, retry_counts = await batch_with_retry(list(range(20)), max_concurrent=5)
        assert len(results) == 20

    @pytest.mark.asyncio
    async def test_executor_file_io(self):
        content = await executor_file_io()
        assert content == "executor로 작성"

    @pytest.mark.asyncio
    async def test_bulk_file_processing(self):
        results = await bulk_file_processing()
        assert len(results) == 20

    @pytest.mark.asyncio
    async def test_file_watcher(self):
        changes = await file_watcher_example()
        assert len(changes) >= 1
