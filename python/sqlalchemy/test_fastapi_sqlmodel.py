"""SQLModel + FastAPI - CRUD API, Depends(get_session), TestClient"""

import os
import tempfile

import pytest
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import Field, Session, SQLModel, create_engine, select


# --- 모델 정의 ---
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class HeroAPI(HeroBase, table=True):
    __tablename__ = "heroes_api"
    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroPublic(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


# --- FastAPI 앱 팩토리 ---
def create_app(engine):
    _app = FastAPI()

    def get_session():
        with Session(engine) as session:
            yield session

    @_app.post("/heroes", response_model=HeroPublic, status_code=201)
    def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
        db_hero = HeroAPI.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

    @_app.get("/heroes", response_model=list[HeroPublic])
    def read_heroes(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
    ):
        heroes = session.exec(select(HeroAPI).offset(offset).limit(limit)).all()
        return heroes

    @_app.get("/heroes/{hero_id}", response_model=HeroPublic)
    def read_hero(*, session: Session = Depends(get_session), hero_id: int):
        hero = session.get(HeroAPI, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="히어로를 찾을 수 없습니다")
        return hero

    @_app.patch("/heroes/{hero_id}", response_model=HeroPublic)
    def update_hero(
        *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
    ):
        db_hero = session.get(HeroAPI, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="히어로를 찾을 수 없습니다")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

    @_app.delete("/heroes/{hero_id}")
    def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
        hero = session.get(HeroAPI, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="히어로를 찾을 수 없습니다")
        session.delete(hero)
        session.commit()
        return {"ok": True}

    return _app


# --- 테스트 ---
@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)
    app = create_app(engine)
    with TestClient(app) as c:
        yield c


class TestFastAPISQLModel:
    """SQLModel + FastAPI 통합 테스트"""

    def test_create_hero(self, client):
        """POST /heroes - 히어로 생성"""
        response = client.post(
            "/heroes",
            json={"name": "스파이더맨", "secret_name": "피터 파커", "age": 20},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "스파이더맨"
        assert data["id"] is not None

    def test_create_hero_validation_error(self, client):
        """POST /heroes - 필수 필드 누락 → 422"""
        response = client.post("/heroes", json={"name": "배트맨"})

        assert response.status_code == 422

    def test_read_heroes(self, client):
        """GET /heroes - 목록 조회"""
        client.post("/heroes", json={"name": "아이언맨", "secret_name": "토니", "age": 45})
        client.post("/heroes", json={"name": "캡틴", "secret_name": "스티브", "age": 100})

        response = client.get("/heroes")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_read_heroes_with_pagination(self, client):
        """GET /heroes - 페이지네이션"""
        for i in range(5):
            client.post("/heroes", json={"name": f"히어로{i}", "secret_name": f"비밀{i}"})

        response = client.get("/heroes?offset=2&limit=2")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_hero_by_id(self, client):
        """GET /heroes/:id - 단건 조회"""
        create_resp = client.post(
            "/heroes", json={"name": "원더우먼", "secret_name": "다이애나", "age": 30}
        )
        hero_id = create_resp.json()["id"]

        response = client.get(f"/heroes/{hero_id}")

        assert response.status_code == 200
        assert response.json()["name"] == "원더우먼"

    def test_read_hero_not_found(self, client):
        """GET /heroes/:id - 404"""
        response = client.get("/heroes/999")

        assert response.status_code == 404

    def test_update_hero(self, client):
        """PATCH /heroes/:id - 부분 업데이트"""
        create_resp = client.post(
            "/heroes", json={"name": "플래시", "secret_name": "배리", "age": 28}
        )
        hero_id = create_resp.json()["id"]

        response = client.patch(f"/heroes/{hero_id}", json={"age": 29})

        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 29
        assert data["name"] == "플래시"  # 변경되지 않음

    def test_delete_hero(self, client):
        """DELETE /heroes/:id - 삭제"""
        create_resp = client.post(
            "/heroes", json={"name": "삭제대상", "secret_name": "비밀"}
        )
        hero_id = create_resp.json()["id"]

        response = client.delete(f"/heroes/{hero_id}")
        assert response.status_code == 200
        assert response.json() == {"ok": True}

        # 삭제 확인
        response = client.get(f"/heroes/{hero_id}")
        assert response.status_code == 404
