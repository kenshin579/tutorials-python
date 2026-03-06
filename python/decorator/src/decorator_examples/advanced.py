import functools


# --- 2.1 데코레이터 팩토리 ---
def repeat(n: int = 2):
    """인자를 받는 데코레이터"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def flexible_decorator(func=None, *, n: int = 2):
    """@decorator / @decorator() 모두 지원하는 인자 선택적 데코레이터"""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = f(*args, **kwargs)
            return result

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


# --- 2.2 클래스 데코레이터 ---
class CountCalls:
    """__call__로 상태를 유지하는 데코레이터"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


def add_method(cls):
    """클래스를 대상으로 하는 데코레이터"""
    cls.greet = lambda self: f"Hello from {cls.__name__}"
    return cls


# --- 2.3 데코레이터 체이닝 ---
def bold(func):
    """텍스트를 <b> 태그로 감싸는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper


def italic(func):
    """텍스트를 <i> 태그로 감싸는 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"

    return wrapper
