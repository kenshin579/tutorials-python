"""간단한 계산기 모듈 - 커버리지 측정 데모용"""


class Calculator:
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

    def power(self, base: float, exp: int) -> float:
        if exp < 0:
            raise ValueError("음수 지수는 지원하지 않습니다")
        result = 1.0
        for _ in range(exp):
            result *= base
        return result

    def factorial(self, n: int) -> int:
        if n < 0:
            raise ValueError("음수의 팩토리얼은 정의되지 않습니다")
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
