"""모델 정의 및 관계 설정 테스트."""

from peewee import prefetch

from models import Article, ArticleTag, Post, PostTag, Tag, User


class TestUserModel:
    def test_create_user(self):
        user = User.create(username="alice", email="alice@example.com")
        assert user.id is not None
        assert user.username == "alice"
        assert user.is_active is True

    def test_unique_username(self):
        User.create(username="alice", email="alice@example.com")
        import pytest

        with pytest.raises(Exception):
            User.create(username="alice", email="other@example.com")


class TestOneToMany:
    def test_user_posts_relationship(self):
        user = User.create(username="alice", email="alice@example.com")
        Post.create(title="Post 1", content="Content", author=user)
        Post.create(title="Post 2", content="Content", author=user)

        assert user.posts.count() == 2

    def test_post_author_backref(self):
        user = User.create(username="alice", email="alice@example.com")
        post = Post.create(title="Post 1", content="Content", author=user)

        assert post.author.username == "alice"


class TestManyToMany:
    def test_manual_through_table(self):
        user = User.create(username="alice", email="alice@example.com")
        post = Post.create(title="Post", content="Content", author=user)
        tag1 = Tag.create(name="Python")
        tag2 = Tag.create(name="Peewee")

        PostTag.create(post=post, tag=tag1)
        PostTag.create(post=post, tag=tag2)

        tags = [pt.tag.name for pt in post.post_tags]
        assert set(tags) == {"Python", "Peewee"}

    def test_many_to_many_field(self):
        article = Article.create(title="Test Article")
        tag1 = Tag.create(name="Python")
        tag2 = Tag.create(name="ORM")

        article.tags.add([tag1, tag2])

        assert article.tags.count() == 2
        assert tag1.articles.count() == 1

    def test_many_to_many_remove(self):
        article = Article.create(title="Test Article")
        tag = Tag.create(name="Python")
        article.tags.add(tag)

        article.tags.remove(tag)
        assert article.tags.count() == 0


class TestPrefetch:
    def test_prefetch_avoids_n_plus_1(self):
        alice = User.create(username="alice", email="alice@example.com")
        bob = User.create(username="bob", email="bob@example.com")
        Post.create(title="A1", content="c", author=alice)
        Post.create(title="A2", content="c", author=alice)
        Post.create(title="B1", content="c", author=bob)

        users = prefetch(User.select(), Post.select())
        result = {u.username: len(u.posts) for u in users}

        assert result["alice"] == 2
        assert result["bob"] == 1
