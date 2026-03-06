"""Generator 함수: yield, 생명주기, next() 실행 흐름"""

import inspect


# 1. yield vs return
def simple_return():
    """일반 함수 - 값을 반환하고 종료"""
    return 1
    return 2  # noqa: 도달 불가


def simple_generator():
    """Generator 함수 - yield로 값을 생산하고 상태 보존"""
    yield 1
    yield 2
    yield 3


# 2. next() 호출 시 실행 흐름 시각화
def verbose_generator():
    """실행 흐름을 print로 시각화"""
    print("  [generator] 시작")
    yield "첫 번째"
    print("  [generator] 첫 번째 yield 이후 재개")
    yield "두 번째"
    print("  [generator] 두 번째 yield 이후 재개")
    yield "세 번째"
    print("  [generator] 함수 끝 → StopIteration 발생")


# 3. Generator 생명주기 상태 확인
def lifecycle_demo():
    """inspect.getgeneratorstate()로 Generator 상태 확인"""

    def countdown(n):
        while n > 0:
            yield n
            n -= 1

    gen = countdown(3)

    print(f"생성 직후:     {inspect.getgeneratorstate(gen)}")  # GEN_CREATED
    print(f"next() → {next(gen)}")
    print(f"next() 후:     {inspect.getgeneratorstate(gen)}")  # GEN_SUSPENDED
    print(f"next() → {next(gen)}")
    print(f"next() → {next(gen)}")

    try:
        next(gen)
    except StopIteration:
        pass

    print(f"소진 후:       {inspect.getgeneratorstate(gen)}")  # GEN_CLOSED


# 4. Generator로 CountDown 재구현 (Iterator 클래스 vs Generator 비교)
def countdown_gen(start: int):
    """Generator 버전 카운트다운 - Iterator 클래스보다 훨씬 간결"""
    while start > 0:
        yield start
        start -= 1


if __name__ == "__main__":
    print("=== yield vs return ===")
    print(f"return: {simple_return()}")
    print(f"generator: {list(simple_generator())}")

    print("\n=== next() 실행 흐름 ===")
    gen = verbose_generator()
    for i in range(3):
        print(f"[caller] next() 호출 #{i + 1}")
        value = next(gen)
        print(f"[caller] 받은 값: {value}")

    print("\n=== Generator 생명주기 ===")
    lifecycle_demo()

    print("\n=== Generator 카운트다운 ===")
    print(list(countdown_gen(5)))
