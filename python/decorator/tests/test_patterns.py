import logging
import time
from functools import lru_cache

import pytest

from decorator_examples.patterns import log_calls, retry, timer, ttl_cache, validate_types


def test_log_calls(caplog):
    @log_calls
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(1, 2)

    assert result == 3
    assert "Calling add" in caplog.text
    assert "add returned 3" in caplog.text


def test_lru_cache():
    call_count = 0

    @lru_cache(maxsize=128)
    def expensive(n):
        nonlocal call_count
        call_count += 1
        return n * 2

    assert expensive(5) == 10
    assert expensive(5) == 10  # 캐시 히트
    assert call_count == 1  # 실제 호출은 1번만


def test_ttl_cache():
    call_count = 0

    @ttl_cache(seconds=1)
    def compute(n):
        nonlocal call_count
        call_count += 1
        return n * 2

    assert compute(5) == 10
    assert compute(5) == 10  # 캐시 히트
    assert call_count == 1

    time.sleep(1.1)  # TTL 만료
    assert compute(5) == 10
    assert call_count == 2  # 재호출


def test_retry_success():
    attempt_count = 0

    @retry(max_retries=3, delay=0.01, backoff=1.0)
    def flaky():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError("not yet")
        return "ok"

    result = flaky()
    assert result == "ok"
    assert attempt_count == 3


def test_retry_all_fail():
    @retry(max_retries=2, delay=0.01, backoff=1.0)
    def always_fail():
        raise ValueError("fail")

    with pytest.raises(ValueError, match="fail"):
        always_fail()


def test_timer(capsys):
    @timer
    def slow():
        time.sleep(0.05)
        return "done"

    result = slow()
    assert result == "done"
    captured = capsys.readouterr()
    assert "slow took" in captured.out


def test_validate_types_pass():
    @validate_types(name=str, age=int)
    def greet(name, age):
        return f"{name} is {age}"

    assert greet("Alice", 30) == "Alice is 30"
    assert greet(name="Bob", age=25) == "Bob is 25"


def test_validate_types_fail_positional():
    @validate_types(name=str, age=int)
    def greet(name, age):
        return f"{name} is {age}"

    with pytest.raises(TypeError, match="name must be str"):
        greet(123, 30)


def test_validate_types_fail_keyword():
    @validate_types(age=int)
    def greet(name, age):
        return f"{name} is {age}"

    with pytest.raises(TypeError, match="age must be int"):
        greet("Alice", age="thirty")
