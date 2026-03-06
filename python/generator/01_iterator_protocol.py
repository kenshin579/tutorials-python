"""Iterator 프로토콜: __iter__, __next__, StopIteration"""


# 1. 커스텀 Iterator 클래스
class CountDown:
    """카운트다운 Iterator - __iter__와 __next__ 직접 구현"""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# 2. for 루프 내부 동작 시연
def for_loop_internals():
    """for 루프가 내부적으로 iter() → next() → StopIteration을 처리하는 흐름"""
    countdown = CountDown(3)
    iterator = iter(countdown)  # __iter__() 호출

    print("=== for 루프 내부 동작 시연 ===")
    while True:
        try:
            value = next(iterator)  # __next__() 호출
            print(f"next() → {value}")
        except StopIteration:
            print("StopIteration 발생 → 루프 종료")
            break


# 3. Iterable vs Iterator 구분
class Range:
    """Iterable 객체 - 여러 번 순회 가능 (매번 새 Iterator 생성)"""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __iter__(self):
        return RangeIterator(self.start, self.end)


class RangeIterator:
    """Range의 Iterator - 한 번만 순회 가능"""

    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


if __name__ == "__main__":
    # CountDown 사용
    print("=== CountDown ===")
    for n in CountDown(5):
        print(n, end=" ")
    print()

    # for 루프 내부 동작
    for_loop_internals()

    # Iterable vs Iterator
    print("\n=== Iterable (여러 번 순회 가능) ===")
    r = Range(1, 4)
    print("1차:", list(r))
    print("2차:", list(r))
