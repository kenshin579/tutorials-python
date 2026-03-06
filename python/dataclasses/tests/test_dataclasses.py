"""Dataclasses & attrs 예제 테스트"""

import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod01 = importlib.import_module("01_basic_usage")
mod02 = importlib.import_module("02_field_options")
mod03 = importlib.import_module("03_post_init")
mod04 = importlib.import_module("04_frozen")
mod05 = importlib.import_module("05_inheritance")
mod06 = importlib.import_module("06_comparison")
mod07 = importlib.import_module("07_attrs_intro")
mod08 = importlib.import_module("08_cattrs_serialization")


class TestBasicUsage:
    def test_point_creation(self):
        p = mod01.Point(1.0, 2.0)
        assert p.x == 1.0
        assert p.y == 2.0

    def test_point_equality(self):
        p1 = mod01.Point(1.0, 2.0)
        p2 = mod01.Point(1.0, 2.0)
        p3 = mod01.Point(3.0, 4.0)
        assert p1 == p2
        assert p1 != p3

    def test_point_repr(self):
        p = mod01.Point(1.0, 2.0)
        assert "Point" in repr(p)

    def test_config_defaults(self):
        config = mod01.Config()
        assert config.host == "localhost"
        assert config.port == 8080
        assert config.debug is False

    def test_version_ordering(self):
        v1 = mod01.Version(1, 0, 0)
        v2 = mod01.Version(2, 0, 0)
        v3 = mod01.Version(1, 1, 0)
        assert v1 < v2
        assert v1 < v3
        assert sorted([v2, v3, v1]) == [v1, v3, v2]


class TestFieldOptions:
    def test_default_factory_independent(self):
        s1 = mod02.Student("Alice")
        s2 = mod02.Student("Bob")
        s1.grades.append(90)
        assert s1.grades == [90]
        assert s2.grades == []

    def test_repr_excludes_password(self):
        user = mod02.User("alice", "a@b.com", "secret123")
        assert "secret123" not in repr(user)

    def test_compare_excludes_login_count(self):
        u1 = mod02.User("alice", "a@b.com", "secret", login_count=5)
        u2 = mod02.User("alice", "a@b.com", "secret", login_count=10)
        assert u1 == u2

    def test_init_false_word_count(self):
        article = mod02.Article("Hello", "one two three four five")
        assert article.word_count == 5

    def test_kw_only(self):
        conn = mod02.Connection(host="localhost", port=5432)
        assert conn.host == "localhost"
        assert conn.port == 5432


class TestPostInit:
    def test_temperature_valid(self):
        t = mod03.Temperature(100.0)
        assert t.celsius == 100.0

    def test_temperature_invalid(self):
        with pytest.raises(ValueError, match="절대영도"):
            mod03.Temperature(-300.0)

    def test_rectangle_derived_fields(self):
        rect = mod03.Rectangle(10.0, 5.0)
        assert rect.area == 50.0
        assert rect.perimeter == 30.0

    def test_initvar(self):
        u1 = mod03.User("Alice", "alice@example.com")
        assert u1.email_domain == "example.com"
        assert u1.greeting == "Hello, Alice!"

        u2 = mod03.User("Bob", "bob@test.org", uppercase=True)
        assert u2.greeting == "Hello, BOB!"

    def test_product_total(self):
        product = mod03.Product("Laptop", 1000.0, 2, discount=0.1)
        assert product.total == 1800.0

    def test_product_invalid_price(self):
        with pytest.raises(ValueError, match="가격"):
            mod03.Product("Item", -100.0, 1)


class TestFrozen:
    def test_frozen_immutable(self):
        from dataclasses import FrozenInstanceError

        p = mod04.Point(1.0, 2.0)
        with pytest.raises(FrozenInstanceError):
            p.x = 10.0  # type: ignore[misc]

    def test_frozen_hashable(self):
        red = mod04.Color(255, 0, 0)
        green = mod04.Color(0, 255, 0)
        color_set = {red, green, mod04.Color(255, 0, 0)}
        assert len(color_set) == 2

    def test_color_hex(self):
        red = mod04.Color(255, 0, 0)
        assert red.hex == "#ff0000"

    def test_replace(self):
        from dataclasses import replace

        config = mod04.Config()
        dev = replace(config, debug=True)
        assert dev.debug is True
        assert config.debug is False


class TestInheritance:
    def test_dog_inheritance(self):
        dog = mod05.Dog(name="Buddy", sound="Woof!", breed="Golden")
        assert dog.name == "Buddy"
        assert dog.breed == "Golden"
        assert dog.speak() == "Buddy says Woof!"

    def test_kw_only_inheritance(self):
        child = mod05.ChildKwOnly(name="test", value=1, required_field="required")
        assert child.required_field == "required"

    def test_slots_no_dict(self):
        slotted = mod05.SlottedPoint(1.0, 2.0, 3.0)
        assert not hasattr(slotted, "__dict__")

    def test_regular_has_dict(self):
        regular = mod05.RegularPoint(1.0, 2.0, 3.0)
        assert hasattr(regular, "__dict__")


class TestComparison:
    def test_dataclass_mutable(self):
        dc = mod06.UserDC("Alice", 30, "a@b.com")
        dc.age = 31
        assert dc.age == 31

    def test_namedtuple_immutable(self):
        nt = mod06.UserNT("Alice", 30, "a@b.com")
        with pytest.raises(AttributeError):
            nt.age = 31  # type: ignore[misc]

    def test_namedtuple_indexing(self):
        nt = mod06.UserNT("Alice", 30, "a@b.com")
        assert nt[0] == "Alice"
        assert nt[1] == 30

    def test_typeddict_is_dict(self):
        td: mod06.UserTD = {"name": "Alice", "age": 30, "email": "a@b.com"}
        assert isinstance(td, dict)

    def test_memory_comparison(self):
        sizes = mod06.memory_comparison()
        assert all(v > 0 for v in sizes.values())

    def test_speed_comparison(self):
        speeds = mod06.speed_comparison(n=1000)
        assert all(v > 0 for v in speeds.values())


class TestAttrs:
    def test_define_mutable(self):
        p = mod07.Point(1.0, 2.0)
        p.x = 10.0
        assert p.x == 10.0

    def test_frozen_immutable(self):
        import attr

        color = mod07.Color(255, 0, 0)
        with pytest.raises(attr.exceptions.FrozenInstanceError):
            color.r = 128  # type: ignore[misc]

    def test_validator(self):
        user = mod07.User(name="Alice", age=30, email="alice@example.com")
        assert user.name == "Alice"

    def test_validator_rejects_invalid(self):
        with pytest.raises((ValueError, TypeError)):
            mod07.User(name="Bob", age=-1, email="bob@test.com")

    def test_converter(self):
        record = mod07.Record(id="42", name=123, tags=["a"])  # type: ignore[arg-type]
        assert record.id == 42
        assert isinstance(record.id, int)
        assert record.name == "123"
        assert isinstance(record.name, str)

    def test_factory_independent(self):
        t1 = mod07.TaskList("Work")
        t2 = mod07.TaskList("Personal")
        t1.tasks.append("meeting")
        assert t1.tasks == ["meeting"]
        assert t2.tasks == []


class TestCattrs:
    def test_unstructure(self):
        import cattrs

        user = mod08.User(name="Alice", age=30, email="a@b.com")
        result = cattrs.unstructure(user)
        assert result == {"name": "Alice", "age": 30, "email": "a@b.com"}

    def test_structure(self):
        import cattrs

        data = {"name": "Bob", "age": 25, "email": "bob@test.com"}
        user = cattrs.structure(data, mod08.User)
        assert user.name == "Bob"
        assert user.age == 25

    def test_nested_roundtrip(self):
        import cattrs

        emp = mod08.Employee(
            name="Alice",
            role="Engineer",
            address=mod08.Address(city="Seoul", country="Korea"),
        )
        d = cattrs.unstructure(emp)
        restored = cattrs.structure(d, mod08.Employee)
        assert restored == emp

    def test_list_structure(self):
        import cattrs

        team = mod08.Team(
            name="Backend",
            members=[
                mod08.Employee("Alice", "Lead", mod08.Address("Seoul", "Korea")),
            ],
        )
        d = cattrs.unstructure(team)
        restored = cattrs.structure(d, mod08.Team)
        assert len(restored.members) == 1
        assert restored.members[0].name == "Alice"

    def test_api_response(self):
        import cattrs

        raw = {
            "status": 200,
            "data": [{"name": "Alice", "age": 30, "email": "a@b.com"}],
            "total": 1,
        }
        response = cattrs.structure(raw, mod08.APIResponse)
        assert response.status == 200
        assert len(response.data) == 1
        assert response.data[0].name == "Alice"
