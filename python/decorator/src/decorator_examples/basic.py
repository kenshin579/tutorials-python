import functools


# --- 1.1 일급 함수 & 클로저 ---
def first_class_demo():
    """함수를 인자로 전달하고 반환하는 예시"""

    def greet(name: str) -> str:
        return f"Hello, {name}!"

    def call_func(func, arg):
        return func(arg)

    return call_func(greet, "World")


def closure_demo():
    """클로저로 외부 변수를 캡처하는 예시"""

    def outer(message: str):
        def inner(name: str) -> str:
            return f"{message}, {name}!"

        return inner

    hello = outer("Hello")
    return hello("Python")  # "Hello, Python!"


# --- 1.2 함수 데코레이터 기본 ---
def simple_decorator(func):
    """기본 데코레이터 - @wraps 없이"""

    def wrapper(*args, **kwargs):
        print(f"Before: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After: {func.__name__}")
        return result

    return wrapper


# --- 1.3 functools.wraps ---
def proper_decorator(func):
    """@wraps 적용 데코레이터"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Before: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After: {func.__name__}")
        return result

    return wrapper
