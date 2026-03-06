"""Protocol 정의, 구조적 서브타이핑 동작 확인"""

import unittest
from typing import Protocol


# Protocol 정의: 메서드 시그니처만 선언
class Drawable(Protocol):
    def draw(self) -> str: ...


class Resizable(Protocol):
    def resize(self, factor: float) -> None: ...


# 명시적 상속 없이 Protocol 충족
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Square:
    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Drawing square with side {self.side}"


class Text:
    """draw() 메서드가 없으므로 Drawable을 충족하지 않음"""

    def __init__(self, content: str):
        self.content = content

    def display(self) -> str:
        return self.content


# Protocol을 타입 힌트로 활용하는 함수
def render(item: Drawable) -> str:
    return item.draw()


def render_all(items: list[Drawable]) -> list[str]:
    return [item.draw() for item in items]


# 여러 Protocol을 조합
class Widget(Drawable, Resizable, Protocol):
    pass


def process_widget(widget: Widget) -> str:
    widget.resize(2.0)
    return widget.draw()


class TestProtocolBasic(unittest.TestCase):
    def test_structural_subtyping(self):
        """명시적 상속 없이 메서드 시그니처만 맞으면 호환"""
        circle = Circle(5)
        result = render(circle)
        assert result == "Drawing circle with radius 5"

    def test_multiple_implementations(self):
        """여러 클래스가 동일한 Protocol을 충족"""
        items = [Circle(3), Square(4)]
        results = render_all(items)
        assert results == [
            "Drawing circle with radius 3",
            "Drawing square with side 4",
        ]

    def test_protocol_composition(self):
        """여러 Protocol을 조합하여 사용"""
        circle = Circle(5)
        result = process_widget(circle)
        assert result == "Drawing circle with radius 10.0"


class TestProtocolWithAttributes(unittest.TestCase):
    """Protocol에 속성 정의"""

    class Named(Protocol):
        name: str

    class Person:
        def __init__(self, name: str):
            self.name = name

    class Robot:
        def __init__(self, serial: str):
            self.name = f"Robot-{serial}"

    def greet(self, entity: "TestProtocolWithAttributes.Named") -> str:
        return f"Hello, {entity.name}!"

    def test_attribute_protocol(self):
        person = self.Person("Alice")
        robot = self.Robot("X100")
        assert self.greet(person) == "Hello, Alice!"
        assert self.greet(robot) == "Hello, Robot-X100!"


if __name__ == "__main__":
    unittest.main()
