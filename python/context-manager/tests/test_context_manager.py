"""Context Manager 예제 테스트"""

import asyncio
import importlib
import io
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mod_custom = importlib.import_module("custom_context_manager")
mod_decorator = importlib.import_module("contextmanager_decorator")
mod_practical = importlib.import_module("practical_examples")
mod_async = importlib.import_module("async_context_manager")

ManagedResource = mod_custom.ManagedResource
SuppressError = mod_custom.SuppressError
DatabaseConnection = mod_custom.DatabaseConnection
managed_resource = mod_decorator.managed_resource
timer = mod_decorator.timer
transaction = mod_practical.transaction
FakeDB = mod_practical.FakeDB
temp_env = mod_practical.temp_env
locked = mod_practical.locked
AsyncDBConnection = mod_async.AsyncDBConnection


# --- custom_context_manager ---
class TestCustomContextManager:
    def test_managed_resource(self):
        with ManagedResource("test") as res:
            assert res.name == "test"

    def test_suppress_error(self):
        with SuppressError(ValueError):
            raise ValueError("should be suppressed")
        # 여기까지 도달하면 성공

    def test_suppress_does_not_catch_other(self):
        try:
            with SuppressError(ValueError):
                raise TypeError("not suppressed")
            assert False, "should not reach here"
        except TypeError:
            pass  # 예상대로 전파됨

    def test_database_connection(self):
        with DatabaseConnection("test:5432") as db:
            assert db.connected is True
            result = db.execute("SELECT 1")
            assert "SELECT 1" in result
        assert db.connected is False

    def test_database_connection_error(self):
        try:
            with DatabaseConnection("test:5432") as db:
                raise RuntimeError("error")
        except RuntimeError:
            assert db.connected is False


# --- contextmanager_decorator ---
class TestContextManagerDecorator:
    def test_managed_resource_decorator(self):
        with managed_resource("테스트") as name:
            assert name == "테스트"

    def test_timer(self, capsys):
        with timer("test"):
            sum(range(100))
        captured = capsys.readouterr()
        assert "test:" in captured.out


# --- practical_examples ---
class TestPracticalExamples:
    def test_transaction_commit(self):
        db = FakeDB()
        with transaction(db) as d:
            d.set("key", "value")
        assert db.get("key") == "value"

    def test_transaction_rollback(self):
        db = FakeDB()
        db.set("key", "original")
        try:
            with transaction(db) as d:
                d.set("key", "changed")
                raise ValueError("rollback!")
        except ValueError:
            pass
        assert db.get("key") == "original"

    def test_temp_env(self):
        os.environ.pop("TEST_VAR_XYZ", None)
        with temp_env(TEST_VAR_XYZ="hello"):
            assert os.environ["TEST_VAR_XYZ"] == "hello"
        assert os.environ.get("TEST_VAR_XYZ") is None

    def test_locked(self):
        lock = threading.Lock()
        with locked(lock):
            assert lock.locked()
        assert not lock.locked()

    def test_locked_timeout(self):
        lock = threading.Lock()
        lock.acquire()
        try:
            with locked(lock, timeout=0.01):
                pass
            assert False, "should not reach here"
        except TimeoutError:
            pass
        finally:
            lock.release()


# --- async_context_manager ---
class TestAsyncContextManager:
    def test_async_db_connection(self):
        async def _test():
            async with AsyncDBConnection("test:5432") as db:
                assert db.connected is True
                result = await db.query("SELECT 1")
                assert "SELECT 1" in result
            assert db.connected is False

        asyncio.run(_test())
