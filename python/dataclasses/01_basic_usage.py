"""@dataclass 기본 사용법"""

from dataclasses import dataclass


# 1. dataclass 없이 작성한 클래스 (boilerplate가 많다)
class PointManual:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"PointManual(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointManual):
            return NotImplemented
        return self.x == other.x and self.y == other.y


# 2. dataclass로 동일한 클래스 — boilerplate 제거
@dataclass
class Point:
    x: float
    y: float


# 3. 기본값 설정
@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


# 4. @dataclass 매개변수 옵션
@dataclass(repr=True, eq=True, order=True)
class Version:
    major: int
    minor: int
    patch: int


if __name__ == "__main__":
    # 기본 사용법
    print("=== @dataclass 기본 ===")
    p1 = Point(1.0, 2.0)
    p2 = Point(1.0, 2.0)
    p3 = Point(3.0, 4.0)
    print(f"p1: {p1}")
    print(f"p1 == p2: {p1 == p2}")  # True
    print(f"p1 == p3: {p1 == p3}")  # False

    # 기본값
    print("\n=== 기본값 ===")
    config = Config()
    print(f"config: {config}")
    custom = Config(host="0.0.0.0", port=9090, debug=True)
    print(f"custom: {custom}")

    # order=True
    print("\n=== order=True ===")
    v1 = Version(1, 0, 0)
    v2 = Version(2, 1, 0)
    v3 = Version(1, 2, 0)
    versions = sorted([v2, v3, v1])
    print(f"sorted: {versions}")
