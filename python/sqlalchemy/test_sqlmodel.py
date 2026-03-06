"""SQLModel 기본 - table=True, 데이터 모델, Pydantic 통합"""

import pytest
from pydantic import ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select


# --- DB 테이블 모델 (table=True) ---
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


# --- 데이터 전용 모델 (table=False, 기본값) ---
class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroResponse(SQLModel):
    id: int
    name: str
    age: int | None = None


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


class TestSQLModelBasic:
    """SQLModel 기본 사용법"""

    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine)

    def teardown_method(self):
        SQLModel.metadata.drop_all(self.engine)

    def test_table_model_crud(self):
        """table=True 모델로 CRUD"""
        with Session(self.engine) as session:
            hero = Hero(name="스파이더맨", secret_name="피터 파커", age=20)
            session.add(hero)
            session.commit()
            session.refresh(hero)

            assert hero.id is not None
            assert hero.name == "스파이더맨"

    def test_select_with_sqlmodel(self):
        """SQLModel의 select() 사용"""
        with Session(self.engine) as session:
            session.add(Hero(name="아이언맨", secret_name="토니 스타크", age=45))
            session.add(Hero(name="스파이더맨", secret_name="피터 파커", age=20))
            session.commit()

        with Session(self.engine) as session:
            heroes = session.exec(select(Hero).where(Hero.age >= 30)).all()

            assert len(heroes) == 1
            assert heroes[0].name == "아이언맨"

    def test_data_model_validation(self):
        """데이터 모델 (table=False)은 Pydantic 검증 수행"""
        hero_create = HeroCreate(name="배트맨", secret_name="브루스 웨인", age=35)

        assert hero_create.name == "배트맨"
        assert hero_create.model_dump() == {
            "name": "배트맨",
            "secret_name": "브루스 웨인",
            "age": 35,
        }

    def test_data_model_validation_error(self):
        """데이터 모델 검증 실패"""
        with pytest.raises(ValidationError):
            HeroCreate(secret_name="이름 없음")  # name 필수

    def test_model_validate_create(self):
        """데이터 모델 → DB 모델 변환"""
        hero_create = HeroCreate(name="원더우먼", secret_name="다이애나", age=30)

        with Session(self.engine) as session:
            hero = Hero.model_validate(hero_create)
            session.add(hero)
            session.commit()
            session.refresh(hero)

            assert hero.id is not None
            assert hero.name == "원더우먼"

    def test_response_model(self):
        """DB 모델 → 응답 모델 변환 (secret_name 제외)"""
        with Session(self.engine) as session:
            hero = Hero(name="플래시", secret_name="배리 앨런", age=28)
            session.add(hero)
            session.commit()
            session.refresh(hero)

            response = HeroResponse.model_validate(hero)

            assert response.id == hero.id
            assert response.name == "플래시"
            assert not hasattr(response, "secret_name") or "secret_name" not in response.model_dump()

    def test_update_pattern(self):
        """업데이트 패턴 - exclude_unset으로 부분 업데이트"""
        with Session(self.engine) as session:
            hero = Hero(name="슈퍼맨", secret_name="클라크 켄트", age=35)
            session.add(hero)
            session.commit()
            session.refresh(hero)
            hero_id = hero.id

        with Session(self.engine) as session:
            hero = session.get(Hero, hero_id)
            update_data = HeroUpdate(name="슈퍼맨(수정)")

            # exclude_unset=True: 명시적으로 설정된 값만 업데이트
            hero_data = update_data.model_dump(exclude_unset=True)
            hero.sqlmodel_update(hero_data)
            session.add(hero)
            session.commit()
            session.refresh(hero)

            assert hero.name == "슈퍼맨(수정)"
            assert hero.secret_name == "클라크 켄트"  # 변경되지 않음
