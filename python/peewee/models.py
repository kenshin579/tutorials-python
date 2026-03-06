import datetime

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    ManyToManyField,
    Model,
    TextField,
)

from database import db


class BaseModel(Model):
    class Meta:
        database = db


# ── User ─────────────────────────────────────────────
class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "users"


# ── Post (1:N with User) ────────────────────────────
class Post(BaseModel):
    id = AutoField()
    title = CharField(max_length=200)
    content = TextField()
    published = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(User, backref="posts", on_delete="CASCADE")

    class Meta:
        table_name = "posts"


# ── Tag (N:M with Post) ─────────────────────────────
class Tag(BaseModel):
    id = AutoField()
    name = CharField(unique=True, max_length=50)

    class Meta:
        table_name = "tags"


# ManyToManyField 방식
class Article(BaseModel):
    id = AutoField()
    title = CharField(max_length=200)
    tags = ManyToManyField(Tag, backref="articles")

    class Meta:
        table_name = "articles"


ArticleTag = Article.tags.get_through_model()


# 수동 중간 테이블 방식
class PostTag(BaseModel):
    post = ForeignKeyField(Post, backref="post_tags", on_delete="CASCADE")
    tag = ForeignKeyField(Tag, backref="post_tags", on_delete="CASCADE")

    class Meta:
        table_name = "post_tags"
        primary_key = False
        indexes = ((("post", "tag"), True),)  # unique together


ALL_TABLES = [User, Post, Tag, Article, ArticleTag, PostTag]
