import functools
import logging
import time

logger = logging.getLogger(__name__)


# --- 3.1 로깅 ---
def log_calls(func):
    """함수 호출/반환을 자동 기록하는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Calling %s(args=%s, kwargs=%s)", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.info("%s returned %s", func.__name__, result)
        return result

    return wrapper


# --- 3.2 캐싱 ---
def ttl_cache(seconds: int = 60):
    """TTL 기반 커스텀 캐시 데코레이터"""

    def decorator(func):
        cache: dict = {}

        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < seconds:
                    return result
            result = func(*args)
            cache[args] = (result, now)
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator


# --- 3.3 retry ---
def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """지수 백오프 retry 데코레이터"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


# --- 3.4 실행 시간 측정 ---
def timer(func):
    """함수 실행 시간을 측정하는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


# --- 3.5 입력값 검증 ---
def validate_types(**type_hints):
    """인자 타입 검증 데코레이터"""

    def decorator(func):
        import inspect

        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # positional args 검증
            for i, value in enumerate(args):
                if i < len(param_names):
                    name = param_names[i]
                    if name in type_hints and not isinstance(value, type_hints[name]):
                        raise TypeError(f"{name} must be {type_hints[name].__name__}, got {type(value).__name__}")
            # keyword args 검증
            for name, value in kwargs.items():
                if name in type_hints and not isinstance(value, type_hints[name]):
                    raise TypeError(f"{name} must be {type_hints[name].__name__}, got {type(value).__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
