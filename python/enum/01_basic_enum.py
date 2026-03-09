"""Enum 기본 문법 - 정의, 멤버 접근, 이터레이션, 싱글턴"""

from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


# 멤버 접근 방식 3가지
def access_enum_members():
    """Enum 멤버에 접근하는 3가지 방법을 보여준다."""
    by_attr = Color.RED        # 속성 접근
    by_name = Color["RED"]     # 이름으로 접근
    by_value = Color(1)        # 값으로 접근
    return by_attr, by_name, by_value


# name, value 속성
def get_name_and_value(member: Color) -> tuple[str, int]:
    return member.name, member.value


# 이터레이션
def list_all_colors() -> list[Color]:
    return list(Color)


# 싱글턴 특성
def is_singleton() -> bool:
    """Enum 멤버는 싱글턴이므로 is 비교가 가능하다."""
    return Color.RED is Color.RED
