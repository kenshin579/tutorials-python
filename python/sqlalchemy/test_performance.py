"""성능 최적화 - N+1 문제, eager loading, echo"""

from __future__ import annotations

import logging

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
)


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    employees: Mapped[list[Employee]] = relationship(back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped[Department] = relationship(back_populates="employees")


def count_queries(engine):
    """실행된 쿼리 수를 추적하는 헬퍼"""
    queries = []

    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        queries.append(statement)

    return queries


class TestNPlusOneProblem:
    """N+1 문제와 해결법"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self._seed_data()

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def _seed_data(self):
        with Session(self.engine) as session:
            for i in range(5):
                dept = Department(name=f"부서{i}")
                dept.employees = [
                    Employee(name=f"직원{i}-{j}") for j in range(3)
                ]
                session.add(dept)
            session.commit()

    def test_n_plus_1_problem(self):
        """N+1 문제 시연 - lazy loading이 쿼리 폭발을 일으킴"""
        queries = count_queries(self.engine)

        with Session(self.engine) as session:
            # 1번 쿼리: 모든 부서 조회
            depts = session.execute(select(Department)).scalars().all()

            # N번 쿼리: 각 부서의 직원 접근 시마다 추가 쿼리
            for dept in depts:
                _ = dept.employees  # lazy loading → 추가 쿼리 발생

        # 1(부서) + 5(각 부서의 직원) = 6개 쿼리 실행
        select_queries = [q for q in queries if q.startswith("SELECT")]
        assert len(select_queries) >= 6  # N+1 문제!

    def test_selectinload_solution(self):
        """selectinload로 N+1 해결 - SELECT IN 쿼리"""
        queries = count_queries(self.engine)

        with Session(self.engine) as session:
            # selectinload: 2번의 쿼리로 모든 데이터 로딩
            stmt = select(Department).options(selectinload(Department.employees))
            depts = session.execute(stmt).scalars().all()

            for dept in depts:
                assert len(dept.employees) == 3  # 추가 쿼리 없음

        select_queries = [q for q in queries if q.startswith("SELECT")]
        assert len(select_queries) == 2  # 부서 1번 + 직원 IN 1번

    def test_joinedload_solution(self):
        """joinedload로 N+1 해결 - LEFT JOIN"""
        queries = count_queries(self.engine)

        with Session(self.engine) as session:
            # joinedload: 1번의 JOIN 쿼리로 모든 데이터 로딩
            stmt = select(Department).options(joinedload(Department.employees))
            depts = session.execute(stmt).unique().scalars().all()

            for dept in depts:
                assert len(dept.employees) == 3

        select_queries = [q for q in queries if q.startswith("SELECT")]
        assert len(select_queries) == 1  # JOIN 1번


class TestEchoMode:
    """echo=True로 SQL 로그 확인"""

    def test_echo_logs_sql(self, caplog):
        """echo=True 설정 시 SQL 로그 출력"""
        engine = create_engine("sqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)

        with caplog.at_level(logging.INFO, logger="sqlalchemy.engine"):
            with Session(engine) as session:
                dept = Department(name="개발팀")
                session.add(dept)
                session.commit()

        # SQL 로그가 출력되었는지 확인
        sql_logs = [r.message for r in caplog.records if "INSERT" in r.message]
        assert len(sql_logs) > 0

        Base.metadata.drop_all(engine)
