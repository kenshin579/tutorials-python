"""쿼리 빌더, 집계, 결과 형식 테스트."""

from peewee import fn

from models import Post, PostTag, Tag, User


def _seed():
    alice = User.create(username="alice", email="a@e.com")
    bob = User.create(username="bob", email="b@e.com")

    python = Tag.create(name="Python")
    fastapi = Tag.create(name="FastAPI")

    for i in range(1, 6):
        post = Post.create(
            title=f"Alice Post {i}",
            content=f"Content {i}",
            published=(i % 2 == 1),
            author=alice,
        )
        PostTag.create(post=post, tag=python)

    for i in range(1, 3):
        post = Post.create(
            title=f"Bob Post {i}",
            content=f"Content {i}",
            published=True,
            author=bob,
        )
        PostTag.create(post=post, tag=fastapi)

    return alice, bob


class TestChaining:
    def test_select_where_order_limit(self):
        _seed()
        posts = list(
            Post.select()
            .where(Post.published == True)
            .order_by(Post.title)
            .limit(3)
        )
        assert len(posts) == 3
        assert all(p.published for p in posts)


class TestJoin:
    def test_join_filter_by_user(self):
        _seed()
        posts = list(
            Post.select(Post, User).join(User).where(User.username == "alice")
        )
        assert len(posts) == 5
        assert all(p.author.username == "alice" for p in posts)


class TestAggregate:
    def test_count_posts_per_user(self):
        _seed()
        query = (
            User.select(User.username, fn.COUNT(Post.id).alias("post_count"))
            .join(Post)
            .group_by(User.username)
            .order_by(User.username)
        )
        result = [(r.username, r.post_count) for r in query]
        assert result == [("alice", 5), ("bob", 2)]

    def test_having_filter(self):
        _seed()
        query = (
            User.select(User.username, fn.COUNT(Post.id).alias("post_count"))
            .join(Post)
            .group_by(User.username)
            .having(fn.COUNT(Post.id) > 3)
        )
        result = [(r.username, r.post_count) for r in query]
        assert result == [("alice", 5)]


class TestResultFormats:
    def test_dicts(self):
        User.create(username="alice", email="a@e.com")
        rows = list(User.select().dicts())
        assert isinstance(rows[0], dict)
        assert rows[0]["username"] == "alice"

    def test_tuples(self):
        User.create(username="alice", email="a@e.com")
        rows = list(User.select().tuples())
        assert isinstance(rows[0], tuple)

    def test_namedtuples(self):
        User.create(username="alice", email="a@e.com")
        rows = list(User.select().namedtuples())
        assert hasattr(rows[0], "username")
        assert rows[0].username == "alice"
