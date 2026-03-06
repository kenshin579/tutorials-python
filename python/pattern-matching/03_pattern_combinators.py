"""패턴 조합: OR 패턴, guard 조건, 중첩 패턴"""

from dataclasses import dataclass


# ── 1. OR 패턴 ──────────────────────────────────────────────────

def classify_http_status(status: int) -> str:
    """OR 패턴으로 여러 값을 하나의 케이스로 묶는다."""
    match status:
        case 200 | 201 | 204:
            return "성공"
        case 301 | 302 | 307:
            return "리다이렉트"
        case 400 | 401 | 403 | 404:
            return "클라이언트 에러"
        case 500 | 502 | 503:
            return "서버 에러"
        case _:
            return f"기타: {status}"


def classify_char(ch: str) -> str:
    """OR 패턴으로 문자 분류."""
    match ch:
        case "+" | "-":
            return "부호 연산자"
        case "*" | "/":
            return "곱셈/나눗셈 연산자"
        case "(" | ")":
            return "괄호"
        case _:
            return "기타"


@dataclass
class Move:
    direction: str


@dataclass
class Attack:
    target: str


@dataclass
class Heal:
    target: str


def describe_action(action) -> str:
    """OR 패턴과 캡처 변수 — 양쪽 모두 동일 변수 바인딩 필요."""
    match action:
        case Attack(target=name) | Heal(target=name):
            return f"대상: {name}"
        case Move(direction=d):
            return f"이동: {d}"
        case _:
            return "알 수 없는 행동"


# ── 2. guard 조건 ──────────────────────────────────────────────

def classify_age(age: int) -> str:
    """guard 조건으로 범위 기반 분류."""
    match age:
        case n if n < 0:
            return "잘못된 나이"
        case n if n < 13:
            return "어린이"
        case n if n < 20:
            return "청소년"
        case n if n < 65:
            return "성인"
        case _:
            return "시니어"


def evaluate_score(score: int, curve: int = 0) -> str:
    """guard 조건으로 조정 점수 기반 등급 판정."""
    match score + curve:
        case s if s >= 90:
            return "A"
        case s if s >= 80:
            return "B"
        case s if s >= 70:
            return "C"
        case s if s >= 60:
            return "D"
        case _:
            return "F"


def process_request(request: dict) -> str:
    """매핑 패턴 + guard 조건 조합."""
    match request:
        case {"method": "GET", "path": path} if path.startswith("/api/"):
            return f"API 조회: {path}"
        case {"method": "GET", "path": path}:
            return f"페이지 조회: {path}"
        case {"method": "POST", "path": path, "body": body} if len(body) > 1000:
            return f"대용량 POST: {path} ({len(body)}bytes)"
        case {"method": "POST", "path": path}:
            return f"POST 요청: {path}"
        case _:
            return "지원하지 않는 요청"


# ── 3. 중첩 패턴 ──────────────────────────────────────────────

def extract_first_user_name(data: dict) -> str:
    """깊은 구조의 JSON 데이터에서 값 추출."""
    match data:
        case {"users": [{"name": name}, *_]}:
            return f"첫 번째 사용자: {name}"
        case {"users": []}:
            return "사용자 없음"
        case _:
            return "users 필드 없음"


def parse_api_response(response: dict) -> str:
    """API 응답 구조별 분기 처리."""
    match response:
        case {"status": "ok", "data": {"items": [first, *rest]}}:
            return f"성공 — 첫 항목: {first}, 나머지 {len(rest)}개"
        case {"status": "ok", "data": {"items": []}}:
            return "성공 — 결과 없음"
        case {"status": "error", "error": {"code": code, "message": msg}}:
            return f"에러 [{code}]: {msg}"
        case {"status": "ok", "data": data}:
            return f"성공 — 데이터: {data}"
        case _:
            return "알 수 없는 응답 형식"


def analyze_config(config: dict) -> str:
    """중첩 매핑 + 시퀀스 패턴."""
    match config:
        case {"database": {"host": host, "port": port}, "cache": {"enabled": True}}:
            return f"DB: {host}:{port}, 캐시 활성"
        case {"database": {"host": host, "port": port}}:
            return f"DB: {host}:{port}, 캐시 비활성"
        case _:
            return "설정 없음"


if __name__ == "__main__":
    # OR 패턴
    print("=== OR 패턴 ===")
    print(classify_http_status(200))   # 성공
    print(classify_http_status(404))   # 클라이언트 에러
    print(classify_http_status(503))   # 서버 에러

    print(classify_char("+"))   # 부호 연산자
    print(classify_char("*"))   # 곱셈/나눗셈 연산자

    print(describe_action(Attack("dragon")))  # 대상: dragon
    print(describe_action(Heal("knight")))    # 대상: knight

    # guard 조건
    print("\n=== guard 조건 ===")
    print(classify_age(5))     # 어린이
    print(classify_age(15))    # 청소년
    print(classify_age(30))    # 성인
    print(classify_age(70))    # 시니어

    print(evaluate_score(85))         # A (커브 0)
    print(evaluate_score(85, 5))      # A (커브 5)
    print(evaluate_score(75, 5))      # B

    print(process_request({"method": "GET", "path": "/api/users"}))
    print(process_request({"method": "GET", "path": "/home"}))

    # 중첩 패턴
    print("\n=== 중첩 패턴 ===")
    print(extract_first_user_name({"users": [{"name": "Alice"}, {"name": "Bob"}]}))
    print(extract_first_user_name({"users": []}))

    print(parse_api_response({
        "status": "ok",
        "data": {"items": ["a", "b", "c"]}
    }))
    print(parse_api_response({
        "status": "error",
        "error": {"code": 404, "message": "Not Found"}
    }))

    print(analyze_config({
        "database": {"host": "localhost", "port": 5432},
        "cache": {"enabled": True}
    }))
