"""Optional, Union, Literal 타입"""

from typing import Literal


# 1. Optional — None이 될 수 있는 타입
# Python 3.10+: X | None
def find_user(user_id: int) -> str | None:
    """유저를 찾지 못하면 None 반환"""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)


def greet_user(name: str | None = None) -> str:
    """Optional 매개변수"""
    if name is None:
        return "Hello, Guest!"
    return f"Hello, {name}!"


# 2. Union — 여러 타입 중 하나
# Python 3.10+: X | Y
def process_id(id_value: int | str) -> str:
    """int 또는 str을 받아 문자열로 반환"""
    if isinstance(id_value, int):
        return f"ID-{id_value:06d}"
    return id_value.upper()


def parse_value(raw: str) -> int | float | str:
    """문자열을 파싱하여 적절한 타입으로 반환"""
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


# 3. Literal — 허용 값 제한
Mode = Literal["read", "write", "append"]


def open_file(path: str, mode: Mode = "read") -> str:
    """mode를 특정 문자열 값으로 제한"""
    return f"Opening {path} in {mode} mode"


Direction = Literal["north", "south", "east", "west"]


def move(direction: Direction, steps: int = 1) -> str:
    return f"Moving {direction} {steps} steps"


# 4. Literal과 Union 결합
StatusCode = Literal[200, 201, 400, 404, 500]


def handle_response(code: StatusCode) -> str:
    if code in (200, 201):
        return "Success"
    elif code in (400, 404):
        return "Client Error"
    else:
        return "Server Error"


if __name__ == "__main__":
    # Optional
    print(f"find_user(1): {find_user(1)}")
    print(f"find_user(99): {find_user(99)}")
    print(f"greet_user(): {greet_user()}")
    print(f"greet_user('Alice'): {greet_user('Alice')}")

    # Union
    print(f"\nprocess_id(42): {process_id(42)}")
    print(f"process_id('abc'): {process_id('abc')}")
    print(f"parse_value('42'): {parse_value('42')} ({type(parse_value('42')).__name__})")
    print(f"parse_value('3.14'): {parse_value('3.14')} ({type(parse_value('3.14')).__name__})")

    # Literal
    print(f"\nopen_file('data.txt', 'write'): {open_file('data.txt', 'write')}")
    print(f"move('north', 3): {move('north', 3)}")
    print(f"handle_response(200): {handle_response(200)}")
