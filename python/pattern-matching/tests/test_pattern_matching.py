"""패턴 매칭 예제 테스트"""

import importlib
import sys
import os

import pytest

# 부모 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 숫자로 시작하는 모듈을 importlib로 로드
mod01 = importlib.import_module("01_basic_patterns")
mod02 = importlib.import_module("02_structural_patterns")
mod03 = importlib.import_module("03_pattern_combinators")
mod04 = importlib.import_module("04_practical_examples")
mod05 = importlib.import_module("05_match_vs_if")

# mod01
http_status_message = mod01.http_status_message
greet_by_language = mod01.greet_by_language
check_value = mod01.check_value
describe_value = mod01.describe_value
parse_greeting = mod01.parse_greeting
classify_number = mod01.classify_number
describe_color = mod01.describe_color
check_http_status = mod01.check_http_status
BasicColor = mod01.Color

# mod02
Point = mod02.Point
Circle = mod02.Circle
Rectangle = mod02.Rectangle
analyze_sequence = mod02.analyze_sequence
head_tail = mod02.head_tail
analyze_coordinates = mod02.analyze_coordinates
classify_command = mod02.classify_command
process_event = mod02.process_event
extract_user_info = mod02.extract_user_info
describe_point = mod02.describe_point
describe_shape = mod02.describe_shape

# mod03
classify_http_status = mod03.classify_http_status
classify_char = mod03.classify_char
Attack = mod03.Attack
Heal = mod03.Heal
Move = mod03.Move
describe_action = mod03.describe_action
classify_age = mod03.classify_age
evaluate_score = mod03.evaluate_score
process_request = mod03.process_request
extract_first_user_name = mod03.extract_first_user_name
parse_api_response = mod03.parse_api_response
analyze_config = mod03.analyze_config

# mod04
parse_command = mod04.parse_command
State = mod04.State
Event = mod04.Event
transition = mod04.transition
handle_api_response = mod04.handle_api_response
extract_notifications = mod04.extract_notifications
Num = mod04.Num
Add = mod04.Add
Mul = mod04.Mul
Neg = mod04.Neg
evaluate = mod04.evaluate
format_expr = mod04.format_expr

# mod05
day_type_if = mod05.day_type_if
day_type_match = mod05.day_type_match
MPoint = mod05.Point
quadrant_if = mod05.quadrant_if
quadrant_match = mod05.quadrant_match
handle_response_if = mod05.handle_response_if
handle_response_match = mod05.handle_response_match
temperature_if = mod05.temperature_if
temperature_match = mod05.temperature_match


# ── 01_basic_patterns ─────────────────────────────────────────

class TestHttpStatusMessage:
    def test_known_status(self):
        assert http_status_message(200) == "OK"
        assert http_status_message(404) == "Not Found"
        assert http_status_message(500) == "Internal Server Error"

    def test_unknown_status(self):
        assert http_status_message(418) == "Unknown status: 418"


class TestGreetByLanguage:
    def test_known_languages(self):
        assert greet_by_language("ko") == "안녕하세요"
        assert greet_by_language("en") == "Hello"
        assert greet_by_language("ja") == "こんにちは"

    def test_unknown_language(self):
        assert greet_by_language("fr") == "Hi"


class TestCheckValue:
    def test_bool_none(self):
        assert check_value(True) == "boolean True"
        assert check_value(False) == "boolean False"
        assert check_value(None) == "None value"

    def test_zero(self):
        assert check_value(0) == "zero"

    def test_other(self):
        assert check_value(42) == "other: 42"


class TestDescribeValue:
    def test_zero(self):
        assert describe_value(0) == "zero"

    def test_capture(self):
        assert describe_value(42) == "captured: 42"
        assert describe_value("hello") == "captured: hello"


class TestParseGreeting:
    def test_hello(self):
        assert parse_greeting("hello World") == "인사 대상: World"

    def test_other_greeting(self):
        assert parse_greeting("hi Alice") == "hi -> Alice"

    def test_unknown(self):
        assert parse_greeting("a b c") == "알 수 없는 형식"


class TestClassifyNumber:
    def test_values(self):
        assert classify_number(0) == "zero"
        assert classify_number(1) == "one"
        assert classify_number(99) == "other"


class TestDescribeColorBasic:
    def test_enum_colors(self):
        assert describe_color(BasicColor.RED) == "빨간색"
        assert describe_color(BasicColor.GREEN) == "초록색"
        assert describe_color(BasicColor.BLUE) == "파란색"


class TestCheckHttpStatus:
    def test_known_codes(self):
        assert check_http_status(200) == "성공"
        assert check_http_status(404) == "찾을 수 없음"
        assert check_http_status(500) == "서버 에러"

    def test_unknown_code(self):
        assert check_http_status(201) == "기타"


# ── 02_structural_patterns ─────────────────────────────────────

class TestAnalyzeSequence:
    def test_empty(self):
        assert analyze_sequence([]) == "빈 시퀀스"

    def test_single(self):
        assert analyze_sequence([42]) == "단일 요소: 42"

    def test_two(self):
        assert analyze_sequence([1, 2]) == "두 요소: 1, 2"

    def test_many(self):
        assert analyze_sequence([1, 2, 3, 4]) == "첫 번째: 1, 나머지: [2, 3, 4]"


class TestHeadTail:
    def test_empty(self):
        assert head_tail([]) == (None, [])

    def test_non_empty(self):
        assert head_tail([10, 20, 30]) == (10, [20, 30])


class TestAnalyzeCoordinates:
    def test_two_points(self):
        assert analyze_coordinates([[0, 0], [3, 4]]) == "두 점 사이 거리 벡터: (3, 4)"

    def test_single_point(self):
        assert analyze_coordinates([[5, 10]]) == "단일 점: (5, 10)"


class TestClassifyCommand:
    def test_quit(self):
        assert classify_command(["quit"]) == "프로그램 종료"

    def test_go(self):
        assert classify_command(["go", "north"]) == "north(으)로 이동"

    def test_pick_up(self):
        assert classify_command(["pick", "up", "sword"]) == "sword 줍기"


class TestProcessEvent:
    def test_click(self):
        assert process_event({"type": "click", "x": 10, "y": 20}) == "클릭 이벤트: (10, 20)"

    def test_keypress(self):
        assert process_event({"type": "keypress", "key": "Enter"}) == "키 입력: Enter"


class TestExtractUserInfo:
    def test_full_info(self):
        result = extract_user_info({"name": "Alice", "email": "a@b.com"})
        assert "Alice" in result and "a@b.com" in result

    def test_name_only(self):
        assert extract_user_info({"name": "Bob"}) == "사용자: Bob (이메일 없음)"


class TestDescribePoint:
    def test_origin(self):
        assert describe_point(Point(0, 0)) == "원점"

    def test_y_axis(self):
        assert describe_point(Point(0, 5)) == "Y축 위의 점 (y=5)"

    def test_general(self):
        assert describe_point(Point(3, 4)) == "일반 점 (3, 4)"


class TestDescribeShape:
    def test_circle_at_origin(self):
        assert describe_shape(Circle(Point(0, 0), 5)) == "원점 중심 원 (반지름=5)"

    def test_rectangle(self):
        result = describe_shape(Rectangle(Point(1, 2), 10, 5))
        assert "사각형" in result


# ── 03_pattern_combinators ─────────────────────────────────────

class TestClassifyHttpStatus:
    def test_success(self):
        assert classify_http_status(200) == "성공"
        assert classify_http_status(201) == "성공"

    def test_client_error(self):
        assert classify_http_status(404) == "클라이언트 에러"

    def test_server_error(self):
        assert classify_http_status(503) == "서버 에러"


class TestClassifyChar:
    def test_operators(self):
        assert classify_char("+") == "부호 연산자"
        assert classify_char("*") == "곱셈/나눗셈 연산자"


class TestDescribeAction:
    def test_or_pattern_with_capture(self):
        assert describe_action(Attack("dragon")) == "대상: dragon"
        assert describe_action(Heal("knight")) == "대상: knight"
        assert describe_action(Move("north")) == "이동: north"


class TestClassifyAge:
    def test_ranges(self):
        assert classify_age(-1) == "잘못된 나이"
        assert classify_age(5) == "어린이"
        assert classify_age(15) == "청소년"
        assert classify_age(30) == "성인"
        assert classify_age(70) == "시니어"


class TestEvaluateScore:
    def test_grades(self):
        assert evaluate_score(95) == "A"
        assert evaluate_score(85) == "B"
        assert evaluate_score(75) == "C"
        assert evaluate_score(55) == "F"

    def test_with_curve(self):
        assert evaluate_score(85, 5) == "A"


class TestExtractFirstUserName:
    def test_with_users(self):
        assert extract_first_user_name({"users": [{"name": "Alice"}]}) == "첫 번째 사용자: Alice"

    def test_empty_users(self):
        assert extract_first_user_name({"users": []}) == "사용자 없음"

    def test_no_users_field(self):
        assert extract_first_user_name({}) == "users 필드 없음"


class TestParseApiResponse:
    def test_success_with_items(self):
        resp = {"status": "ok", "data": {"items": ["a", "b", "c"]}}
        assert "첫 항목: a" in parse_api_response(resp)

    def test_error(self):
        resp = {"status": "error", "error": {"code": 404, "message": "Not Found"}}
        assert "에러 [404]" in parse_api_response(resp)


# ── 04_practical_examples ──────────────────────────────────────

class TestParseCommand:
    def test_quit(self):
        assert parse_command("quit") == "종료"
        assert parse_command("exit") == "종료"

    def test_go(self):
        assert parse_command("go north") == "north(으)로 이동"

    def test_attack(self):
        assert parse_command("attack dragon") == "dragon 공격"

    def test_say(self):
        assert parse_command("say hello world") == '말하기: "hello world"'

    def test_empty(self):
        assert parse_command("") == "빈 입력"


class TestStateMachine:
    def test_normal_flow(self):
        assert transition(State.IDLE, Event.CONNECT) == State.CONNECTING
        assert transition(State.CONNECTING, Event.CONNECTED) == State.CONNECTED
        assert transition(State.CONNECTED, Event.DISCONNECT) == State.DISCONNECTING
        assert transition(State.DISCONNECTING, Event.DISCONNECTED) == State.IDLE

    def test_error_and_retry(self):
        assert transition(State.CONNECTING, Event.ERROR) == State.ERROR
        assert transition(State.ERROR, Event.RETRY) == State.CONNECTING

    def test_global_error(self):
        assert transition(State.CONNECTED, Event.ERROR) == State.ERROR


class TestHandleApiResponse:
    def test_pagination(self):
        resp = {
            "status": "ok",
            "data": [1, 2, 3],
            "meta": {"page": 1, "total_pages": 5}
        }
        assert "페이지 1/5" in handle_api_response(resp)

    def test_auth_error(self):
        resp = {"status": "error", "error": {"code": 401, "message": "Unauthorized"}}
        assert "인증 에러" in handle_api_response(resp)


class TestExtractNotifications:
    def test_mixed_notifications(self):
        payload = {
            "notifications": [
                {"type": "mention", "from": "Alice", "message": "확인"},
                {"type": "like", "from": "Bob", "post_id": 42},
            ]
        }
        results = extract_notifications(payload)
        assert len(results) == 2
        assert "@Alice" in results[0]
        assert "Bob" in results[1]


class TestAST:
    def test_evaluate(self):
        expr = Mul(Add(Num(2), Num(3)), Num(4))
        assert evaluate(expr) == 20.0

    def test_neg(self):
        expr = Neg(Add(Num(5), Num(3)))
        assert evaluate(expr) == -8.0

    def test_format(self):
        expr = Add(Num(1), Num(2))
        assert format_expr(expr) == "(1 + 2)"

    def test_unknown_node(self):
        with pytest.raises(ValueError):
            evaluate("invalid")


# ── 05_match_vs_if ─────────────────────────────────────────────

class TestDayType:
    def test_consistency(self):
        for day in ["Monday", "Saturday", "Sunday", "xyz"]:
            assert day_type_if(day) == day_type_match(day)


class TestQuadrant:
    def test_consistency(self):
        test_points = [MPoint(0, 0), MPoint(1, 1), MPoint(-1, 1), MPoint(-1, -1), MPoint(1, -1), MPoint(0, 5)]
        for p in test_points:
            assert quadrant_if(p) == quadrant_match(p)


class TestHandleResponse:
    def test_consistency(self):
        responses = [
            {"status": "ok", "data": {"items": ["a", "b"]}},
            {"status": "ok", "data": {"items": []}},
            {"status": "error", "error": {"message": "fail"}},
            {"invalid": True},
        ]
        for resp in responses:
            assert handle_response_if(resp) == handle_response_match(resp)


class TestTemperature:
    def test_consistency(self):
        for t in [-5, 5, 15, 25, 35]:
            assert temperature_if(t) == temperature_match(t)
