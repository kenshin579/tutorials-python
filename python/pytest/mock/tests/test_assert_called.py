"""assert_called 계열 호출 검증 메서드."""

from unittest.mock import Mock, call

import pytest


class TestAssertCalled:
    """호출 여부 검증."""

    def test_assert_called(self):
        """한 번이라도 호출되었는지 검증."""
        mock = Mock()
        mock(1, 2)

        mock.assert_called()

    def test_assert_called_once(self):
        """정확히 1회 호출되었는지 검증."""
        mock = Mock()
        mock("hello")

        mock.assert_called_once()

    def test_assert_called_once_실패(self):
        """2회 이상 호출 시 assert_called_once 실패."""
        mock = Mock()
        mock("first")
        mock("second")

        with pytest.raises(AssertionError):
            mock.assert_called_once()

    def test_assert_not_called(self):
        """호출되지 않았는지 검증."""
        mock = Mock()

        mock.assert_not_called()


class TestAssertCalledWith:
    """호출 인자 검증."""

    def test_assert_called_with(self):
        """마지막 호출의 인자를 검증."""
        mock = Mock()
        mock("hello", key="value")

        mock.assert_called_with("hello", key="value")

    def test_assert_called_once_with(self):
        """정확히 1회 호출 + 인자 동시 검증."""
        mock = Mock()
        mock(42, name="test")

        mock.assert_called_once_with(42, name="test")

    def test_assert_any_call(self):
        """호출 이력 중 특정 인자로 한 번이라도 호출되었는지 검증."""
        mock = Mock()
        mock("first")
        mock("second")
        mock("third")

        mock.assert_any_call("second")


class TestCallHistory:
    """호출 이력 상세 확인."""

    def test_call_count(self):
        """호출 횟수 확인."""
        mock = Mock()
        mock(1)
        mock(2)
        mock(3)

        assert mock.call_count == 3

    def test_call_args(self):
        """마지막 호출의 인자 확인."""
        mock = Mock()
        mock("hello", key="world")

        assert mock.call_args.args == ("hello",)
        assert mock.call_args.kwargs == {"key": "world"}

    def test_call_args_list(self):
        """전체 호출 이력 확인."""
        mock = Mock()
        mock("first")
        mock("second", x=1)
        mock("third")

        assert mock.call_args_list == [
            call("first"),
            call("second", x=1),
            call("third"),
        ]

    def test_reset_mock(self):
        """reset_mock()으로 호출 이력 초기화."""
        mock = Mock()
        mock("before")
        assert mock.call_count == 1

        mock.reset_mock()
        assert mock.call_count == 0
        mock.assert_not_called()
