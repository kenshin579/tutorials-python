"""실전 패턴: 플러그인 시스템, Repository 패턴"""

import unittest
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ============================================================
# 패턴 1: Protocol 기반 플러그인 시스템
# ============================================================
@runtime_checkable
class Plugin(Protocol):
    name: str

    def execute(self, data: dict) -> dict: ...


class LoggingPlugin:
    name = "logging"

    def execute(self, data: dict) -> dict:
        data["logged"] = True
        return data


class ValidationPlugin:
    name = "validation"

    def execute(self, data: dict) -> dict:
        if "value" in data and isinstance(data["value"], int) and data["value"] > 0:
            data["valid"] = True
        else:
            data["valid"] = False
        return data


class TransformPlugin:
    name = "transform"

    def execute(self, data: dict) -> dict:
        if "value" in data:
            data["value"] = data["value"] * 2
        return data


class PluginManager:
    def __init__(self):
        self._plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        if isinstance(plugin, Plugin):
            self._plugins.append(plugin)
        else:
            raise TypeError(f"{type(plugin).__name__} does not satisfy Plugin protocol")

    def run(self, data: dict) -> dict:
        for plugin in self._plugins:
            data = plugin.execute(data)
        return data

    @property
    def plugin_names(self) -> list[str]:
        return [p.name for p in self._plugins]


# ============================================================
# 패턴 2: ABC 기반 Repository 패턴
# ============================================================
class Entity:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Entity) and self.id == other.id

    def __repr__(self):
        return f"Entity(id={self.id}, name='{self.name}')"


class Repository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Entity | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Entity]:
        pass

    @abstractmethod
    def save(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    def exists(self, id: int) -> bool:
        """일반 메서드: 기본 구현 제공"""
        return self.find_by_id(id) is not None


class InMemoryRepository(Repository):
    def __init__(self):
        self._store: dict[int, Entity] = {}

    def find_by_id(self, id: int) -> Entity | None:
        return self._store.get(id)

    def find_all(self) -> list[Entity]:
        return list(self._store.values())

    def save(self, entity: Entity) -> None:
        self._store[entity.id] = entity

    def delete(self, id: int) -> bool:
        if id in self._store:
            del self._store[id]
            return True
        return False


class TestPluginSystem(unittest.TestCase):
    def test_register_and_run_plugins(self):
        manager = PluginManager()
        manager.register(LoggingPlugin())
        manager.register(ValidationPlugin())
        manager.register(TransformPlugin())

        result = manager.run({"value": 5})
        assert result["logged"] is True
        assert result["valid"] is True
        assert result["value"] == 10

    def test_plugin_names(self):
        manager = PluginManager()
        manager.register(LoggingPlugin())
        manager.register(ValidationPlugin())
        assert manager.plugin_names == ["logging", "validation"]

    def test_invalid_plugin_rejected(self):
        manager = PluginManager()
        with self.assertRaises(TypeError):
            manager.register("not a plugin")

    def test_plugin_isinstance_check(self):
        assert isinstance(LoggingPlugin(), Plugin)
        assert isinstance(ValidationPlugin(), Plugin)


class TestRepositoryPattern(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.entity1 = Entity(1, "Alice")
        self.entity2 = Entity(2, "Bob")

    def test_save_and_find(self):
        self.repo.save(self.entity1)
        found = self.repo.find_by_id(1)
        assert found == self.entity1

    def test_find_all(self):
        self.repo.save(self.entity1)
        self.repo.save(self.entity2)
        all_entities = self.repo.find_all()
        assert len(all_entities) == 2

    def test_delete(self):
        self.repo.save(self.entity1)
        assert self.repo.delete(1) is True
        assert self.repo.find_by_id(1) is None
        assert self.repo.delete(999) is False

    def test_exists(self):
        """ABC의 일반 메서드 exists()는 기본 구현 사용"""
        self.repo.save(self.entity1)
        assert self.repo.exists(1) is True
        assert self.repo.exists(999) is False

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Repository()


if __name__ == "__main__":
    unittest.main()
