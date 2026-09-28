"""auto() 자동 값 할당"""

from enum import Enum, StrEnum, auto


class Priority(Enum):
    LOW = auto()      # 1
    MEDIUM = auto()   # 2
    HIGH = auto()     # 3
    CRITICAL = auto() # 4


# _generate_next_value_ 오버라이드
class OrdinalEnum(Enum):
    """값을 0부터 시작하도록 커스텀 자동 값 생성"""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return count  # 0부터 시작

    FIRST = auto()   # 0
    SECOND = auto()  # 1
    THIRD = auto()   # 2


# StrEnum + auto(): 이름을 소문자 값으로 자동 할당
class Status(StrEnum):
    ACTIVE = auto()    # "active"
    INACTIVE = auto()  # "inactive"
    PENDING = auto()   # "pending"
