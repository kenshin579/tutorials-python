"""ABC 기본: 추상 클래스 정의, 인스턴스 생성 불가, 일반+추상 메서드 혼합"""

import unittest
from abc import ABC, abstractmethod


# 기본 추상 클래스 정의
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

    def describe(self) -> str:
        """일반 메서드: 하위 클래스에서 그대로 사용 가능"""
        return f"I am a {self.__class__.__name__} and I say: {self.speak()}"


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


# 추상 메서드를 구현하지 않은 불완전한 클래스
class IncompleteAnimal(Animal):
    pass


class TestABCBasic(unittest.TestCase):
    def test_concrete_class_instantiation(self):
        """구체 클래스는 정상적으로 인스턴스 생성 가능"""
        dog = Dog()
        assert dog.speak() == "Woof!"

        cat = Cat()
        assert cat.speak() == "Meow!"

    def test_abstract_class_cannot_be_instantiated(self):
        """추상 클래스는 직접 인스턴스 생성 불가 → TypeError"""
        with self.assertRaises(TypeError) as ctx:
            Animal()
        assert "abstract method" in str(ctx.exception).lower()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        """추상 메서드를 구현하지 않은 하위 클래스도 인스턴스 생성 불가"""
        with self.assertRaises(TypeError):
            IncompleteAnimal()

    def test_mixed_methods(self):
        """일반 메서드와 추상 메서드 혼합 사용"""
        dog = Dog()
        assert dog.describe() == "I am a Dog and I say: Woof!"

    def test_isinstance_check(self):
        """ABC 하위 클래스는 isinstance 검사 통과"""
        dog = Dog()
        assert isinstance(dog, Animal)
        assert isinstance(dog, Dog)


if __name__ == "__main__":
    unittest.main()
