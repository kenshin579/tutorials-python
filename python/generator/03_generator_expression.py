"""Generator Expression vs List Comprehension"""

import sys


# 1. 문법 비교
def syntax_comparison():
    """Generator Expression vs List Comprehension 문법"""
    n = 10

    # List Comprehension - 즉시 전체 리스트 생성 (eager)
    list_comp = [x**2 for x in range(n)]

    # Generator Expression - 요청 시 하나씩 생성 (lazy)
    gen_expr = (x**2 for x in range(n))

    print(f"List Comprehension: {list_comp}")
    print(f"Generator Expression: {gen_expr}")
    print(f"Generator → list: {list(gen_expr)}")


# 2. 메모리 사용량 비교
def memory_comparison():
    """sys.getsizeof()로 메모리 차이 측정"""
    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print(f"{'N':>12} | {'List (bytes)':>15} | {'Generator (bytes)':>18} | {'배율':>8}")
    print("-" * 65)

    for n in sizes:
        list_comp = [x**2 for x in range(n)]
        gen_expr = (x**2 for x in range(n))

        list_size = sys.getsizeof(list_comp)
        gen_size = sys.getsizeof(gen_expr)

        print(f"{n:>12,} | {list_size:>15,} | {gen_size:>18,} | {list_size / gen_size:>7.0f}x")


# 3. 선택 기준
def when_to_use():
    """언제 어떤 것을 선택해야 하는지"""
    data = range(100)

    # Generator Expression 적합: 한 번만 순회, 대용량 데이터
    total = sum(x**2 for x in data)
    print(f"합계 (Generator Expression): {total}")

    # List Comprehension 적합: 여러 번 사용, 인덱싱 필요, 작은 데이터
    squares = [x**2 for x in range(10)]
    print(f"첫 번째 값: {squares[0]}, 마지막 값: {squares[-1]}")
    print(f"길이: {len(squares)}")

    # 중첩 가능
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = list(x for row in matrix for x in row)
    print(f"평탄화: {flat}")


if __name__ == "__main__":
    print("=== 문법 비교 ===")
    syntax_comparison()

    print("\n=== 메모리 사용량 비교 ===")
    memory_comparison()

    print("\n=== 선택 기준 ===")
    when_to_use()
