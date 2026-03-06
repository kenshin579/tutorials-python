"""cattrs: structure/unstructure로 직렬화/역직렬화"""

import json

import cattrs
from attrs import define, frozen


# 1. 기본 structure/unstructure
@define
class User:
    name: str
    age: int
    email: str


# 2. 중첩 구조
@frozen
class Address:
    city: str
    country: str


@frozen
class Employee:
    name: str
    role: str
    address: Address


# 3. 리스트 포함 구조
@frozen
class Team:
    name: str
    members: list[Employee]


# 4. JSON API 응답 변환
@frozen
class APIResponse:
    status: int
    data: list[User]
    total: int


def basic_demo() -> None:
    """기본 structure/unstructure 사용"""
    # unstructure: 객체 → dict
    user = User(name="Alice", age=30, email="alice@example.com")
    user_dict = cattrs.unstructure(user)
    print(f"unstructure: {user_dict}")

    # structure: dict → 객체
    data = {"name": "Bob", "age": 25, "email": "bob@test.com"}
    user2 = cattrs.structure(data, User)
    print(f"structure: {user2}")


def nested_demo() -> None:
    """중첩 구조 변환"""
    emp = Employee(
        name="Alice",
        role="Engineer",
        address=Address(city="Seoul", country="Korea"),
    )

    # 객체 → dict (중첩도 자동 변환)
    emp_dict = cattrs.unstructure(emp)
    print(f"unstructure: {emp_dict}")

    # dict → 객체 (중첩도 자동 복원)
    restored = cattrs.structure(emp_dict, Employee)
    print(f"structure: {restored}")


def list_demo() -> None:
    """리스트 포함 구조 변환"""
    team = Team(
        name="Backend",
        members=[
            Employee("Alice", "Lead", Address("Seoul", "Korea")),
            Employee("Bob", "Developer", Address("Tokyo", "Japan")),
        ],
    )

    team_dict = cattrs.unstructure(team)
    print(f"unstructure: {json.dumps(team_dict, indent=2)}")

    restored = cattrs.structure(team_dict, Team)
    print(f"structure: {restored}")


def json_api_demo() -> None:
    """JSON API 응답 변환 실전 예시"""
    # API에서 받은 JSON 응답
    json_response = """{
        "status": 200,
        "data": [
            {"name": "Alice", "age": 30, "email": "alice@example.com"},
            {"name": "Bob", "age": 25, "email": "bob@test.com"}
        ],
        "total": 2
    }"""

    # JSON → dict → 타입 안전한 객체
    raw = json.loads(json_response)
    response = cattrs.structure(raw, APIResponse)

    print(f"status: {response.status}")
    print(f"total: {response.total}")
    for user in response.data:
        print(f"  user: {user.name} ({user.email})")

    # 객체 → JSON (역방향)
    back_to_json = json.dumps(cattrs.unstructure(response), indent=2)
    print(f"back to JSON:\n{back_to_json}")


if __name__ == "__main__":
    print("=== 기본 structure/unstructure ===")
    basic_demo()

    print("\n=== 중첩 구조 ===")
    nested_demo()

    print("\n=== 리스트 포함 구조 ===")
    list_demo()

    print("\n=== JSON API 응답 변환 ===")
    json_api_demo()
