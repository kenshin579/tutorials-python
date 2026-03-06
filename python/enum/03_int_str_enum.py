"""IntEnum, StrEnum - 타입 호환 Enum"""

from enum import Enum, IntEnum, StrEnum


class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# 일반 Enum과의 비교
class PureColor(Enum):
    RED = 1
    GREEN = 2


class IntColor(IntEnum):
    RED = 1
    GREEN = 2


def int_enum_comparison():
    """IntEnum은 정수와 직접 비교/연산이 가능하다."""
    return {
        "inteum_eq_int": HttpStatus.OK == 200,          # True
        "intenum_gt": HttpStatus.NOT_FOUND > 200,       # True
        "intenum_arithmetic": HttpStatus.OK + 1,        # 201
        "pure_eq_int": PureColor.RED == 1,              # False (일반 Enum)
    }


def str_enum_usage():
    """StrEnum은 문자열 연산에 직접 사용 가능하다."""
    return {
        "format": f"level: {LogLevel.DEBUG}",           # "level: debug"
        "upper": LogLevel.DEBUG.upper(),                # "DEBUG"
        "concat": "log_" + LogLevel.INFO,               # "log_info"
        "eq_str": LogLevel.DEBUG == "debug",            # True
    }
