"""pytest-cov 데모: 코드 커버리지 측정

실행 방법:
    pytest --cov=src --cov-report=term-missing tests/test_cov.py
    pytest --cov=src --cov-report=html tests/test_cov.py
    pytest --cov=src --cov-fail-under=80 tests/test_cov.py
"""

import pytest


class TestCalculatorCoverage:
    """Calculator의 각 메서드를 테스트하여 커버리지를 측정한다"""

    def test_add(self, calculator):
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0

    def test_subtract(self, calculator):
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(0, 5) == -5

    def test_multiply(self, calculator):
        assert calculator.multiply(3, 4) == 12
        assert calculator.multiply(0, 100) == 0

    def test_divide(self, calculator):
        assert calculator.divide(10, 2) == 5.0
        assert calculator.divide(7, 2) == 3.5

    def test_divide_by_zero(self, calculator):
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            calculator.divide(10, 0)

    def test_power(self, calculator):
        assert calculator.power(2, 3) == 8.0
        assert calculator.power(5, 0) == 1.0

    def test_power_negative_exp(self, calculator):
        with pytest.raises(ValueError, match="음수 지수"):
            calculator.power(2, -1)

    def test_factorial(self, calculator):
        assert calculator.factorial(0) == 1
        assert calculator.factorial(5) == 120

    def test_factorial_negative(self, calculator):
        with pytest.raises(ValueError, match="음수의 팩토리얼"):
            calculator.factorial(-1)
