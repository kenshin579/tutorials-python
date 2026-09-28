"""Name Mangling (__name) 예제"""


class Base:
    """Name mangling 기본 예제"""

    def __init__(self):
        self.public = "public"
        self._protected = "protected"
        self.__private = "mangled"  # _Base__private로 변환됨

    def get_private(self) -> str:
        return self.__private


class Child(Base):
    """상속 시 name mangling으로 이름 충돌이 방지되는 예제"""

    def __init__(self):
        super().__init__()
        self.__private = "child_mangled"  # _Child__private로 변환됨

    def get_child_private(self) -> str:
        return self.__private


# 상속 구조에서 이름 충돌 방지
class Account:
    """부모 클래스의 내부 데이터를 보호하는 예제"""

    def __init__(self, balance: float):
        self.__balance = balance  # _Account__balance

    def get_balance(self) -> float:
        return self.__balance


class SavingsAccount(Account):
    """자식 클래스에서 동일한 이름을 사용해도 충돌하지 않는다."""

    def __init__(self, balance: float, interest_rate: float):
        super().__init__(balance)
        self.__balance = balance * (1 + interest_rate)  # _SavingsAccount__balance

    def get_projected_balance(self) -> float:
        return self.__balance
