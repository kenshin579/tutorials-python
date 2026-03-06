"""실전 활용: 커맨드 파서, 상태 머신, JSON 파싱, AST 처리"""

from dataclasses import dataclass
from enum import Enum, auto


# ── 1. 커맨드 파서 ──────────────────────────────────────────────

def parse_command(raw: str) -> str:
    """CLI 인자 분기 처리."""
    match raw.strip().split():
        case ["quit" | "exit" | "q"]:
            return "종료"
        case ["help"]:
            return "도움말 표시"
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            return f"{direction}(으)로 이동"
        case ["attack", target]:
            return f"{target} 공격"
        case ["pick", "up", item]:
            return f"{item} 줍기"
        case ["use", item, "on", target]:
            return f"{target}에게 {item} 사용"
        case ["say", *words]:
            return f'말하기: "{" ".join(words)}"'
        case []:
            return "빈 입력"
        case _:
            return "알 수 없는 명령어"


# ── 2. 상태 머신 ──────────────────────────────────────────────

class State(Enum):
    IDLE = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    ERROR = auto()


class Event(Enum):
    CONNECT = auto()
    CONNECTED = auto()
    DISCONNECT = auto()
    DISCONNECTED = auto()
    ERROR = auto()
    RETRY = auto()


def transition(state: State, event: Event) -> State:
    """이벤트 기반 상태 전환."""
    match (state, event):
        case (State.IDLE, Event.CONNECT):
            return State.CONNECTING
        case (State.CONNECTING, Event.CONNECTED):
            return State.CONNECTED
        case (State.CONNECTING, Event.ERROR):
            return State.ERROR
        case (State.CONNECTED, Event.DISCONNECT):
            return State.DISCONNECTING
        case (State.DISCONNECTING, Event.DISCONNECTED):
            return State.IDLE
        case (State.ERROR, Event.RETRY):
            return State.CONNECTING
        case (_, Event.ERROR):
            return State.ERROR
        case _:
            return state  # 상태 유지


# ── 3. JSON/API 응답 파싱 ──────────────────────────────────────

def handle_api_response(response: dict) -> str:
    """REST API 응답 구조별 분기."""
    match response:
        # 페이지네이션 응답
        case {
            "status": "ok",
            "data": list(items),
            "meta": {"page": page, "total_pages": total}
        }:
            return f"페이지 {page}/{total} — {len(items)}건"
        # 단일 객체 응답
        case {"status": "ok", "data": {"id": id_, "type": type_}}:
            return f"객체: {type_}#{id_}"
        # 빈 응답
        case {"status": "ok", "data": None}:
            return "데이터 없음"
        # 인증 에러
        case {"status": "error", "error": {"code": 401 | 403, "message": msg}}:
            return f"인증 에러: {msg}"
        # 일반 에러
        case {"status": "error", "error": {"code": code, "message": msg}}:
            return f"에러 [{code}]: {msg}"
        case _:
            return "알 수 없는 응답 형식"


def extract_notifications(payload: dict) -> list[str]:
    """중첩 JSON 구조에서 알림 메시지를 추출한다."""
    results = []
    match payload:
        case {"notifications": [*notifications]}:
            for notif in notifications:
                match notif:
                    case {"type": "mention", "from": sender, "message": msg}:
                        results.append(f"@{sender}: {msg}")
                    case {"type": "like", "from": sender, "post_id": pid}:
                        results.append(f"{sender}님이 게시물 #{pid} 좋아요")
                    case {"type": type_, **rest}:
                        results.append(f"기타 알림: {type_}")
        case _:
            results.append("알림 없음")
    return results


# ── 4. AST 노드 처리 ──────────────────────────────────────────

@dataclass
class Num:
    value: float


@dataclass
class Add:
    left: object
    right: object


@dataclass
class Mul:
    left: object
    right: object


@dataclass
class Neg:
    operand: object


def evaluate(expr) -> float:
    """간단한 수식 AST를 재귀적으로 평가한다."""
    match expr:
        case Num(value=v):
            return v
        case Add(left=l, right=r):
            return evaluate(l) + evaluate(r)
        case Mul(left=l, right=r):
            return evaluate(l) * evaluate(r)
        case Neg(operand=e):
            return -evaluate(e)
        case _:
            raise ValueError(f"알 수 없는 노드: {expr}")


def format_expr(expr) -> str:
    """AST를 사람이 읽기 쉬운 문자열로 변환한다."""
    match expr:
        case Num(value=v):
            return str(v) if v == int(v) else f"{v}"
        case Add(left=l, right=r):
            return f"({format_expr(l)} + {format_expr(r)})"
        case Mul(left=l, right=r):
            return f"({format_expr(l)} * {format_expr(r)})"
        case Neg(operand=e):
            return f"(-{format_expr(e)})"
        case _:
            return "?"


if __name__ == "__main__":
    # 커맨드 파서
    print("=== 커맨드 파서 ===")
    print(parse_command("go north"))         # north(으)로 이동
    print(parse_command("attack dragon"))    # dragon 공격
    print(parse_command("pick up sword"))    # sword 줍기
    print(parse_command("use potion on ally"))  # ally에게 potion 사용
    print(parse_command("say hello world"))  # 말하기: "hello world"
    print(parse_command("quit"))             # 종료

    # 상태 머신
    print("\n=== 상태 머신 ===")
    state = State.IDLE
    for event in [Event.CONNECT, Event.CONNECTED, Event.DISCONNECT, Event.DISCONNECTED]:
        new_state = transition(state, event)
        print(f"  {state.name} + {event.name} → {new_state.name}")
        state = new_state

    # 에러 → 재시도
    state = transition(State.CONNECTING, Event.ERROR)
    print(f"  CONNECTING + ERROR → {state.name}")
    state = transition(state, Event.RETRY)
    print(f"  ERROR + RETRY → {state.name}")

    # JSON/API 파싱
    print("\n=== JSON/API 파싱 ===")
    print(handle_api_response({
        "status": "ok",
        "data": [1, 2, 3],
        "meta": {"page": 1, "total_pages": 5}
    }))
    print(handle_api_response({
        "status": "error",
        "error": {"code": 401, "message": "Unauthorized"}
    }))

    notifications = extract_notifications({
        "notifications": [
            {"type": "mention", "from": "Alice", "message": "확인해주세요"},
            {"type": "like", "from": "Bob", "post_id": 42},
        ]
    })
    for n in notifications:
        print(f"  {n}")

    # AST 처리
    print("\n=== AST 처리 ===")
    # (2 + 3) * 4
    expr = Mul(Add(Num(2), Num(3)), Num(4))
    print(f"  수식: {format_expr(expr)}")
    print(f"  결과: {evaluate(expr)}")

    # -(5 + 3)
    expr2 = Neg(Add(Num(5), Num(3)))
    print(f"  수식: {format_expr(expr2)}")
    print(f"  결과: {evaluate(expr2)}")
