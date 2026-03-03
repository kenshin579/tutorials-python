from myapp.main import greet


def test_greet() -> None:
    result = greet("Python")
    assert "Hello, Python!" in result
