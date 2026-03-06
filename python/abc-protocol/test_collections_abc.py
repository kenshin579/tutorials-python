"""collections.abc 주요 ABC 사용, __subclasshook__, register()"""

import unittest
from collections.abc import (
    Callable,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    MutableSequence,
    Sequence,
    Sized,
)
from abc import ABCMeta


# 커스텀 이터레이터: Iterator ABC 구현
class Countdown(Iterator):
    def __init__(self, start: int):
        self._current = start

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


# 커스텀 시퀀스: Sequence ABC 구현 (__getitem__, __len__만 구현하면 나머지 자동 제공)
class FixedList(Sequence):
    def __init__(self, *items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)


# __subclasshook__으로 가상 하위 클래스 자동 인식
class Closeable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Closeable:
            if hasattr(subclass, "close") and callable(subclass.close):
                return True
        return NotImplemented


class FileWrapper:
    """close() 메서드가 있으므로 Closeable의 가상 하위 클래스로 인식"""

    def close(self):
        pass


class PlainObject:
    """close() 메서드가 없으므로 Closeable이 아님"""

    pass


# register()로 기존 클래스에 ABC 등록
class Printable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return NotImplemented


class Document:
    def render(self) -> str:
        return "Document content"


# Document를 Printable로 등록
Printable.register(Document)


class TestCollectionsABC(unittest.TestCase):
    def test_iterator(self):
        countdown = Countdown(3)
        assert list(countdown) == [3, 2, 1]
        assert isinstance(Countdown(1), Iterator)
        assert isinstance(Countdown(1), Iterable)

    def test_sequence(self):
        """Sequence ABC: __getitem__과 __len__만 구현하면 index, count 등 자동 제공"""
        fl = FixedList(10, 20, 30, 20)
        assert fl[0] == 10
        assert len(fl) == 4
        assert fl.index(20) == 1  # 자동 제공
        assert fl.count(20) == 2  # 자동 제공
        assert 30 in fl  # __contains__ 자동 제공
        assert isinstance(fl, Sequence)

    def test_builtin_types_are_abc_instances(self):
        """내장 타입은 이미 collections.abc에 등록되어 있음"""
        assert isinstance([1, 2], MutableSequence)
        assert isinstance((1, 2), Sequence)
        assert isinstance({"a": 1}, Mapping)
        assert isinstance("hello", Sized)
        assert isinstance("hello", Iterable)
        assert isinstance(42, Hashable)
        assert isinstance(len, Callable)


class TestSubclasshook(unittest.TestCase):
    def test_subclasshook_with_close(self):
        """close() 메서드가 있으면 Closeable로 인식"""
        assert isinstance(FileWrapper(), Closeable)
        assert issubclass(FileWrapper, Closeable)

    def test_subclasshook_without_close(self):
        """close() 메서드가 없으면 Closeable이 아님"""
        assert not isinstance(PlainObject(), Closeable)


class TestRegister(unittest.TestCase):
    def test_register(self):
        """register()로 등록된 클래스는 isinstance 검사 통과"""
        doc = Document()
        assert isinstance(doc, Printable)
        assert issubclass(Document, Printable)

    def test_register_does_not_affect_mro(self):
        """register()는 MRO에 영향을 주지 않음 (가상 하위 클래스)"""
        assert Printable not in Document.__mro__


if __name__ == "__main__":
    unittest.main()
