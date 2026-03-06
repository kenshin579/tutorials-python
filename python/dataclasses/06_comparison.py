"""dataclass vs NamedTuple vs TypedDict 비교 및 벤치마크"""

import sys
import timeit
from dataclasses import dataclass
from typing import NamedTuple, TypedDict


# 1. 동일한 데이터 구조를 세 가지 방식으로 정의
@dataclass
class UserDC:
    name: str
    age: int
    email: str


class UserNT(NamedTuple):
    name: str
    age: int
    email: str


class UserTD(TypedDict):
    name: str
    age: int
    email: str


@dataclass(slots=True)
class UserDCSlots:
    name: str
    age: int
    email: str


# 2. 기능 비교 함수
def feature_comparison() -> None:
    # dataclass — 변경 가능
    dc = UserDC("Alice", 30, "alice@example.com")
    dc.age = 31  # OK

    # NamedTuple — 불변
    nt = UserNT("Alice", 30, "alice@example.com")
    # nt.age = 31  # AttributeError!
    print(f"NamedTuple 인덱싱: nt[0] = {nt[0]}")
    print(f"NamedTuple 언패킹: name={nt.name}, age={nt.age}")

    # TypedDict — 딕셔너리 기반
    td: UserTD = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    td["age"] = 31  # OK (딕셔너리)
    print(f"TypedDict 접근: td['name'] = {td['name']}")


# 3. 메모리 비교
def memory_comparison() -> dict[str, int]:
    dc = UserDC("Alice", 30, "alice@example.com")
    nt = UserNT("Alice", 30, "alice@example.com")
    td: UserTD = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    dc_slots = UserDCSlots("Alice", 30, "alice@example.com")

    sizes = {
        "dataclass": sys.getsizeof(dc) + sys.getsizeof(dc.__dict__),
        "dataclass(slots)": sys.getsizeof(dc_slots),
        "NamedTuple": sys.getsizeof(nt),
        "TypedDict": sys.getsizeof(td),
    }
    return sizes


# 4. 생성 속도 비교
def speed_comparison(n: int = 100_000) -> dict[str, float]:
    results = {}
    results["dataclass"] = timeit.timeit(
        'UserDC("Alice", 30, "alice@example.com")',
        globals={"UserDC": UserDC},
        number=n,
    )
    results["dataclass(slots)"] = timeit.timeit(
        'UserDCSlots("Alice", 30, "alice@example.com")',
        globals={"UserDCSlots": UserDCSlots},
        number=n,
    )
    results["NamedTuple"] = timeit.timeit(
        'UserNT("Alice", 30, "alice@example.com")',
        globals={"UserNT": UserNT},
        number=n,
    )
    results["TypedDict"] = timeit.timeit(
        '{"name": "Alice", "age": 30, "email": "alice@example.com"}',
        number=n,
    )
    return results


if __name__ == "__main__":
    # 기능 비교
    print("=== 기능 비교 ===")
    feature_comparison()

    # 메모리 비교
    print("\n=== 메모리 비교 (bytes) ===")
    sizes = memory_comparison()
    for name, size in sizes.items():
        print(f"  {name:20s}: {size:4d} bytes")

    # 생성 속도 비교
    print("\n=== 생성 속도 비교 (100,000회) ===")
    speeds = speed_comparison()
    for name, elapsed in speeds.items():
        print(f"  {name:20s}: {elapsed:.4f}s")
