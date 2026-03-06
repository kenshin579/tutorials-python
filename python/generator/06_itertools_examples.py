"""itertools 활용 예제"""

from itertools import (
    chain,
    combinations,
    count,
    cycle,
    dropwhile,
    filterfalse,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    takewhile,
    zip_longest,
)


# 1. 무한 이터레이터
def infinite_iterators():
    """count, cycle, repeat"""
    # count: 시작값부터 step만큼 증가
    print("count(10, 2):", list(islice(count(10, 2), 5)))

    # cycle: 반복 순환
    print("cycle('AB'):", list(islice(cycle("AB"), 6)))

    # repeat: 값 반복 (횟수 제한 가능)
    print("repeat(7, 3):", list(repeat(7, 3)))


# 2. 조합 이터레이터
def combining_iterators():
    """chain, islice, zip_longest"""
    # chain: 여러 이터러블 연결
    print("chain:", list(chain([1, 2], [3, 4], [5])))

    # islice: 슬라이싱 (start, stop, step)
    print("islice:", list(islice(range(100), 0, 10, 2)))

    # zip_longest: 짧은 쪽 fillvalue로 채움
    print("zip_longest:", list(zip_longest([1, 2, 3], ["a", "b"], fillvalue="-")))


# 3. 필터링
def filtering_iterators():
    """takewhile, dropwhile, filterfalse"""
    data = [1, 3, 5, 2, 4, 6, 1]

    # takewhile: 조건이 True인 동안 가져옴 (False 나오면 중단)
    print("takewhile(<5):", list(takewhile(lambda x: x < 5, data)))

    # dropwhile: 조건이 True인 동안 건너뜀 (False부터 전부 가져옴)
    print("dropwhile(<5):", list(dropwhile(lambda x: x < 5, data)))

    # filterfalse: 조건이 False인 것만 가져옴 (filter의 반대)
    print("filterfalse(짝수):", list(filterfalse(lambda x: x % 2 == 0, data)))


# 4. 그룹핑
def grouping_iterators():
    """groupby - 정렬 필수 주의"""
    data = [
        {"name": "Alice", "dept": "Engineering"},
        {"name": "Bob", "dept": "Engineering"},
        {"name": "Charlie", "dept": "Marketing"},
        {"name": "Diana", "dept": "Marketing"},
        {"name": "Eve", "dept": "Engineering"},
    ]

    # 정렬하지 않으면 같은 키가 분리됨
    print("정렬 없이 groupby:")
    for key, group in groupby(data, key=lambda x: x["dept"]):
        print(f"  {key}: {[p['name'] for p in group]}")

    # 정렬 후 groupby
    print("\n정렬 후 groupby:")
    sorted_data = sorted(data, key=lambda x: x["dept"])
    for key, group in groupby(sorted_data, key=lambda x: x["dept"]):
        print(f"  {key}: {[p['name'] for p in group]}")


# 5. 조합론
def combinatoric_iterators():
    """product, permutations, combinations"""
    # product: 데카르트 곱
    print("product:", list(product("AB", "12")))

    # permutations: 순열
    print("permutations:", list(permutations("ABC", 2)))

    # combinations: 조합
    print("combinations:", list(combinations("ABCD", 2)))


if __name__ == "__main__":
    print("=== 무한 이터레이터 ===")
    infinite_iterators()

    print("\n=== 조합 이터레이터 ===")
    combining_iterators()

    print("\n=== 필터링 ===")
    filtering_iterators()

    print("\n=== 그룹핑 ===")
    grouping_iterators()

    print("\n=== 조합론 ===")
    combinatoric_iterators()
