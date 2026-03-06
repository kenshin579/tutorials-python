"""Type Hints 예제 테스트"""

import asyncio
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod01 = importlib.import_module("01_basic_types")
mod02 = importlib.import_module("02_optional_union_literal")
mod03 = importlib.import_module("03_generics")
mod04 = importlib.import_module("04_protocol")
mod05 = importlib.import_module("05_callable_awaitable")
mod06 = importlib.import_module("06_utility_types")


class TestBasicTypes:
    def test_greet(self):
        assert mod01.greet("Python") == "Hello, Python!"

    def test_add(self):
        assert mod01.add(3, 5) == 8

    def test_process_items(self):
        assert mod01.process_items(["a", "b", "c", "d"], 2) == ["a", "b"]

    def test_get_or_default(self):
        assert mod01.get_or_default({"a": 1}, "a", 0) == 1
        assert mod01.get_or_default({"a": 1}, "b", 99) == 99


class TestOptionalUnionLiteral:
    def test_find_user(self):
        assert mod02.find_user(1) == "Alice"
        assert mod02.find_user(99) is None

    def test_greet_user(self):
        assert mod02.greet_user() == "Hello, Guest!"
        assert mod02.greet_user("Alice") == "Hello, Alice!"

    def test_process_id(self):
        assert mod02.process_id(42) == "ID-000042"
        assert mod02.process_id("abc") == "ABC"

    def test_parse_value(self):
        assert mod02.parse_value("42") == 42
        assert mod02.parse_value("3.14") == 3.14
        assert mod02.parse_value("hello") == "hello"

    def test_open_file(self):
        assert "write" in mod02.open_file("data.txt", "write")

    def test_handle_response(self):
        assert mod02.handle_response(200) == "Success"
        assert mod02.handle_response(404) == "Client Error"
        assert mod02.handle_response(500) == "Server Error"


class TestGenerics:
    def test_first(self):
        assert mod03.first([1, 2, 3]) == 1
        assert mod03.first(["a", "b"]) == "a"

    def test_identity(self):
        assert mod03.identity(42) == 42
        assert mod03.identity("hello") == "hello"

    def test_make_speak(self):
        assert mod03.make_speak(mod03.Dog()) == "Woof!"
        assert mod03.make_speak(mod03.Cat()) == "Meow!"

    def test_stack(self):
        stack = mod03.Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.peek() == 3
        assert stack.pop() == 3
        assert len(stack) == 2

    def test_pair(self):
        pair = mod03.Pair("key", 42)
        assert pair.key == "key"
        assert pair.value == 42


class TestProtocol:
    def test_render(self):
        assert mod04.render(mod04.Circle()) == "○"
        assert mod04.render(mod04.Square()) == "□"

    def test_check_item(self):
        assert mod04.check_item([1, 2, 3], 2) is True
        assert mod04.check_item([], 1) is False

    def test_runtime_checkable(self):
        assert isinstance(mod04.FileResource(), mod04.Closeable)
        assert not isinstance("string", mod04.Closeable)


class TestCallable:
    def test_apply(self):
        assert mod05.apply(mod05.add, 3, 5) == 8
        assert mod05.apply(mod05.multiply, 3, 5) == 15

    def test_create_multiplier(self):
        double = mod05.create_multiplier(2)
        assert double(5) == 10

    def test_process_async(self):
        async def _test():
            result = await mod05.process_async(mod05.fetch_data("test"))
            assert "TEST" in result

        asyncio.run(_test())


class TestUtilityTypes:
    def test_dot_product(self):
        assert mod06.dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == 32.0

    def test_transpose(self):
        assert mod06.transpose([[1.0, 2.0], [3.0, 4.0]]) == [[1.0, 3.0], [2.0, 4.0]]

    def test_is_str_list(self):
        assert mod06.is_str_list(["a", "b"]) is True
        assert mod06.is_str_list([1, "b"]) is False

    def test_process_items(self):
        assert mod06.process_items(["a", "b", "c"]) == "a, b, c"

    def test_create_user(self):
        user = {"name": "Alice", "age": 30, "email": "a@b.com"}
        assert "Alice" in mod06.create_user(user)

    def test_get_config(self):
        config = mod06.get_config({"port": 9090})
        assert config["port"] == 9090
