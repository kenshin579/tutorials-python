"""Protocol: 구조적 서브타이핑 (duck typing의 타입 힌트 버전)"""

from typing import Protocol, runtime_checkable


# 1. 기본 Protocol 정의
class Drawable(Protocol):
    """draw() 메서드를 가진 모든 객체"""

    def draw(self) -> str: ...


class Circle:
    def draw(self) -> str:
        return "○"


class Square:
    def draw(self) -> str:
        return "□"


class Text:
    """draw() 메서드가 없음 → Drawable 아님"""

    def render(self) -> str:
        return "text"


def render(shape: Drawable) -> str:
    """Drawable Protocol을 만족하는 객체만 허용"""
    return shape.draw()


# 2. 여러 메서드를 가진 Protocol
class Sized(Protocol):
    def __len__(self) -> int: ...


class Container(Protocol):
    def __contains__(self, item: object) -> bool: ...


class SizedContainer(Sized, Container, Protocol):
    """여러 Protocol 조합"""

    ...


def check_item(container: SizedContainer, item: object) -> bool:
    """크기 확인 + 포함 여부 확인"""
    if len(container) == 0:
        return False
    return item in container


# 3. runtime_checkable Protocol
@runtime_checkable
class Closeable(Protocol):
    """close() 메서드가 있는 객체"""

    def close(self) -> None: ...


class FileResource:
    def close(self) -> None:
        print("  FileResource closed")


class NetworkResource:
    def close(self) -> None:
        print("  NetworkResource closed")


def safe_close(resource: object) -> None:
    """runtime_checkable로 isinstance() 사용 가능"""
    if isinstance(resource, Closeable):
        resource.close()
    else:
        print(f"  {type(resource).__name__}은 Closeable이 아님")


if __name__ == "__main__":
    # 기본 Protocol
    print("=== Drawable Protocol ===")
    print(f"Circle: {render(Circle())}")
    print(f"Square: {render(Square())}")

    # SizedContainer
    print("\n=== SizedContainer ===")
    print(f"check [1,2,3] contains 2: {check_item([1, 2, 3], 2)}")
    print(f"check [] contains 1: {check_item([], 1)}")

    # runtime_checkable
    print("\n=== runtime_checkable ===")
    safe_close(FileResource())
    safe_close(NetworkResource())
    safe_close("not closeable")
