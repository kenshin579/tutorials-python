"""비교와 직렬화 - ==, is, JSON, DB 패턴"""

import json
from enum import Enum, IntEnum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class IntColor(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3


# == vs is 비교
def comparison_examples() -> dict:
    return {
        "enum_is": Color.RED is Color.RED,      # True (싱글턴)
        "enum_eq": Color.RED == Color.RED,       # True
        "enum_eq_int": Color.RED == 1,           # False (일반 Enum)
        "intenum_eq_int": IntColor.RED == 1,     # True (IntEnum)
    }


# JSON 직렬화
class EnumEncoder(json.JSONEncoder):
    """Enum을 JSON으로 직렬화하는 커스텀 인코더"""

    def default(self, obj):
        if isinstance(obj, Enum):
            return {"__enum__": type(obj).__name__, "name": obj.name, "value": obj.value}
        return super().default(obj)


def enum_to_json(data: dict) -> str:
    """Enum 값을 포함한 딕셔너리를 JSON으로 변환한다."""
    return json.dumps(data, cls=EnumEncoder)


def enum_from_json(json_str: str, enum_class: type[Enum]) -> dict:
    """JSON 문자열에서 Enum 값을 복원한다."""

    def decode_enum(obj):
        if "__enum__" in obj:
            return enum_class(obj["value"])
        return obj

    return json.loads(json_str, object_hook=decode_enum)


# DB 저장 패턴 - value를 저장/복원
def to_db_value(member: Enum):
    """DB에 저장할 값을 추출한다."""
    return member.value


def from_db_value(enum_class: type[Enum], value):
    """DB에서 읽은 값으로 Enum 멤버를 복원한다."""
    return enum_class(value)
