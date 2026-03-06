"""Peewee 쿼리 빌더 예제."""

from peewee import fn, prefetch

from database import db
from models import ALL_TABLES, Post, PostTag, Tag, User


def setup():
    db.connect()
    db.create_tables(ALL_TABLES)
    _seed_data()


def teardown():
    db.drop_tables(ALL_TABLES)
    db.close()


def _seed_data():
    alice = User.create(username="alice", email="alice@example.com")
    bob = User.create(username="bob", email="bob@example.com")

    python = Tag.create(name="Python")
    peewee = Tag.create(name="Peewee")
    fastapi = Tag.create(name="FastAPI")

    for i in range(1, 6):
        post = Post.create(
            title=f"Alice Post {i}",
            content=f"Content {i}",
            published=(i % 2 == 1),
            author=alice,
        )
        PostTag.create(post=post, tag=python)
        if i <= 3:
            PostTag.create(post=post, tag=peewee)

    for i in range(1, 4):
        post = Post.create(
            title=f"Bob Post {i}",
            content=f"Content {i}",
            published=True,
            author=bob,
        )
        PostTag.create(post=post, tag=fastapi)


# ── 체이닝: select / where / order_by / limit ────────
def query_chaining():
    """select().where().order_by().limit() 체이닝."""
    posts = (
        Post.select()
        .where(Post.published == True)
        .order_by(Post.created_at.desc())
        .limit(3)
    )
    return list(posts)


# ── JOIN ─────────────────────────────────────────────
def query_join():
    """join()으로 명시적 JOIN 쿼리."""
    query = (
        Post.select(Post, User)
        .join(User)
        .where(User.username == "alice")
    )
    return [(p.title, p.author.username) for p in query]


# ── 집계 함수 ────────────────────────────────────────
def query_aggregate():
    """fn.COUNT(), fn.SUM() 집계 함수."""
    query = (
        User.select(User.username, fn.COUNT(Post.id).alias("post_count"))
        .join(Post)
        .group_by(User.username)
    )
    return [(row.username, row.post_count) for row in query]


def query_having():
    """group_by() + having() 그룹 필터."""
    query = (
        User.select(User.username, fn.COUNT(Post.id).alias("post_count"))
        .join(Post)
        .group_by(User.username)
        .having(fn.COUNT(Post.id) > 3)
    )
    return [(row.username, row.post_count) for row in query]


# ── 결과 형식 ────────────────────────────────────────
def query_result_formats():
    """dicts(), tuples(), namedtuples() 결과 형식."""
    base = User.select().limit(2)

    as_dicts = list(base.dicts())
    as_tuples = list(base.tuples())
    as_namedtuples = list(base.namedtuples())

    return as_dicts, as_tuples, as_namedtuples


# ── prefetch: N+1 문제 방지 ──────────────────────────
def query_prefetch():
    """prefetch()로 N+1 문제 방지."""
    users = User.select()
    posts = Post.select()
    users_with_posts = prefetch(users, posts)

    result = []
    for user in users_with_posts:
        result.append((user.username, [p.title for p in user.posts]))
    return result


if __name__ == "__main__":
    setup()
    try:
        print("=== 체이닝 ===")
        for post in query_chaining():
            print(f"  {post.title} (published={post.published})")

        print("\n=== JOIN ===")
        for title, author in query_join():
            print(f"  {title} by {author}")

        print("\n=== 집계 ===")
        for username, count in query_aggregate():
            print(f"  {username}: {count} posts")

        print("\n=== HAVING (post_count > 3) ===")
        for username, count in query_having():
            print(f"  {username}: {count} posts")

        print("\n=== 결과 형식 ===")
        dicts, tuples, namedtuples = query_result_formats()
        print(f"  dicts: {dicts}")
        print(f"  tuples: {tuples}")
        print(f"  namedtuples: {namedtuples}")

        print("\n=== prefetch ===")
        for username, posts in query_prefetch():
            print(f"  {username}: {posts}")
    finally:
        teardown()
