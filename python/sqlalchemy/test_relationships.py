"""관계 설정 - 1:N, N:M, back_populates, lazy loading"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
    joinedload,
)


class Base(DeclarativeBase):
    pass


# --- 1:N 관계: Author ↔ Book ---
class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    books: Mapped[list[Book]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name!r})"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped[Author] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title!r})"


# --- N:M 관계: Student ↔ Course (association table) ---
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    courses: Mapped[list[Course]] = relationship(
        secondary=student_course, back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    students: Mapped[list[Student]] = relationship(
        secondary=student_course, back_populates="courses"
    )


class TestOneToMany:
    """1:N 관계 (Author ↔ Book)"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_create_with_relationship(self):
        """관계를 통한 생성"""
        with Session(self.engine) as session:
            author = Author(name="김작가")
            author.books.append(Book(title="파이썬 입문"))
            author.books.append(Book(title="파이썬 심화"))
            session.add(author)
            session.commit()

        with Session(self.engine) as session:
            author = session.execute(
                select(Author).where(Author.name == "김작가")
            ).scalars().first()

            assert len(author.books) == 2
            titles = [b.title for b in author.books]
            assert "파이썬 입문" in titles

    def test_back_populates(self):
        """back_populates - 양방향 관계"""
        with Session(self.engine) as session:
            author = Author(name="이작가")
            book = Book(title="SQL 가이드", author=author)
            session.add(book)
            session.commit()

        with Session(self.engine) as session:
            book = session.execute(
                select(Book).where(Book.title == "SQL 가이드")
            ).scalars().first()

            assert book.author.name == "이작가"
            assert book in book.author.books

    def test_selectinload(self):
        """selectinload - eager loading으로 N+1 방지"""
        with Session(self.engine) as session:
            author = Author(name="박작가")
            author.books = [
                Book(title=f"책{i}") for i in range(5)
            ]
            session.add(author)
            session.commit()

        with Session(self.engine) as session:
            # selectinload: SELECT IN 쿼리로 관계 데이터 한번에 로딩
            stmt = select(Author).options(selectinload(Author.books))
            author = session.execute(stmt).scalars().first()

            assert len(author.books) == 5

    def test_joinedload(self):
        """joinedload - JOIN으로 한번의 쿼리로 로딩"""
        with Session(self.engine) as session:
            author = Author(name="최작가")
            author.books = [Book(title="조인 테스트")]
            session.add(author)
            session.commit()

        with Session(self.engine) as session:
            # joinedload: LEFT JOIN으로 한번의 쿼리
            stmt = select(Author).options(joinedload(Author.books)).where(
                Author.name == "최작가"
            )
            author = session.execute(stmt).unique().scalars().first()

            assert len(author.books) == 1
            assert author.books[0].title == "조인 테스트"


class TestManyToMany:
    """N:M 관계 (Student ↔ Course)"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_many_to_many(self):
        """N:M 관계 생성 및 조회"""
        with Session(self.engine) as session:
            python = Course(title="Python 기초")
            fastapi = Course(title="FastAPI 개발")
            db_course = Course(title="데이터베이스")

            student1 = Student(name="홍길동", courses=[python, fastapi])
            student2 = Student(name="김철수", courses=[python, db_course])

            session.add_all([student1, student2])
            session.commit()

        with Session(self.engine) as session:
            # 홍길동이 수강하는 과목
            hong = session.execute(
                select(Student).where(Student.name == "홍길동")
            ).scalars().first()
            assert len(hong.courses) == 2

            # Python 기초를 수강하는 학생
            python = session.execute(
                select(Course).where(Course.title == "Python 기초")
            ).scalars().first()
            assert len(python.students) == 2

    def test_add_remove_relationship(self):
        """N:M 관계 추가/제거"""
        with Session(self.engine) as session:
            student = Student(name="이영희")
            course = Course(title="알고리즘")
            student.courses.append(course)
            session.add(student)
            session.commit()

            assert len(student.courses) == 1

            # 관계 제거
            student.courses.remove(course)
            session.commit()

            assert len(student.courses) == 0
