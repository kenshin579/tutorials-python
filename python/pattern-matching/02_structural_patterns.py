"""구조 패턴: 시퀀스, 매핑, 클래스 패턴"""

from dataclasses import dataclass


# ── 1. 시퀀스 패턴 ──────────────────────────────────────────────

def analyze_sequence(data: list) -> str:
    """리스트/튜플 디스트럭처링."""
    match data:
        case []:
            return "빈 시퀀스"
        case [single]:
            return f"단일 요소: {single}"
        case [first, second]:
            return f"두 요소: {first}, {second}"
        case [first, *rest]:
            return f"첫 번째: {first}, 나머지: {rest}"


def head_tail(items: list) -> tuple:
    """head/tail 분리 패턴."""
    match items:
        case []:
            return None, []
        case [head, *tail]:
            return head, tail


def analyze_coordinates(points: list) -> str:
    """중첩 시퀀스 패턴."""
    match points:
        case [[x1, y1], [x2, y2]]:
            dx, dy = x2 - x1, y2 - y1
            return f"두 점 사이 거리 벡터: ({dx}, {dy})"
        case [[x, y]]:
            return f"단일 점: ({x}, {y})"
        case []:
            return "점 없음"
        case _:
            return f"점 {len(points)}개"


def classify_command(command: list[str]) -> str:
    """시퀀스 패턴으로 명령어 파싱."""
    match command:
        case ["quit"]:
            return "프로그램 종료"
        case ["go", direction]:
            return f"{direction}(으)로 이동"
        case ["go", direction, steps]:
            return f"{direction}(으)로 {steps}걸음 이동"
        case ["pick", "up", item]:
            return f"{item} 줍기"
        case _:
            return "알 수 없는 명령어"


# ── 2. 매핑 패턴 ──────────────────────────────────────────────

def process_event(event: dict) -> str:
    """딕셔너리 키 기반 매칭."""
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"클릭 이벤트: ({x}, {y})"
        case {"type": "keypress", "key": key}:
            return f"키 입력: {key}"
        case {"type": "scroll", "direction": direction}:
            return f"스크롤: {direction}"
        case {"type": event_type}:
            return f"기타 이벤트: {event_type}"
        case _:
            return "알 수 없는 이벤트"


def extract_user_info(data: dict) -> str:
    """매핑 패턴 — 추가 키가 있어도 매칭된다 (partial match)."""
    match data:
        case {"name": name, "email": email, **rest}:
            extra = f", 추가 정보: {rest}" if rest else ""
            return f"사용자: {name} ({email}){extra}"
        case {"name": name}:
            return f"사용자: {name} (이메일 없음)"
        case _:
            return "사용자 정보 없음"


# ── 3. 클래스 패턴 ──────────────────────────────────────────────

@dataclass
class Point:
    x: float
    y: float


@dataclass
class Circle:
    center: Point
    radius: float


@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float


def describe_point(point: Point) -> str:
    """클래스 패턴 — 속성 기반 매칭."""
    match point:
        case Point(x=0, y=0):
            return "원점"
        case Point(x=0, y=y):
            return f"Y축 위의 점 (y={y})"
        case Point(x=x, y=0):
            return f"X축 위의 점 (x={x})"
        case Point(x=x, y=y):
            return f"일반 점 ({x}, {y})"


def describe_shape(shape) -> str:
    """중첩 클래스 패턴."""
    match shape:
        case Circle(center=Point(x=0, y=0), radius=r):
            return f"원점 중심 원 (반지름={r})"
        case Circle(center=center, radius=r):
            return f"원 (중심=({center.x}, {center.y}), 반지름={r})"
        case Rectangle(top_left=Point(x=x, y=y), width=w, height=h):
            return f"사각형 (좌상단=({x}, {y}), {w}x{h})"
        case _:
            return "알 수 없는 도형"


# __match_args__ 수동 정의 예시
class Color:
    __match_args__ = ("r", "g", "b")

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b


def describe_color(color: Color) -> str:
    """__match_args__로 위치 인자 매칭."""
    match color:
        case Color(0, 0, 0):
            return "검정"
        case Color(255, 255, 255):
            return "흰색"
        case Color(r, 0, 0):
            return f"빨강 계열 (r={r})"
        case Color(r, g, b):
            return f"RGB({r}, {g}, {b})"


if __name__ == "__main__":
    # 시퀀스 패턴
    print("=== 시퀀스 패턴 ===")
    print(analyze_sequence([]))              # 빈 시퀀스
    print(analyze_sequence([42]))            # 단일 요소: 42
    print(analyze_sequence([1, 2]))          # 두 요소: 1, 2
    print(analyze_sequence([1, 2, 3, 4]))    # 첫 번째: 1, 나머지: [2, 3, 4]

    print(head_tail([10, 20, 30]))           # (10, [20, 30])

    print(analyze_coordinates([[0, 0], [3, 4]]))  # 두 점 사이 거리 벡터: (3, 4)

    print(classify_command(["go", "north"]))      # north(으)로 이동
    print(classify_command(["pick", "up", "sword"]))  # sword 줍기

    # 매핑 패턴
    print("\n=== 매핑 패턴 ===")
    print(process_event({"type": "click", "x": 100, "y": 200}))
    print(process_event({"type": "keypress", "key": "Enter"}))

    print(extract_user_info({"name": "Alice", "email": "alice@example.com", "age": 30}))
    print(extract_user_info({"name": "Bob"}))

    # 클래스 패턴
    print("\n=== 클래스 패턴 ===")
    print(describe_point(Point(0, 0)))       # 원점
    print(describe_point(Point(0, 5)))       # Y축 위의 점 (y=5)
    print(describe_point(Point(3, 4)))       # 일반 점 (3, 4)

    print(describe_shape(Circle(Point(0, 0), 5)))      # 원점 중심 원
    print(describe_shape(Rectangle(Point(1, 2), 10, 5)))  # 사각형

    print(describe_color(Color(0, 0, 0)))        # 검정
    print(describe_color(Color(255, 255, 255)))  # 흰색
    print(describe_color(Color(128, 0, 0)))      # 빨강 계열
