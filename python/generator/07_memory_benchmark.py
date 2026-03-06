"""메모리 효율 비교: list vs generator 벤치마크"""

import sys
import time
import tracemalloc


def process_with_list(n: int) -> int:
    """리스트로 전체 데이터를 메모리에 올려서 처리"""
    data = [x**2 for x in range(n)]
    return sum(data)


def process_with_generator(n: int) -> int:
    """Generator로 한 건씩 처리"""
    data = (x**2 for x in range(n))
    return sum(data)


def measure_memory_and_time(func, n: int) -> tuple[int, float, float]:
    """함수 실행 시 메모리 사용량과 실행 시간 측정"""
    tracemalloc.start()
    start_time = time.perf_counter()

    result = func(n)

    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, peak_memory, end_time - start_time


def benchmark():
    """list vs generator 벤치마크 비교"""
    sizes = [10_000, 100_000, 1_000_000]

    print(f"{'N':>12} | {'방식':<12} | {'메모리 (KB)':>14} | {'시간 (ms)':>10} | {'결과 일치'}")
    print("-" * 75)

    for n in sizes:
        result_list, mem_list, time_list = measure_memory_and_time(process_with_list, n)
        result_gen, mem_gen, time_gen = measure_memory_and_time(process_with_generator, n)

        match = result_list == result_gen

        print(f"{n:>12,} | {'List':<12} | {mem_list / 1024:>14,.1f} | {time_list * 1000:>10.2f} | ")
        print(f"{'':>12} | {'Generator':<12} | {mem_gen / 1024:>14,.1f} | {time_gen * 1000:>10.2f} | {match}")
        print("-" * 75)


def getsizeof_comparison():
    """sys.getsizeof로 객체 자체 크기 비교"""
    n = 1_000_000
    list_obj = [x for x in range(n)]
    gen_obj = (x for x in range(n))

    list_size = sys.getsizeof(list_obj)
    gen_size = sys.getsizeof(gen_obj)

    print(f"\n=== sys.getsizeof (N={n:,}) ===")
    print(f"List:      {list_size:>12,} bytes ({list_size / 1024 / 1024:.1f} MB)")
    print(f"Generator: {gen_size:>12,} bytes ({gen_size / 1024:.1f} KB)")
    print(f"배율:      {list_size / gen_size:>12,.0f}x")


if __name__ == "__main__":
    print("=== List vs Generator 벤치마크 ===")
    benchmark()
    getsizeof_comparison()
