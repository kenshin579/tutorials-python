"""상속과 데이터클래스: 필드 순서, 기본값 문제, slots=True"""

import sys
from dataclasses import dataclass, field


# 1. 기본 상속 — 부모/자식 필드 순서
@dataclass
class Animal:
    name: str
    sound: str = "..."


@dataclass
class Dog(Animal):
    breed: str = "Unknown"

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"


# 2. 기본값 문제 — 부모에 기본값 있으면 자식에 필수 필드 불가
#    해결법: kw_only 사용
@dataclass
class Base:
    name: str
    value: int = 0


# 아래는 TypeError 발생:
# @dataclass
# class Child(Base):
#     required_field: str  # Error! 기본값 없는 필드가 기본값 있는 필드 뒤에 올 수 없음

# 해결법 1: kw_only=True
@dataclass(kw_only=True)
class ChildKwOnly(Base):
    required_field: str


# 해결법 2: 개별 필드에 kw_only
@dataclass
class ChildFieldKwOnly(Base):
    required_field: str = field(kw_only=True)


# 3. slots=True (Python 3.10+) — 메모리 최적화
@dataclass
class RegularPoint:
    x: float
    y: float
    z: float


@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float
    z: float


if __name__ == "__main__":
    # 기본 상속
    print("=== 기본 상속 ===")
    dog = Dog(name="Buddy", sound="Woof!", breed="Golden")
    print(f"dog: {dog}")
    print(f"speak: {dog.speak()}")

    # kw_only 해결
    print("\n=== kw_only 해결 ===")
    child1 = ChildKwOnly(name="test", value=1, required_field="필수값")
    print(f"child1: {child1}")

    child2 = ChildFieldKwOnly("test", 1, required_field="필수값")
    print(f"child2: {child2}")

    # slots=True 메모리 비교
    print("\n=== slots=True 메모리 비교 ===")
    regular = RegularPoint(1.0, 2.0, 3.0)
    slotted = SlottedPoint(1.0, 2.0, 3.0)

    regular_size = sys.getsizeof(regular) + sys.getsizeof(regular.__dict__)
    slotted_size = sys.getsizeof(slotted)

    print(f"RegularPoint 크기: {regular_size} bytes (인스턴스 + __dict__)")
    print(f"SlottedPoint 크기: {slotted_size} bytes")
    print(f"절감: {regular_size - slotted_size} bytes ({(1 - slotted_size / regular_size) * 100:.0f}%)")

    # slots=True는 __dict__ 없음
    print(f"\nRegularPoint has __dict__: {hasattr(regular, '__dict__')}")
    print(f"SlottedPoint has __dict__: {hasattr(slotted, '__dict__')}")
