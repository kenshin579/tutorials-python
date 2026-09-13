"""pytest-benchmark 데모: 성능 벤치마크

실행 방법:
    pytest tests/test_benchmark.py
    pytest tests/test_benchmark.py --benchmark-save=baseline
    pytest tests/test_benchmark.py --benchmark-compare=0001_baseline
"""

from src.calculator import Calculator


# === 기본 벤치마크 ===


def test_sort_performance(benchmark):
    """sorted() 함수의 실행 시간을 측정한다"""
    data = list(range(1000, 0, -1))
    result = benchmark(sorted, data)
    assert result == list(range(1, 1001))


def test_list_comprehension_vs_map(benchmark):
    """리스트 컴프리헨션의 성능을 측정한다"""
    data = list(range(1000))

    def square_with_comprehension():
        return [x**2 for x in data]

    result = benchmark(square_with_comprehension)
    assert len(result) == 1000


# === pedantic 모드 (정밀 측정) ===


def test_factorial_pedantic(benchmark):
    """pedantic 모드: rounds와 iterations를 직접 지정하여 정밀 측정"""
    calc = Calculator()
    benchmark.pedantic(calc.factorial, args=(10,), rounds=100, iterations=10)


def test_power_pedantic(benchmark):
    """power 함수의 정밀 벤치마크"""
    calc = Calculator()
    benchmark.pedantic(calc.power, args=(2, 20), rounds=100, iterations=10)


# === 비교용 벤치마크 ===


def test_string_concat_plus(benchmark):
    """문자열 + 연산자 성능"""

    def concat_plus():
        result = ""
        for i in range(100):
            result += str(i)
        return result

    benchmark(concat_plus)


def test_string_concat_join(benchmark):
    """문자열 join() 성능"""

    def concat_join():
        return "".join(str(i) for i in range(100))

    benchmark(concat_join)
