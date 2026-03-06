"""타입 힌트 기본: 내장 타입, 컬렉션, 함수 시그니처"""

from typing import Any


# 1. 내장 타입
name: str = "Alice"
age: int = 30
height: float = 165.5
is_active: bool = True
data: bytes = b"hello"


# 2. 컬렉션 타입 (Python 3.9+ 소문자 제네릭)
numbers: list[int] = [1, 2, 3]
config: dict[str, Any] = {"host": "localhost", "port": 8080}
point: tuple[int, int] = (10, 20)
variable_tuple: tuple[int, ...] = (1, 2, 3, 4, 5)
tags: set[str] = {"python", "typing"}
frozen: frozenset[int] = frozenset({1, 2, 3})

# 중첩 컬렉션
matrix: list[list[int]] = [[1, 2], [3, 4]]
nested: dict[str, list[int]] = {"scores": [90, 85, 92]}


# 3. 함수 시그니처
def greet(name: str) -> str:
    """매개변수와 반환 타입"""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    return a + b


def print_message(msg: str) -> None:
    """반환값 없는 함수는 -> None"""
    print(msg)


def process_items(items: list[str], limit: int = 10) -> list[str]:
    """기본값이 있는 매개변수"""
    return items[:limit]


def get_or_default(data: dict[str, int], key: str, default: int = 0) -> int:
    return data.get(key, default)


# 4. 변수 어노테이션
count: int  # 초기값 없이 타입만 선언
count = 0


if __name__ == "__main__":
    print(f"name: {name} (type: {type(name).__name__})")
    print(f"numbers: {numbers}")
    print(f"config: {config}")
    print(f"greet: {greet('Python')}")
    print(f"add: {add(3, 5)}")
    print(f"process: {process_items(['a', 'b', 'c', 'd'], 2)}")
