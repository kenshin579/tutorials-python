"""Peewee CRUD 연산 예제."""

from database import db
from models import ALL_TABLES, Post, Tag, PostTag, User


def setup():
    db.connect()
    db.create_tables(ALL_TABLES)


def teardown():
    db.drop_tables(ALL_TABLES)
    db.close()


# ── Create ───────────────────────────────────────────
def create_single():
    """Model.create()로 단건 생성."""
    user = User.create(username="alice", email="alice@example.com")
    return user


def create_many():
    """insert_many()로 다건 생성."""
    users = [
        {"username": "bob", "email": "bob@example.com"},
        {"username": "charlie", "email": "charlie@example.com"},
    ]
    User.insert_many(users).execute()


# ── Read ─────────────────────────────────────────────
def read_by_id(user_id: int):
    """get_by_id()로 PK 조회."""
    return User.get_by_id(user_id)


def read_with_filter():
    """select().where()로 조건 조회."""
    return list(User.select().where(User.is_active == True))


# ── Update ───────────────────────────────────────────
def update_single(user: User, new_email: str):
    """인스턴스 수정 후 save()."""
    user.email = new_email
    user.save()
    return user


def update_bulk():
    """update().where()로 벌크 업데이트."""
    rows = User.update(is_active=False).where(User.username == "bob").execute()
    return rows


# ── Delete ───────────────────────────────────────────
def delete_single(user: User):
    """delete_instance()로 단건 삭제."""
    return user.delete_instance()


def delete_bulk():
    """delete().where()로 벌크 삭제."""
    rows = User.delete().where(User.is_active == False).execute()
    return rows


# ── get_or_create ────────────────────────────────────
def get_or_create_user(username: str, email: str):
    """get_or_create(): 있으면 조회, 없으면 생성."""
    user, created = User.get_or_create(
        username=username,
        defaults={"email": email},
    )
    return user, created


if __name__ == "__main__":
    setup()
    try:
        # Create
        alice = create_single()
        print(f"Created: {alice.username} (id={alice.id})")

        create_many()
        print(f"Total users: {User.select().count()}")

        # Read
        user = read_by_id(alice.id)
        print(f"Read by id: {user.username}")

        active_users = read_with_filter()
        print(f"Active users: {[u.username for u in active_users]}")

        # Update
        update_single(alice, "alice_new@example.com")
        print(f"Updated email: {alice.email}")

        rows = update_bulk()
        print(f"Bulk updated: {rows} rows")

        # get_or_create
        user, created = get_or_create_user("dave", "dave@example.com")
        print(f"get_or_create: {user.username}, created={created}")

        user, created = get_or_create_user("dave", "dave@example.com")
        print(f"get_or_create: {user.username}, created={created}")

        # Delete
        delete_bulk()
        print(f"After bulk delete: {User.select().count()} users")
    finally:
        teardown()
