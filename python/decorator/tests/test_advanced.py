from decorator_examples.advanced import (
    CountCalls,
    add_method,
    bold,
    flexible_decorator,
    italic,
    repeat,
)


def test_repeat_decorator():
    call_count = 0

    @repeat(n=3)
    def increment():
        nonlocal call_count
        call_count += 1
        return call_count

    result = increment()
    assert call_count == 3
    assert result == 3


def test_repeat_preserves_metadata():
    @repeat(n=2)
    def my_func():
        """My docstring"""

    assert my_func.__name__ == "my_func"


def test_flexible_decorator_without_args():
    call_count = 0

    @flexible_decorator
    def increment():
        nonlocal call_count
        call_count += 1
        return call_count

    increment()
    assert call_count == 2  # default n=2


def test_flexible_decorator_with_args():
    call_count = 0

    @flexible_decorator(n=4)
    def increment():
        nonlocal call_count
        call_count += 1
        return call_count

    increment()
    assert call_count == 4


def test_count_calls():
    @CountCalls
    def say_hello():
        return "hello"

    assert say_hello.count == 0
    say_hello()
    assert say_hello.count == 1
    say_hello()
    say_hello()
    assert say_hello.count == 3


def test_count_calls_preserves_metadata():
    @CountCalls
    def my_func():
        """My docstring"""

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "My docstring"


def test_add_method():
    @add_method
    class MyClass:
        pass

    obj = MyClass()
    assert obj.greet() == "Hello from MyClass"


def test_chaining_order():
    @bold
    @italic
    def greet():
        return "hello"

    # italic이 먼저 적용되고, bold가 그 결과를 감싼다
    assert greet() == "<b><i>hello</i></b>"


def test_chaining_reversed():
    @italic
    @bold
    def greet():
        return "hello"

    assert greet() == "<i><b>hello</b></i>"
