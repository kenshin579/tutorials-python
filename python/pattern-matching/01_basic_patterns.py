"""기본 패턴: 리터럴, 캡처, 와일드카드, 상수 매칭"""

from enum import Enum


# ── 1. 리터럴 패턴 ──────────────────────────────────────────────

def http_status_message(status: int) -> str:
    """HTTP 상태 코드를 메시지로 변환한다."""
    match status:
        case 200:
            return "OK"
        case 301:
            return "Moved Permanently"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return f"Unknown status: {status}"


def greet_by_language(lang: str) -> str:
    """언어 코드에 따른 인사말을 반환한다."""
    match lang:
        case "ko":
            return "안녕하세요"
        case "en":
            return "Hello"
        case "ja":
            return "こんにちは"
        case _:
            return "Hi"


def check_value(value) -> str:
    """다양한 리터럴 타입 매칭 예시."""
    match value:
        case True:
            return "boolean True"
        case False:
            return "boolean False"
        case None:
            return "None value"
        case 0:
            return "zero"
        case _:
            return f"other: {value}"


# ── 2. 캡처 패턴 ──────────────────────────────────────────────

def describe_value(value) -> str:
    """캡처 패턴으로 변수에 바인딩한다."""
    match value:
        case 0:
            return "zero"
        case x:  # 어떤 값이든 매칭하고 x에 바인딩
            return f"captured: {x}"


def parse_greeting(message: str) -> str:
    """문자열 분리 후 캡처 패턴 활용."""
    match message.split():
        case ["hello", name]:
            return f"인사 대상: {name}"
        case [greeting, name]:  # 두 단어 모두 캡처
            return f"{greeting} -> {name}"
        case _:
            return "알 수 없는 형식"


# ── 3. 와일드카드 패턴 ──────────────────────────────────────────

def classify_number(n: int) -> str:
    """와일드카드 패턴으로 기본 분기를 처리한다."""
    match n:
        case 0:
            return "zero"
        case 1:
            return "one"
        case _:  # catch-all, 값을 바인딩하지 않음
            return "other"


# ── 4. 상수 매칭 (점 표기 필수) ──────────────────────────────────

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class HttpStatus:
    OK = 200
    NOT_FOUND = 404
    ERROR = 500


def describe_color(color: Color) -> str:
    """Enum 상수 매칭 — 점 표기(dotted name) 필수."""
    match color:
        case Color.RED:
            return "빨간색"
        case Color.GREEN:
            return "초록색"
        case Color.BLUE:
            return "파란색"
        case _:
            return "알 수 없는 색"


def check_http_status(code: int) -> str:
    """클래스 속성을 상수로 매칭한다."""
    match code:
        case HttpStatus.OK:
            return "성공"
        case HttpStatus.NOT_FOUND:
            return "찾을 수 없음"
        case HttpStatus.ERROR:
            return "서버 에러"
        case _:
            return "기타"


if __name__ == "__main__":
    # 리터럴 패턴
    print("=== 리터럴 패턴 ===")
    print(http_status_message(200))   # OK
    print(http_status_message(404))   # Not Found
    print(http_status_message(418))   # Unknown status: 418

    print(greet_by_language("ko"))    # 안녕하세요
    print(greet_by_language("en"))    # Hello

    # bool/None은 리터럴 패턴으로 먼저 매칭됨 (int 0보다 우선)
    print(check_value(True))          # boolean True
    print(check_value(None))          # None value
    print(check_value(0))             # zero

    # 캡처 패턴
    print("\n=== 캡처 패턴 ===")
    print(describe_value(0))          # zero
    print(describe_value(42))         # captured: 42

    print(parse_greeting("hello World"))  # 인사 대상: World
    print(parse_greeting("hi Alice"))     # hi -> Alice

    # 와일드카드 패턴
    print("\n=== 와일드카드 패턴 ===")
    print(classify_number(0))         # zero
    print(classify_number(1))         # one
    print(classify_number(99))        # other

    # 상수 매칭
    print("\n=== 상수 매칭 ===")
    print(describe_color(Color.RED))    # 빨간색
    print(describe_color(Color.BLUE))   # 파란색
    print(check_http_status(200))       # 성공
    print(check_http_status(404))       # 찾을 수 없음
