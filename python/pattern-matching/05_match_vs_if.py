"""if/elif vs match/case 비교"""

import timeit
from dataclasses import dataclass


# ── 1. 단순 값 비교 ─────────────────────────────────────────────

# if/elif 방식
def day_type_if(day: str) -> str:
    if day in ("Saturday", "Sunday"):
        return "주말"
    elif day in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
        return "평일"
    else:
        return "알 수 없음"


# match/case 방식
def day_type_match(day: str) -> str:
    match day:
        case "Saturday" | "Sunday":
            return "주말"
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
            return "평일"
        case _:
            return "알 수 없음"


# ── 2. 구조 분해 (match/case가 유리) ────────────────────────────

@dataclass
class Point:
    x: float
    y: float


# if/elif 방식 — 구조 분해를 수동으로 해야 함
def quadrant_if(point: Point) -> str:
    if point.x == 0 and point.y == 0:
        return "원점"
    elif point.x > 0 and point.y > 0:
        return "1사분면"
    elif point.x < 0 and point.y > 0:
        return "2사분면"
    elif point.x < 0 and point.y < 0:
        return "3사분면"
    elif point.x > 0 and point.y < 0:
        return "4사분면"
    else:
        return "축 위"


# match/case 방식 — guard 조건으로 간결하게
def quadrant_match(point: Point) -> str:
    match point:
        case Point(x=0, y=0):
            return "원점"
        case Point(x=x, y=y) if x > 0 and y > 0:
            return "1사분면"
        case Point(x=x, y=y) if x < 0 and y > 0:
            return "2사분면"
        case Point(x=x, y=y) if x < 0 and y < 0:
            return "3사분면"
        case Point(x=x, y=y) if x > 0 and y < 0:
            return "4사분면"
        case _:
            return "축 위"


# ── 3. 중첩 데이터 (match/case가 확실히 유리) ────────────────────

# if/elif 방식
def handle_response_if(response: dict) -> str:
    if isinstance(response, dict):
        status = response.get("status")
        if status == "ok":
            data = response.get("data")
            if isinstance(data, dict):
                items = data.get("items")
                if isinstance(items, list) and len(items) > 0:
                    return f"첫 항목: {items[0]}"
                return "항목 없음"
        elif status == "error":
            error = response.get("error")
            if isinstance(error, dict):
                return f"에러: {error.get('message', '알 수 없음')}"
    return "알 수 없는 형식"


# match/case 방식
def handle_response_match(response: dict) -> str:
    match response:
        case {"status": "ok", "data": {"items": [first, *_]}}:
            return f"첫 항목: {first}"
        case {"status": "ok", "data": {"items": []}}:
            return "항목 없음"
        case {"status": "error", "error": {"message": msg}}:
            return f"에러: {msg}"
        case _:
            return "알 수 없는 형식"


# ── 4. 범위 비교 (if/elif가 나은 경우) ──────────────────────────

# if/elif 방식 — 범위 비교에 자연스러움
def temperature_if(temp: float) -> str:
    if temp < 0:
        return "영하"
    elif temp < 10:
        return "추움"
    elif temp < 20:
        return "선선"
    elif temp < 30:
        return "따뜻"
    else:
        return "더움"


# match/case 방식 — guard 필수, 오히려 장황
def temperature_match(temp: float) -> str:
    match temp:
        case t if t < 0:
            return "영하"
        case t if t < 10:
            return "추움"
        case t if t < 20:
            return "선선"
        case t if t < 30:
            return "따뜻"
        case _:
            return "더움"


# ── 5. 성능 비교 ────────────────────────────────────────────────

def benchmark():
    """if/elif와 match/case 성능 비교."""
    n = 500_000
    test_data = [200, 301, 404, 500, 418] * (n // 5)

    def run_if():
        for status in test_data:
            if status == 200:
                r = "OK"
            elif status == 301:
                r = "Redirect"
            elif status == 404:
                r = "Not Found"
            elif status == 500:
                r = "Error"
            else:
                r = "Unknown"

    def run_match():
        for status in test_data:
            match status:
                case 200:
                    r = "OK"
                case 301:
                    r = "Redirect"
                case 404:
                    r = "Not Found"
                case 500:
                    r = "Error"
                case _:
                    r = "Unknown"

    if_time = timeit.timeit(run_if, number=3) / 3
    match_time = timeit.timeit(run_match, number=3) / 3

    print(f"  if/elif:    {if_time:.4f}s ({n}건)")
    print(f"  match/case: {match_time:.4f}s ({n}건)")
    ratio = match_time / if_time
    print(f"  비율: match/case는 if/elif 대비 {ratio:.2f}x")


if __name__ == "__main__":
    # 단순 값 비교
    print("=== 단순 값 비교 ===")
    print(f"  if/elif:    {day_type_if('Saturday')}")
    print(f"  match/case: {day_type_match('Saturday')}")

    # 구조 분해
    print("\n=== 구조 분해 ===")
    p = Point(3, 4)
    print(f"  if/elif:    {quadrant_if(p)}")
    print(f"  match/case: {quadrant_match(p)}")

    # 중첩 데이터
    print("\n=== 중첩 데이터 ===")
    resp = {"status": "ok", "data": {"items": ["apple", "banana"]}}
    print(f"  if/elif:    {handle_response_if(resp)}")
    print(f"  match/case: {handle_response_match(resp)}")

    # 범위 비교
    print("\n=== 범위 비교 ===")
    print(f"  if/elif:    {temperature_if(25)}")
    print(f"  match/case: {temperature_match(25)}")

    # 성능
    print("\n=== 성능 비교 ===")
    benchmark()

    # 요약
    print("\n=== 요약 ===")
    print("  match/case 유리: 구조 분해, 중첩 데이터 매칭, 타입별 분기")
    print("  if/elif 유리:    범위 비교, 단순 조건, 복잡한 boolean 조합")
    print("  성능:            거의 동일 (미미한 차이)")
