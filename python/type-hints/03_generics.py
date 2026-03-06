"""제네릭: TypeVar, Generic, ParamSpec"""

from typing import Generic, TypeVar


# 1. TypeVar — 제네릭 함수
T = TypeVar("T")


def first(items: list[T]) -> T:
    """리스트의 첫 번째 요소 반환 — 타입 보존"""
    return items[0]


def identity(value: T) -> T:
    """입력 타입 그대로 반환"""
    return value


K = TypeVar("K")
V = TypeVar("V")


def get_value(d: dict[K, V], key: K, default: V) -> V:
    """딕셔너리에서 값 조회 — 키/값 타입 보존"""
    return d.get(key, default)


# 2. TypeVar with bound — 상한 제약
class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


A = TypeVar("A", bound=Animal)


def make_speak(animal: A) -> str:
    """Animal 또는 그 하위 클래스만 허용"""
    return animal.speak()


# 3. Generic 클래스
class Stack(Generic[T]):
    """제네릭 스택 자료구조"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Pair(Generic[K, V]):
    """두 타입 파라미터를 가진 제네릭 클래스"""

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"Pair({self.key!r}, {self.value!r})"


if __name__ == "__main__":
    # TypeVar
    print(f"first([1,2,3]): {first([1, 2, 3])}")
    print(f"first(['a','b']): {first(['a', 'b'])}")
    print(f"identity(42): {identity(42)}")

    # bound
    print(f"\nmake_speak(Dog()): {make_speak(Dog())}")
    print(f"make_speak(Cat()): {make_speak(Cat())}")

    # Generic class
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"\nStack: peek={stack.peek()}, pop={stack.pop()}, len={len(stack)}")

    pair = Pair("name", "Alice")
    print(f"Pair: {pair}")
