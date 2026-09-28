"""Python 언더스코어 예제 테스트"""

import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod01 = importlib.import_module("01_throwaway_variable")
mod02 = importlib.import_module("02_naming_convention")
mod03 = importlib.import_module("03_name_mangling")
mod04 = importlib.import_module("04_dunder_methods")
mod05 = importlib.import_module("05_main_pattern")
mod06 = importlib.import_module("06_numeric_literal")


class TestThrowawayVariable:
    def test_repeat_hello(self):
        result = mod01.repeat_hello(3)
        assert result == ["hello", "hello", "hello"]

    def test_repeat_hello_zero(self):
        assert mod01.repeat_hello(0) == []

    def test_get_first_and_last(self):
        assert mod01.get_first_and_last((1, 2, 3)) == (1, 3)
        assert mod01.get_first_and_last(("a", "b", "c")) == ("a", "c")

    def test_get_first_item(self):
        assert mod01.get_first_item((1, 2, 3, 4, 5)) == 1

    def test_get_last_item(self):
        assert mod01.get_last_item((1, 2, 3, 4, 5)) == 5

    def test_i18n_example(self):
        result = mod01.i18n_example()
        assert result == "Hello, World!"


class TestNamingConvention:
    def test_api_client_connect(self):
        client = mod02.ApiClient("https://api.example.com")
        result = client.connect()
        assert "Connected" in result
        assert client._session_token is not None

    def test_private_function_accessible(self):
        assert mod02._private_function() == "I am private"

    def test_public_function(self):
        assert mod02.public_function() == "I am public"

    def test_create_element_trailing_underscore(self):
        result = mod02.create_element("div", "container")
        assert result == {"type": "div", "class": "container"}

    def test_all_exports(self):
        assert "ApiClient" in mod02.__all__
        assert "public_function" in mod02.__all__
        assert "_private_function" not in mod02.__all__

    def test_import_star_excludes_private(self):
        """from _internal_module import * 시 _로 시작하는 이름이 제외된다."""
        internal = importlib.import_module("_internal_module")
        # __all__이 정의되지 않은 경우, _로 시작하는 이름은 제외됨
        public_names = [name for name in dir(internal) if not name.startswith("_")]
        assert "public_var" in public_names
        assert "public_func" in public_names


class TestNameMangling:
    def test_basic_mangling(self):
        obj = mod03.Base()
        assert obj.public == "public"
        assert obj._protected == "protected"
        assert obj.get_private() == "mangled"

    def test_mangled_name_in_dir(self):
        obj = mod03.Base()
        assert "_Base__private" in dir(obj)

    def test_cannot_access_double_underscore_directly(self):
        obj = mod03.Base()
        with pytest.raises(AttributeError):
            _ = obj.__private

    def test_child_mangling_no_collision(self):
        child = mod03.Child()
        assert child.get_private() == "mangled"  # 부모의 __private
        assert child.get_child_private() == "child_mangled"  # 자식의 __private

    def test_child_has_both_mangled_names(self):
        child = mod03.Child()
        attrs = dir(child)
        assert "_Base__private" in attrs
        assert "_Child__private" in attrs

    def test_account_mangling(self):
        savings = mod03.SavingsAccount(1000, 0.05)
        assert savings.get_balance() == 1000  # 부모의 __balance
        assert savings.get_projected_balance() == 1050.0  # 자식의 __balance


class TestDunderMethods:
    def test_vector_repr(self):
        v = mod04.Vector(3, 4)
        assert repr(v) == "Vector(3, 4)"

    def test_vector_str(self):
        v = mod04.Vector(3, 4)
        assert str(v) == "(3, 4)"

    def test_vector_equality(self):
        assert mod04.Vector(1, 2) == mod04.Vector(1, 2)
        assert mod04.Vector(1, 2) != mod04.Vector(3, 4)

    def test_vector_lt(self):
        v1 = mod04.Vector(1, 0)  # magnitude = 1
        v2 = mod04.Vector(3, 4)  # magnitude = 25
        assert v1 < v2

    def test_vector_add(self):
        v1 = mod04.Vector(1, 2)
        v2 = mod04.Vector(3, 4)
        result = v1 + v2
        assert result == mod04.Vector(4, 6)

    def test_vector_mul(self):
        v = mod04.Vector(2, 3)
        result = v * 3
        assert result == mod04.Vector(6, 9)

    def test_magic_attributes(self):
        attrs = mod04.show_magic_attributes()
        assert attrs["func_name"] == "sample_function"
        assert "샘플 함수" in attrs["func_doc"]
        assert attrs["class_name"] == "Vector"


class TestMainPattern:
    def test_greet(self):
        assert mod05.greet("Python") == "Hello, Python!"

    def test_module_name_when_imported(self):
        # import 시 __name__은 모듈명이 된다
        assert mod05.get_module_name() == "05_main_pattern"


class TestNumericLiteral:
    def test_decimal_values(self):
        assert mod06.MILLION == 1000000
        assert mod06.BILLION == 1000000000
        assert mod06.PRICE == 29900

    def test_hex_values(self):
        assert mod06.HEX_COLOR == 0xFFFFFF
        assert mod06.HEX_MASK == 0xFF00

    def test_binary_values(self):
        assert mod06.BYTE_MASK == 0b11110000
        assert mod06.PERMISSIONS == 0b01110101

    def test_octal_value(self):
        assert mod06.OCTAL_PERM == 0o755

    def test_float_values(self):
        assert abs(mod06.PI - 3.141592) < 1e-6

    def test_format_examples(self):
        result = mod06.format_examples()
        assert result["million"] == 1_000_000
        assert result["hex_color"] == 16_777_215
