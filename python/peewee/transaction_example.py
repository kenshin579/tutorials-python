"""Peewee 트랜잭션 관리 예제."""

from peewee import IntegrityError

from database import db
from models import ALL_TABLES, User


def setup():
    db.connect()
    db.create_tables(ALL_TABLES)


def teardown():
    db.drop_tables(ALL_TABLES)
    db.close()


# ── db.atomic() context manager ──────────────────────
def transaction_context_manager():
    """db.atomic()을 context manager로 사용."""
    with db.atomic():
        User.create(username="alice", email="alice@example.com")
        User.create(username="bob", email="bob@example.com")
    # 블록 정상 종료 시 자동 COMMIT
    print(f"After commit: {User.select().count()} users")


def transaction_rollback():
    """예외 발생 시 자동 ROLLBACK."""
    try:
        with db.atomic():
            User.create(username="charlie", email="charlie@example.com")
            raise IntegrityError("의도적 에러 - 롤백 테스트")
    except IntegrityError:
        pass
    print(f"After rollback: {User.select().count()} users")


# ── 중첩 트랜잭션 (savepoint) ────────────────────────
def transaction_nested():
    """중첩 atomic() → savepoint 지원."""
    with db.atomic() as outer:
        User.create(username="dave", email="dave@example.com")

        try:
            with db.atomic() as inner:
                User.create(username="eve", email="eve@example.com")
                raise IntegrityError("내부 트랜잭션 롤백")
        except IntegrityError:
            pass  # inner savepoint만 롤백

    # dave는 저장, eve는 롤백
    users = [u.username for u in User.select()]
    print(f"After nested: {users}")


# ── @db.atomic() 데코레이터 ──────────────────────────
@db.atomic()
def create_user_atomic(username: str, email: str):
    """데코레이터 패턴으로 트랜잭션 관리."""
    return User.create(username=username, email=email)


if __name__ == "__main__":
    setup()
    try:
        print("=== context manager ===")
        transaction_context_manager()

        print("\n=== rollback ===")
        transaction_rollback()

        print("\n=== nested (savepoint) ===")
        transaction_nested()

        print("\n=== decorator ===")
        user = create_user_atomic("frank", "frank@example.com")
        print(f"Created with decorator: {user.username}")
    finally:
        teardown()
