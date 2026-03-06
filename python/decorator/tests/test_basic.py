from decorator_examples.basic import (
    closure_demo,
    first_class_demo,
    proper_decorator,
    simple_decorator,
)


def test_first_class_demo():
    assert first_class_demo() == "Hello, World!"


def test_closure_demo():
    assert closure_demo() == "Hello, Python!"


def test_simple_decorator(capsys):
    @simple_decorator
    def say_hello():
        return "hello"

    result = say_hello()
    assert result == "hello"
    captured = capsys.readouterr()
    assert "Before: say_hello" in captured.out
    assert "After: say_hello" in captured.out


def test_simple_decorator_loses_metadata():
    @simple_decorator
    def my_func():
        """My docstring"""

    # @wraps 없이는 메타데이터가 손실된다
    assert my_func.__name__ == "wrapper"
    assert my_func.__doc__ != "My docstring"


def test_proper_decorator_preserves_metadata():
    @proper_decorator
    def my_func():
        """My docstring"""

    # @wraps 있으면 메타데이터가 보존된다
    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "My docstring"
    assert hasattr(my_func, "__wrapped__")


def test_proper_decorator_wrapped_access():
    @proper_decorator
    def original():
        return 42

    # __wrapped__로 원본 함수에 접근 가능
    assert original.__wrapped__() == 42
