"""return_value와 side_effect 사용법."""

from unittest.mock import Mock

import pytest


class TestReturnValue:
    """return_value로 단일 반환값 설정."""

    def test_return_value_기본(self):
        mock = Mock()
        mock.return_value = 42

        assert mock() == 42
        assert mock() == 42  # 항상 같은 값 반환

    def test_메서드_return_value(self):
        mock = Mock()
        mock.calculate.return_value = 100

        assert mock.calculate(1, 2) == 100


class TestSideEffect:
    """side_effect로 다양한 동작 제어."""

    def test_side_effect_순차적_반환(self):
        """리스트를 넣으면 호출마다 순서대로 반환."""
        mock = Mock()
        mock.side_effect = [1, 2, 3]

        assert mock() == 1
        assert mock() == 2
        assert mock() == 3

        # 리스트 소진 후 호출 시 StopIteration 발생
        with pytest.raises(StopIteration):
            mock()

    def test_side_effect_커스텀_함수(self):
        """함수를 넣으면 호출 시 해당 함수가 실행."""
        mock = Mock()
        mock.side_effect = lambda x: x * 2

        assert mock(3) == 6
        assert mock(5) == 10

    def test_side_effect_예외_발생(self):
        """예외 인스턴스를 넣으면 호출 시 예외 발생."""
        mock = Mock()
        mock.side_effect = ValueError("잘못된 입력")

        with pytest.raises(ValueError, match="잘못된 입력"):
            mock()

    def test_side_effect_예외와_정상값_혼합(self):
        """리스트에 예외와 정상값을 섞을 수 있다."""
        mock = Mock()
        mock.side_effect = [
            ConnectionError("연결 실패"),
            {"id": 1, "name": "Frank"},  # 재시도 성공
        ]

        with pytest.raises(ConnectionError):
            mock()

        result = mock()
        assert result["name"] == "Frank"

    def test_side_effect_None으로_초기화(self):
        """side_effect를 None으로 설정하면 return_value로 동작."""
        mock = Mock(return_value=42)
        mock.side_effect = ValueError("에러")

        with pytest.raises(ValueError):
            mock()

        # side_effect를 None으로 해제하면 return_value 사용
        mock.side_effect = None
        assert mock() == 42
