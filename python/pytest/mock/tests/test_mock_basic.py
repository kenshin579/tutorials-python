"""Mock, MagicMock 기본 사용법."""

from unittest.mock import MagicMock, Mock


class TestMockBasic:
    """Mock() 기본 동작 확인."""

    def test_mock_속성_자동_생성(self):
        """Mock 객체는 존재하지 않는 속성에 접근해도 에러가 발생하지 않는다."""
        mock = Mock()

        # 아무 속성이나 접근 가능 - 자동으로 새 Mock 반환
        result = mock.some_attribute
        assert isinstance(result, Mock)

    def test_mock_메서드_자동_생성(self):
        """Mock 객체는 존재하지 않는 메서드도 호출 가능하다."""
        mock = Mock()

        result = mock.some_method(1, 2, 3)
        assert isinstance(result, Mock)

        # 호출 여부 확인 가능
        mock.some_method.assert_called_once_with(1, 2, 3)

    def test_mock_return_value(self):
        """return_value로 반환값을 지정할 수 있다."""
        mock = Mock()
        mock.get_name.return_value = "Frank"

        assert mock.get_name() == "Frank"

    def test_mock_spec으로_인터페이스_제한(self):
        """spec을 지정하면 실제 클래스에 없는 속성 접근 시 AttributeError 발생."""

        class Calculator:
            def add(self, a: int, b: int) -> int:
                return a + b

        mock = Mock(spec=Calculator)
        mock.add.return_value = 10
        assert mock.add(3, 7) == 10

        # spec에 없는 속성 접근 시 에러
        try:
            mock.multiply(3, 7)
            assert False, "AttributeError가 발생해야 한다"
        except AttributeError:
            pass


class TestMagicMock:
    """MagicMock은 매직 메서드를 자동 지원한다."""

    def test_magic_mock_len(self):
        """__len__ 매직 메서드 자동 지원."""
        mock = MagicMock()
        mock.__len__.return_value = 5

        assert len(mock) == 5

    def test_magic_mock_iter(self):
        """__iter__ 매직 메서드 자동 지원."""
        mock = MagicMock()
        mock.__iter__.return_value = iter([1, 2, 3])

        assert list(mock) == [1, 2, 3]

    def test_magic_mock_getitem(self):
        """__getitem__ 매직 메서드 자동 지원."""
        mock = MagicMock()
        mock.__getitem__.return_value = "value"

        assert mock["key"] == "value"

    def test_magic_mock_context_manager(self):
        """컨텍스트 매니저로 사용 가능."""
        mock = MagicMock()
        mock.__enter__.return_value = "resource"

        with mock as resource:
            assert resource == "resource"

    def test_mock_vs_magic_mock_차이(self):
        """일반 Mock은 매직 메서드를 지원하지 않는다."""
        mock = Mock()

        try:
            len(mock)
            assert False, "TypeError가 발생해야 한다"
        except TypeError:
            pass

        # MagicMock은 기본값 반환
        magic = MagicMock()
        assert len(magic) == 0  # 기본값 0
