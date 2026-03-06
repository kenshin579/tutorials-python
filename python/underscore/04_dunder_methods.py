"""던더 메서드와 속성 (__name__) 예제"""


class Vector:
    """주요 매직 메서드를 구현한 Vector 클래스"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # 문자열 표현
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # 비교
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Vector") -> bool:
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

    # 산술 연산
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)


# 매직 속성 예제
def show_magic_attributes() -> dict:
    """주요 매직 속성을 딕셔너리로 반환한다."""

    def sample_function():
        """샘플 함수의 독스트링"""
        pass

    return {
        "func_name": sample_function.__name__,
        "func_doc": sample_function.__doc__,
        "func_module": sample_function.__module__,
        "class_name": Vector.__name__,
        "class_module": Vector.__module__,
    }
