"""field() 옵션: default_factory, repr, compare, init, kw_only"""

from dataclasses import dataclass, field


# 1. default_factory — mutable 기본값
@dataclass
class Student:
    name: str
    grades: list[int] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)


# 2. repr=False, compare=False — 특정 필드 제외
@dataclass
class User:
    username: str
    email: str
    password: str = field(repr=False)  # repr에서 제외 (보안)
    login_count: int = field(default=0, compare=False)  # 비교에서 제외


# 3. init=False — 생성자에서 제외
@dataclass
class Article:
    title: str
    content: str
    word_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.word_count = len(self.content.split())


# 4. kw_only=True (Python 3.10+)
@dataclass(kw_only=True)
class Connection:
    host: str
    port: int = 5432
    database: str = "mydb"
    timeout: int = 30


# 5. 부분 kw_only — 일부 필드만 키워드 전용
@dataclass
class Request:
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict, kw_only=True)
    timeout: int = field(default=30, kw_only=True)


if __name__ == "__main__":
    # default_factory
    print("=== default_factory ===")
    s1 = Student("Alice")
    s2 = Student("Bob")
    s1.grades.append(90)
    print(f"s1: {s1}")
    print(f"s2: {s2}")  # s2.grades는 빈 리스트 (공유 안 됨)

    # repr, compare 제외
    print("\n=== repr=False, compare=False ===")
    u1 = User("alice", "a@b.com", "secret123", login_count=5)
    u2 = User("alice", "a@b.com", "secret123", login_count=10)
    print(f"u1: {u1}")  # password 숨겨짐
    print(f"u1 == u2: {u1 == u2}")  # True (login_count 무시)

    # init=False
    print("\n=== init=False ===")
    article = Article("Hello", "This is a sample article with five words")
    print(f"article: {article}")

    # kw_only
    print("\n=== kw_only ===")
    conn = Connection(host="localhost", port=5432, database="mydb")
    print(f"conn: {conn}")

    # 부분 kw_only
    print("\n=== 부분 kw_only ===")
    req = Request("GET", "https://api.example.com", headers={"Authorization": "Bearer token"})
    print(f"req: {req}")
