"""Generator 예제 테스트"""

import importlib
import sys
import os

# 부모 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 숫자로 시작하는 모듈을 importlib로 로드
mod01 = importlib.import_module("01_iterator_protocol")
mod02 = importlib.import_module("02_generator_basics")
mod04 = importlib.import_module("04_send_throw_close")
mod05 = importlib.import_module("05_yield_from")
mod08 = importlib.import_module("08_practical_patterns")

CountDown = mod01.CountDown
Range = mod01.Range
simple_generator = mod02.simple_generator
countdown_gen = mod02.countdown_gen
running_average = mod04.running_average
echo = mod04.echo
chain_with_yield_from = mod05.chain_with_yield_from
flatten = mod05.flatten
yield_from_examples = mod05.yield_from_examples
fibonacci = mod08.fibonacci
id_generator = mod08.id_generator
pipe = mod08.pipe
double = mod08.double
keep_even = mod08.keep_even
take = mod08.take


# --- 01_iterator_protocol ---
class TestIteratorProtocol:
    def test_countdown(self):
        assert list(CountDown(5)) == [5, 4, 3, 2, 1]

    def test_countdown_zero(self):
        assert list(CountDown(0)) == []

    def test_range_iterable(self):
        r = Range(1, 4)
        assert list(r) == [1, 2, 3]
        assert list(r) == [1, 2, 3]  # 여러 번 순회 가능


# --- 02_generator_basics ---
class TestGeneratorBasics:
    def test_simple_generator(self):
        assert list(simple_generator()) == [1, 2, 3]

    def test_countdown_gen(self):
        assert list(countdown_gen(5)) == [5, 4, 3, 2, 1]

    def test_countdown_gen_zero(self):
        assert list(countdown_gen(0)) == []


# --- 03_generator_expression ---
class TestGeneratorExpression:
    def test_list_vs_generator_same_result(self):
        n = 100
        list_comp = [x**2 for x in range(n)]
        gen_expr = list(x**2 for x in range(n))
        assert list_comp == gen_expr

    def test_generator_smaller_memory(self):
        n = 100_000
        list_comp = [x for x in range(n)]
        gen_expr = (x for x in range(n))
        assert sys.getsizeof(gen_expr) < sys.getsizeof(list_comp)


# --- 04_send_throw_close ---
class TestSendThrowClose:
    def test_running_average(self):
        avg = running_average()
        next(avg)  # 초기화
        assert avg.send(10) == 10.0
        assert avg.send(20) == 15.0
        assert avg.send(30) == 20.0

    def test_echo(self):
        e = echo()
        assert next(e) == "ready"
        assert e.send("hello") == "echo: hello"
        assert e.send("world") == "echo: world"


# --- 05_yield_from ---
class TestYieldFrom:
    def test_chain(self):
        assert list(chain_with_yield_from([1, 2], [3, 4])) == [1, 2, 3, 4]

    def test_flatten(self):
        assert list(flatten([1, [2, 3], [4, [5, 6]], 7])) == [1, 2, 3, 4, 5, 6, 7]

    def test_yield_from_examples(self):
        assert list(yield_from_examples()) == ["A", "B", "C", 0, 1, 2, 10, 20, 30]


# --- 08_practical_patterns ---
class TestPracticalPatterns:
    def test_fibonacci(self):
        fib = fibonacci()
        first_10 = [next(fib) for _ in range(10)]
        assert first_10 == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_id_generator(self):
        ids = id_generator("USR")
        assert next(ids) == "USR-000001"
        assert next(ids) == "USR-000002"

    def test_pipe(self):
        result = list(pipe(range(1, 10), keep_even, double, take(3)))
        assert result == [4, 8, 12]
