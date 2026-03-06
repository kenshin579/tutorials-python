"""유틸리티 타입: TypeAlias, TypeGuard, TypedDict"""

from typing import NotRequired, Required, TypedDict, TypeGuard

# 1. TypeAlias — 복잡한 타입의 별칭 (Python 3.12+ type 문법)
# Python 3.12+: type Vector = list[float]
# Python 3.10+: TypeAlias 사용
type Vector = list[float]
type Matrix = list[Vector]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
type Callback = callable  # noqa: E9998


def dot_product(a: Vector, b: Vector) -> float:
    """벡터 내적"""
    return sum(x * y for x, y in zip(a, b))


def transpose(matrix: Matrix) -> Matrix:
    """행렬 전치"""
    return [list(row) for row in zip(*matrix)]


# 2. TypeGuard — 타입 좁히기 (narrowing)
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """모든 요소가 str인지 검사 — True 반환 시 타입이 list[str]로 좁혀짐"""
    return all(isinstance(x, str) for x in val)


def process_items(items: list[object]) -> str:
    """TypeGuard로 타입 좁히기"""
    if is_str_list(items):
        # 여기서 items는 list[str]로 추론됨
        return ", ".join(items)
    return str(items)


def is_not_none(val: object | None) -> TypeGuard[object]:
    """None이 아닌지 검사"""
    return val is not None


# 3. TypedDict — 키별 타입이 다른 딕셔너리
class UserProfile(TypedDict):
    """필수 필드만 있는 TypedDict"""

    name: str
    age: int
    email: str


class Config(TypedDict, total=False):
    """모든 필드가 선택적 (total=False)"""

    host: str
    port: int
    debug: bool


# Python 3.11+: Required / NotRequired
class APIResponse(TypedDict):
    """필수/선택 필드 혼합"""

    status: Required[int]
    data: Required[dict[str, object]]
    error: NotRequired[str]
    metadata: NotRequired[dict[str, str]]


def create_user(profile: UserProfile) -> str:
    return f"Created: {profile['name']} ({profile['age']})"


def get_config(overrides: Config | None = None) -> Config:
    defaults: Config = {"host": "localhost", "port": 8080, "debug": False}
    if overrides:
        defaults.update(overrides)
    return defaults


if __name__ == "__main__":
    # TypeAlias
    print("=== TypeAlias ===")
    v1: Vector = [1.0, 2.0, 3.0]
    v2: Vector = [4.0, 5.0, 6.0]
    print(f"dot_product: {dot_product(v1, v2)}")

    m: Matrix = [[1.0, 2.0], [3.0, 4.0]]
    print(f"transpose: {transpose(m)}")

    # TypeGuard
    print("\n=== TypeGuard ===")
    mixed: list[object] = [1, "two", 3]
    strings: list[object] = ["a", "b", "c"]
    print(f"is_str_list(mixed): {is_str_list(mixed)}")
    print(f"is_str_list(strings): {is_str_list(strings)}")
    print(f"process(strings): {process_items(strings)}")

    # TypedDict
    print("\n=== TypedDict ===")
    user: UserProfile = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    print(f"create_user: {create_user(user)}")

    config = get_config({"port": 9090})
    print(f"config: {config}")

    response: APIResponse = {"status": 200, "data": {"users": []}}
    print(f"response: {response}")
