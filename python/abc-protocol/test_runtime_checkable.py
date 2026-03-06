"""@runtime_checkable, isinstance() 검사, 제한사항 확인"""

import unittest
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


@runtime_checkable
class HasLength(Protocol):
    def __len__(self) -> int: ...


class DatabaseConnection:
    """close() 메서드가 있으므로 Closeable 충족"""

    def close(self) -> None:
        pass


class FileHandle:
    """close() 메서드가 있으므로 Closeable 충족"""

    def close(self) -> None:
        pass


class PlainObject:
    """close() 메서드가 없으므로 Closeable 미충족"""

    pass


# 시그니처가 다르지만 메서드 이름만 같은 경우
class FakeCloseable:
    """close()가 인자를 받지만, runtime_checkable은 시그니처를 검사하지 않음"""

    def close(self, force: bool = False) -> str:
        return "closed"


class TestRuntimeCheckable(unittest.TestCase):
    def test_isinstance_with_runtime_checkable(self):
        """@runtime_checkable Protocol은 isinstance() 검사 가능"""
        db = DatabaseConnection()
        fh = FileHandle()
        assert isinstance(db, Closeable)
        assert isinstance(fh, Closeable)

    def test_isinstance_fails_without_method(self):
        """메서드가 없으면 isinstance 검사 실패"""
        obj = PlainObject()
        assert not isinstance(obj, Closeable)

    def test_builtin_types_with_has_length(self):
        """내장 타입도 Protocol 검사 가능"""
        assert isinstance([1, 2, 3], HasLength)
        assert isinstance("hello", HasLength)
        assert isinstance({"a": 1}, HasLength)
        assert not isinstance(42, HasLength)

    def test_signature_not_checked_at_runtime(self):
        """제한사항: runtime_checkable은 메서드 존재 여부만 확인, 시그니처는 검사하지 않음"""
        fake = FakeCloseable()
        # close() 메서드가 존재하므로 isinstance는 True
        assert isinstance(fake, Closeable)

    def test_non_runtime_checkable_raises_error(self):
        """@runtime_checkable이 없는 Protocol은 isinstance() 사용 불가"""

        class NonCheckable(Protocol):
            def process(self) -> None: ...

        class Impl:
            def process(self) -> None:
                pass

        with self.assertRaises(TypeError):
            isinstance(Impl(), NonCheckable)


class TestCloseableUtility(unittest.TestCase):
    def test_safe_close(self):
        """runtime_checkable을 활용한 안전한 close 유틸리티"""

        def safe_close(obj: object) -> bool:
            if isinstance(obj, Closeable):
                obj.close()
                return True
            return False

        assert safe_close(DatabaseConnection()) is True
        assert safe_close(PlainObject()) is False


if __name__ == "__main__":
    unittest.main()
