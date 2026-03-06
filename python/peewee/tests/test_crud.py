"""CRUD 연산 테스트."""

import pytest

from models import User


class TestCreate:
    def test_create_single(self):
        user = User.create(username="alice", email="alice@example.com")
        assert user.id is not None
        assert User.select().count() == 1

    def test_insert_many(self):
        users = [
            {"username": "bob", "email": "bob@example.com"},
            {"username": "charlie", "email": "charlie@example.com"},
        ]
        User.insert_many(users).execute()
        assert User.select().count() == 2


class TestRead:
    def test_get_by_id(self):
        user = User.create(username="alice", email="alice@example.com")
        found = User.get_by_id(user.id)
        assert found.username == "alice"

    def test_get_by_id_not_found(self):
        with pytest.raises(User.DoesNotExist):
            User.get_by_id(999)

    def test_select_where(self):
        User.create(username="alice", email="a@e.com", is_active=True)
        User.create(username="bob", email="b@e.com", is_active=False)

        active = list(User.select().where(User.is_active == True))
        assert len(active) == 1
        assert active[0].username == "alice"


class TestUpdate:
    def test_update_instance(self):
        user = User.create(username="alice", email="old@e.com")
        user.email = "new@e.com"
        user.save()

        refreshed = User.get_by_id(user.id)
        assert refreshed.email == "new@e.com"

    def test_bulk_update(self):
        User.create(username="alice", email="a@e.com", is_active=True)
        User.create(username="bob", email="b@e.com", is_active=True)

        rows = User.update(is_active=False).where(User.username == "bob").execute()
        assert rows == 1
        assert User.get(User.username == "bob").is_active is False


class TestDelete:
    def test_delete_instance(self):
        user = User.create(username="alice", email="a@e.com")
        user.delete_instance()
        assert User.select().count() == 0

    def test_bulk_delete(self):
        User.create(username="alice", email="a@e.com", is_active=False)
        User.create(username="bob", email="b@e.com", is_active=True)

        rows = User.delete().where(User.is_active == False).execute()
        assert rows == 1
        assert User.select().count() == 1


class TestGetOrCreate:
    def test_creates_new(self):
        user, created = User.get_or_create(
            username="alice", defaults={"email": "a@e.com"}
        )
        assert created is True
        assert user.username == "alice"

    def test_gets_existing(self):
        User.create(username="alice", email="a@e.com")

        user, created = User.get_or_create(
            username="alice", defaults={"email": "other@e.com"}
        )
        assert created is False
        assert user.email == "a@e.com"
