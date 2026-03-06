"""attrs 라이브러리: @define, @frozen, validator, converter"""

import attr
from attrs import define, field, frozen, validators


# 1. @define — 기본 mutable 클래스 (slots=True 기본)
@define
class Point:
    x: float
    y: float


# 2. @frozen — 불변 클래스
@frozen
class Color:
    r: int
    g: int
    b: int

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"


# 3. validator — 필드 값 검증
@define
class User:
    name: str = field(validator=validators.instance_of(str))
    age: int = field(validator=[validators.instance_of(int), validators.ge(0), validators.le(150)])
    email: str = field(validator=validators.matches_re(r".+@.+\..+"))


# 4. 커스텀 validator
def validate_port(instance: object, attribute: attr.Attribute, value: int) -> None:  # type: ignore[type-arg]
    if not 1 <= value <= 65535:
        raise ValueError(f"포트 번호는 1~65535 사이여야 합니다: {value}")


@define
class ServerConfig:
    host: str = "localhost"
    port: int = field(default=8080, validator=validate_port)
    debug: bool = False


# 5. converter — 자동 타입 변환
@define
class Record:
    id: int = field(converter=int)
    name: str = field(converter=str)
    tags: list[str] = field(factory=list)


# 6. factory — mutable 기본값 (dataclass의 default_factory와 동일)
@define
class TaskList:
    name: str
    tasks: list[str] = field(factory=list)
    metadata: dict[str, str] = field(factory=dict)


if __name__ == "__main__":
    # @define
    print("=== @define ===")
    p = Point(1.0, 2.0)
    print(f"point: {p}")
    p.x = 10.0  # mutable
    print(f"modified: {p}")

    # @frozen
    print("\n=== @frozen ===")
    red = Color(255, 0, 0)
    print(f"color: {red}, hex: {red.hex}")
    try:
        red.r = 128  # type: ignore[misc]
    except attr.exceptions.FrozenInstanceError as e:
        print(f"FrozenInstanceError: {e}")

    # validator
    print("\n=== validator ===")
    user = User(name="Alice", age=30, email="alice@example.com")
    print(f"user: {user}")
    try:
        User(name="Bob", age=-1, email="bob@test.com")
    except ValueError as e:
        print(f"validation error: {e}")

    # 커스텀 validator
    print("\n=== 커스텀 validator ===")
    config = ServerConfig(host="0.0.0.0", port=443)
    print(f"config: {config}")
    try:
        ServerConfig(port=99999)
    except ValueError as e:
        print(f"port error: {e}")

    # converter
    print("\n=== converter ===")
    record = Record(id="42", name=123, tags=["python", "attrs"])  # type: ignore[arg-type]
    print(f"record: {record}")
    print(f"id type: {type(record.id)}, name type: {type(record.name)}")

    # factory
    print("\n=== factory ===")
    t1 = TaskList("Work")
    t2 = TaskList("Personal")
    t1.tasks.append("meeting")
    print(f"t1: {t1}")
    print(f"t2: {t2}")  # 독립적
