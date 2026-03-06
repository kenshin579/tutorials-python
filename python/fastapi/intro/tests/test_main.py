import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.users import fake_db, next_id


@pytest.fixture(autouse=True)
def reset_db():
    """각 테스트 전에 fake_db를 초기화."""
    import app.routers.users as users_module

    users_module.fake_db = {
        1: {"id": 1, "username": "frank", "email": "frank@example.com", "full_name": "Frank Oh"},
        2: {"id": 2, "username": "alice", "email": "alice@example.com", "full_name": "Alice Kim"},
    }
    users_module.next_id = 3
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FastAPI 입문 예제 API"


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_users_with_pagination(client):
    response = await client.get("/users?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "alice"


@pytest.mark.asyncio
async def test_get_user(client):
    response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "frank"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user(client):
    new_user = {"username": "bob", "email": "bob@example.com", "full_name": "Bob Lee"}
    response = await client.post("/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "bob"
    assert data["id"] == 3


@pytest.mark.asyncio
async def test_create_user_validation_error(client):
    response = await client.post("/users", json={"username": "a", "email": "test@test.com"})
    assert response.status_code == 422  # username too short


@pytest.mark.asyncio
async def test_update_user(client):
    response = await client.put("/users/1", json={"email": "new@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    assert response.json()["username"] == "frank"  # 변경 안 된 필드 유지


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    response = await client.put("/users/999", json={"email": "new@example.com"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(client):
    response = await client.delete("/users/1")
    assert response.status_code == 204

    response = await client.get("/users/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dependency_chaining(client):
    response = await client.get("/users/me/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["db_status"] == "active"
