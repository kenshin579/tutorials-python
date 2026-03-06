"""yield from: 서브 제네레이터 위임"""


# 1. yield from 없이 vs 있을 때 비교
def chain_without_yield_from(*iterables):
    """yield from 없이 중첩 순회"""
    for it in iterables:
        for item in it:
            yield item


def chain_with_yield_from(*iterables):
    """yield from으로 간결하게"""
    for it in iterables:
        yield from it


# 2. yield from으로 이터러블 평탄화
def flatten(nested):
    """중첩 리스트 평탄화"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


# 3. 반환값 처리
def sub_generator():
    """서브 제네레이터 - return 값을 전달"""
    total = 0
    while True:
        value = yield
        if value is None:
            return total  # StopIteration(total)으로 변환
        total += value


def delegating_generator():
    """yield from으로 서브 제네레이터의 반환값 받기"""
    result = yield from sub_generator()
    print(f"  서브 제네레이터 반환값: {result}")
    yield result


# 4. 문자열/range도 yield from 가능
def yield_from_examples():
    """다양한 이터러블에 yield from 사용"""
    yield from "ABC"
    yield from range(3)
    yield from [10, 20, 30]


if __name__ == "__main__":
    # 비교
    print("=== yield from 비교 ===")
    a = [1, 2, 3]
    b = [4, 5, 6]
    print(f"without: {list(chain_without_yield_from(a, b))}")
    print(f"with:    {list(chain_with_yield_from(a, b))}")

    # 평탄화
    print("\n=== 중첩 리스트 평탄화 ===")
    nested = [1, [2, 3], [4, [5, 6]], 7]
    print(f"flatten: {list(flatten(nested))}")

    # 반환값 처리
    print("\n=== 반환값 처리 ===")
    dg = delegating_generator()
    next(dg)  # 초기화
    dg.send(10)
    dg.send(20)
    dg.send(30)
    try:
        result = dg.send(None)  # sub_generator 종료 → return total
        print(f"  최종 결과: {result}")
    except StopIteration:
        pass

    # 다양한 이터러블
    print("\n=== 다양한 이터러블 ===")
    print(list(yield_from_examples()))
