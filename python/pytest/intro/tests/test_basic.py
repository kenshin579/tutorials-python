"""pytest 기본 assert문, pytest.raises, pytest.approx 사용법."""

import pytest

from src.calculator import Calculator, add, divide


class TestBasicAssert:
    """pytest assert문 기본 사용법."""

    def test_add(self):
        """pytest는 assert문 하나로 검증한다."""
        calc = Calculator()
        assert calc.add(2, 3) == 5

    def test_subtract(self):
        calc = Calculator()
        assert calc.subtract(10, 4) == 6

    def test_multiply(self):
        calc = Calculator()
        assert calc.multiply(3, 4) == 12

    def test_divide(self):
        calc = Calculator()
        assert calc.divide(10, 2) == 5.0

    def test_assert_with_message(self):
        """실패 시 메시지를 추가할 수 있다."""
        calc = Calculator()
        result = calc.add(2, 3)
        assert result == 5, f"Expected 5 but got {result}"


class TestAssertionRewriting:
    """pytest의 assertion rewriting: 실패 시 상세 diff 자동 표시."""

    def test_리스트_비교(self):
        """리스트 비교 시 어떤 요소가 다른지 자동 표시."""
        assert [1, 2, 3] == [1, 2, 3]

    def test_딕셔너리_비교(self):
        """딕셔너리 비교 시 다른 키-값을 자동 표시."""
        expected = {"name": "Frank", "age": 30}
        result = {"name": "Frank", "age": 30}
        assert result == expected

    def test_문자열_비교(self):
        """긴 문자열 비교 시 diff를 자동 표시."""
        assert "hello world" == "hello world"


class TestPytestRaises:
    """pytest.raises로 예외 발생 검증."""

    def test_raises_기본(self):
        """예외 타입만 검증."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.divide(10, 0)

    def test_raises_메시지_검증(self):
        """match로 예외 메시지를 정규식으로 검증."""
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            divide(10, 0)

    def test_raises_모듈_함수(self):
        """모듈 레벨 함수에서도 동일하게 사용."""
        with pytest.raises(ValueError):
            divide(5, 0)

    def test_raises_예외_객체_접근(self):
        """발생한 예외 객체에 접근할 수 있다."""
        with pytest.raises(ValueError) as exc_info:
            divide(10, 0)
        assert "0으로 나눌 수 없습니다" in str(exc_info.value)


class TestPytestApprox:
    """pytest.approx로 부동소수점 비교."""

    def test_approx_기본(self):
        """부동소수점 오차를 허용하여 비교."""
        assert 0.1 + 0.2 == pytest.approx(0.3)

    def test_approx_상대_오차(self):
        """rel 파라미터로 상대 오차 지정."""
        assert 100.0 == pytest.approx(99.5, rel=0.01)

    def test_approx_절대_오차(self):
        """abs 파라미터로 절대 오차 지정."""
        assert 0.1 + 0.2 == pytest.approx(0.3, abs=1e-10)

    def test_approx_리스트(self):
        """리스트의 각 요소도 approx로 비교 가능."""
        assert [0.1 + 0.2, 0.2 + 0.4] == pytest.approx([0.3, 0.6])
