"""Python Enum 예제 테스트"""

import importlib
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod01 = importlib.import_module("01_basic_enum")
mod02 = importlib.import_module("02_auto_value")
mod03 = importlib.import_module("03_int_str_enum")
mod04 = importlib.import_module("04_flag_enum")
mod05 = importlib.import_module("05_custom_methods")
mod06 = importlib.import_module("06_comparison_serialize")
mod07 = importlib.import_module("07_practical_patterns")


class TestBasicEnum:
    def test_access_by_attribute(self):
        assert mod01.Color.RED.value == 1

    def test_access_by_name(self):
        assert mod01.Color["GREEN"] is mod01.Color.GREEN

    def test_access_by_value(self):
        assert mod01.Color(3) is mod01.Color.BLUE

    def test_name_and_value(self):
        name, value = mod01.get_name_and_value(mod01.Color.RED)
        assert name == "RED"
        assert value == 1

    def test_iteration(self):
        colors = mod01.list_all_colors()
        assert len(colors) == 3
        assert colors[0] is mod01.Color.RED

    def test_singleton(self):
        assert mod01.is_singleton() is True

    def test_direction_string_values(self):
        assert mod01.Direction.NORTH.value == "N"

    def test_access_enum_members(self):
        a, b, c = mod01.access_enum_members()
        assert a is b is c


class TestAutoValue:
    def test_priority_auto_values(self):
        assert mod02.Priority.LOW.value == 1
        assert mod02.Priority.CRITICAL.value == 4

    def test_ordinal_enum_starts_from_zero(self):
        assert mod02.OrdinalEnum.FIRST.value == 0
        assert mod02.OrdinalEnum.SECOND.value == 1
        assert mod02.OrdinalEnum.THIRD.value == 2

    def test_str_enum_auto_lowercase(self):
        assert mod02.Status.ACTIVE == "active"
        assert mod02.Status.INACTIVE == "inactive"
        assert mod02.Status.PENDING == "pending"


class TestIntStrEnum:
    def test_int_enum_comparison(self):
        result = mod03.int_enum_comparison()
        assert result["inteum_eq_int"] is True
        assert result["intenum_gt"] is True
        assert result["intenum_arithmetic"] == 201
        assert result["pure_eq_int"] is False

    def test_str_enum_usage(self):
        result = mod03.str_enum_usage()
        assert result["format"] == "level: debug"
        assert result["upper"] == "DEBUG"
        assert result["concat"] == "log_info"
        assert result["eq_str"] is True

    def test_http_status_values(self):
        assert mod03.HttpStatus.OK == 200
        assert mod03.HttpStatus.NOT_FOUND == 404


class TestFlagEnum:
    def test_permission_combine(self):
        rw = mod04.Permission.READ | mod04.Permission.WRITE
        assert mod04.Permission.READ in rw
        assert mod04.Permission.WRITE in rw
        assert mod04.Permission.EXECUTE not in rw

    def test_check_permission(self):
        rw = mod04.Permission.READ_WRITE
        assert mod04.check_permission(rw, mod04.Permission.READ) is True
        assert mod04.check_permission(rw, mod04.Permission.EXECUTE) is False

    def test_combine_permissions(self):
        result = mod04.combine_permissions(mod04.Permission.READ, mod04.Permission.EXECUTE)
        assert mod04.Permission.READ in result
        assert mod04.Permission.EXECUTE in result

    def test_all_permission(self):
        assert mod04.Permission.READ in mod04.Permission.ALL
        assert mod04.Permission.WRITE in mod04.Permission.ALL
        assert mod04.Permission.EXECUTE in mod04.Permission.ALL

    def test_file_permission(self):
        assert mod04.FilePermission.OWNER_ALL == 0o700
        assert mod04.FilePermission.DEFAULT == 0o755


class TestCustomMethods:
    def test_planet_surface_gravity(self):
        assert mod05.Planet.EARTH.surface_gravity > 0

    def test_planet_weight_on(self):
        earth_weight = 70.0
        mars_weight = mod05.Planet.MARS.weight_on(earth_weight)
        assert mars_weight < earth_weight  # 화성 중력은 지구보다 약함

    def test_planet_str(self):
        s = str(mod05.Planet.EARTH)
        assert "Earth" in s

    def test_planet_format_short(self):
        assert f"{mod05.Planet.EARTH:short}" == "Earth"

    def test_season_from_month(self):
        assert mod05.Season.from_month(3) is mod05.Season.SPRING
        assert mod05.Season.from_month(7) is mod05.Season.SUMMER
        assert mod05.Season.from_month(10) is mod05.Season.AUTUMN
        assert mod05.Season.from_month(1) is mod05.Season.WINTER


class TestComparisonSerialize:
    def test_comparison(self):
        result = mod06.comparison_examples()
        assert result["enum_is"] is True
        assert result["enum_eq"] is True
        assert result["enum_eq_int"] is False
        assert result["intenum_eq_int"] is True

    def test_json_serialize(self):
        data = {"color": mod06.Color.RED}
        json_str = mod06.enum_to_json(data)
        parsed = json.loads(json_str)
        assert parsed["color"]["name"] == "RED"
        assert parsed["color"]["value"] == 1

    def test_json_deserialize(self):
        data = {"color": mod06.Color.RED}
        json_str = mod06.enum_to_json(data)
        restored = mod06.enum_from_json(json_str, mod06.Color)
        assert restored["color"] is mod06.Color.RED

    def test_db_value_roundtrip(self):
        db_val = mod06.to_db_value(mod06.Color.GREEN)
        assert db_val == 2
        restored = mod06.from_db_value(mod06.Color, db_val)
        assert restored is mod06.Color.GREEN


class TestPracticalPatterns:
    def test_order_status_transitions(self):
        pending = mod07.OrderStatus.PENDING
        assert mod07.OrderStatus.CONFIRMED in pending.next_status()
        assert mod07.OrderStatus.CANCELLED in pending.next_status()
        assert mod07.OrderStatus.DELIVERED not in pending.next_status()

    def test_can_transition_to(self):
        assert mod07.OrderStatus.PENDING.can_transition_to(mod07.OrderStatus.CONFIRMED)
        assert not mod07.OrderStatus.DELIVERED.can_transition_to(mod07.OrderStatus.PENDING)

    def test_http_code_category(self):
        assert mod07.HttpCode.OK.category == "Success"
        assert mod07.HttpCode.NOT_FOUND.category == "Client Error"
        assert mod07.HttpCode.INTERNAL_ERROR.category == "Server Error"

    def test_http_code_is_error(self):
        assert not mod07.HttpCode.OK.is_error
        assert mod07.HttpCode.NOT_FOUND.is_error

    def test_environment_config(self):
        dev_config = mod07.Environment.DEV.config
        assert dev_config["debug"] is True
        prod_config = mod07.Environment.PROD.config
        assert prod_config["debug"] is False

    def test_handle_order_match_case(self):
        assert "확인 중" in mod07.handle_order(mod07.OrderStatus.PENDING)
        assert "배송 완료" in mod07.handle_order(mod07.OrderStatus.DELIVERED)
        assert "취소" in mod07.handle_order(mod07.OrderStatus.CANCELLED)
