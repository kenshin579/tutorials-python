"""parametrize: 매개변수화 테스트."""

import pytest

from src.calculator import Calculator


class TestParametrizeBasic:
    """@pytest.mark.parametrize 기본 사용법."""

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_add(self, a, b, expected):
        """여러 입력값으로 동일 테스트를 반복 실행."""
        calc = Calculator()
        assert calc.add(a, b) == expected

    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (7, 2, 3.5),
    ])
    def test_divide(self, a, b, expected):
        calc = Calculator()
        assert calc.divide(a, b) == expected


class TestParametrizeMultiple:
    """다중 파라미터 조합."""

    @pytest.mark.parametrize("a", [1, 2])
    @pytest.mark.parametrize("b", [10, 20])
    def test_multiply_조합(self, a, b):
        """2 x 2 = 4가지 조합이 실행된다."""
        calc = Calculator()
        assert calc.multiply(a, b) == a * b


class TestParametrizeId:
    """pytest.param으로 케이스별 이름 지정."""

    @pytest.mark.parametrize("a, b, expected", [
        pytest.param(2, 3, 5, id="양수-덧셈"),
        pytest.param(-1, -1, -2, id="음수-덧셈"),
        pytest.param(0, 0, 0, id="영-덧셈"),
        pytest.param(1000000, 1, 1000001, id="큰수-덧셈"),
    ])
    def test_add_with_id(self, a, b, expected):
        """테스트 결과에 id가 표시되어 실패 시 어떤 케이스인지 알 수 있다."""
        calc = Calculator()
        assert calc.add(a, b) == expected


class TestParametrizeIndirect:
    """indirect=True: fixture에 파라미터 전달."""

    @pytest.fixture
    def input_value(self, request):
        """parametrize에서 전달된 값을 가공하여 반환."""
        return request.param * 2

    @pytest.mark.parametrize("input_value, expected", [
        (5, 10),
        (3, 6),
        (0, 0),
    ], indirect=["input_value"])
    def test_indirect(self, input_value, expected):
        """input_value fixture가 parametrize 값을 받아 가공한다."""
        assert input_value == expected
