"""@abstractmethod + @property/@classmethod/@staticmethod 조합, super() 호출 패턴"""

import unittest
from abc import ABC, abstractmethod


# @abstractmethod + @property 조합
class Shape(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self._radius**2

    @property
    def name(self) -> str:
        return "Circle"


# @abstractmethod + @classmethod 조합
class Serializable(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, data: str) -> "Serializable":
        pass


class User(Serializable):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data: str) -> "User":
        name, age = data.split(",")
        return cls(name.strip(), int(age.strip()))


# @abstractmethod + @staticmethod 조합
class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(value: str) -> bool:
        pass


class EmailValidator(Validator):
    @staticmethod
    def validate(value: str) -> bool:
        return "@" in value and "." in value


# super() 호출 패턴: 추상 메서드에 기본 구현 제공
class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> str:
        """기본 포맷 제공 — 하위 클래스에서 super()로 호출 가능"""
        return f"[LOG] {message}"


class FileLogger(Logger):
    def log(self, message: str) -> str:
        base = super().log(message)
        return f"{base} -> file"


class ConsoleLogger(Logger):
    def log(self, message: str) -> str:
        base = super().log(message)
        return f"{base} -> console"


class TestAbstractProperty(unittest.TestCase):
    def test_abstract_property(self):
        circle = Circle(5)
        assert circle.name == "Circle"
        assert abs(circle.area - 78.53975) < 0.001

    def test_abstract_property_not_implemented(self):
        with self.assertRaises(TypeError):
            Shape()


class TestAbstractClassmethod(unittest.TestCase):
    def test_from_string(self):
        user = User.from_string("Alice, 30")
        assert user.name == "Alice"
        assert user.age == 30

    def test_abstract_classmethod_not_implemented(self):
        with self.assertRaises(TypeError):
            Serializable()


class TestAbstractStaticmethod(unittest.TestCase):
    def test_validate(self):
        assert EmailValidator.validate("user@example.com") is True
        assert EmailValidator.validate("invalid") is False

    def test_abstract_staticmethod_not_implemented(self):
        with self.assertRaises(TypeError):
            Validator()


class TestSuperCall(unittest.TestCase):
    def test_super_call_pattern(self):
        """추상 메서드의 기본 구현을 super()로 활용"""
        file_logger = FileLogger()
        assert file_logger.log("hello") == "[LOG] hello -> file"

        console_logger = ConsoleLogger()
        assert console_logger.log("hello") == "[LOG] hello -> console"


if __name__ == "__main__":
    unittest.main()
