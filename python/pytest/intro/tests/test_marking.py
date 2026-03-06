"""마킹: skip, skipif, xfail, 커스텀 마커."""

import sys

import pytest

from src.calculator import Calculator


class TestSkip:
    """@pytest.mark.skip: 테스트 건너뛰기."""

    @pytest.mark.skip(reason="아직 구현되지 않은 기능")
    def test_skip_기본(self):
        """무조건 건너뛴다."""
        assert False

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows에서는 실행하지 않음",
    )
    def test_skipif_조건부(self):
        """조건이 True면 건너뛴다."""
        calc = Calculator()
        assert calc.add(1, 1) == 2


class TestXfail:
    """@pytest.mark.xfail: 실패 예상 테스트."""

    @pytest.mark.xfail(reason="known bug: 부동소수점 정밀도 이슈")
    def test_xfail_실패_예상(self):
        """실패하면 xfail로 표시, 성공하면 xpass로 표시."""
        assert 0.1 + 0.2 == 0.3  # 부동소수점이므로 실패

    @pytest.mark.xfail(reason="이 테스트는 예상과 달리 성공한다")
    def test_xfail_성공(self):
        """xfail이지만 실제로는 성공 → xpass로 표시."""
        calc = Calculator()
        assert calc.add(1, 1) == 2

    @pytest.mark.xfail(strict=True, reason="strict 모드: 성공하면 오히려 실패")
    def test_xfail_strict(self):
        """strict=True면 성공 시 테스트 실패로 처리."""
        assert 0.1 + 0.2 == 0.3  # 실패하므로 xfail 정상


class TestCustomMarker:
    """커스텀 마커 정의 및 -m 필터링."""

    @pytest.mark.slow
    def test_slow_테스트(self):
        """pytest -m slow 로 이 테스트만 실행 가능."""
        calc = Calculator()
        total = sum(calc.add(i, i) for i in range(100))
        assert total == 9900

    @pytest.mark.integration
    def test_integration_테스트(self):
        """pytest -m integration 으로 필터링."""
        calc = Calculator()
        result = calc.multiply(calc.add(2, 3), calc.subtract(10, 4))
        assert result == 30

    def test_일반_테스트(self):
        """마커 없는 일반 테스트."""
        calc = Calculator()
        assert calc.add(1, 1) == 2

    @pytest.mark.slow
    @pytest.mark.integration
    def test_다중_마커(self):
        """여러 마커를 동시에 지정할 수 있다."""
        calc = Calculator()
        assert calc.divide(100, 4) == 25.0
