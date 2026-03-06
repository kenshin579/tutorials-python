"""사칙연산 계산기 모듈 (테스트 대상)."""


class Calculator:
    """기본 사칙연산 계산기."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b


def add(a: float, b: float) -> float:
    """모듈 레벨 덧셈 함수."""
    return a + b


def divide(a: float, b: float) -> float:
    """모듈 레벨 나눗셈 함수."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b
