from fastapi import APIRouter, HTTPException, Path, Query, status

from app.dependencies import CommonParams, CurrentUser, DB
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

# 인메모리 저장소
fake_db: dict[int, dict] = {
    1: {"id": 1, "username": "frank", "email": "frank@example.com", "full_name": "Frank Oh"},
    2: {"id": 2, "username": "alice", "email": "alice@example.com", "full_name": "Alice Kim"},
}
next_id = 3


@router.get(
    "",
    response_model=list[UserResponse],
    summary="사용자 목록 조회",
    description="페이지네이션을 지원하는 사용자 목록 조회 API",
)
def list_users(commons: CommonParams, db: DB):
    """Query 파라미터와 클래스 기반 의존성 예시."""
    users = list(fake_db.values())
    return users[commons.skip : commons.skip + commons.limit]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="사용자 상세 조회",
    responses={404: {"description": "사용자를 찾을 수 없음"}},
)
def get_user(
    user_id: int = Path(ge=1, description="사용자 ID"),
):
    """Path 파라미터와 타입 자동 변환 예시."""
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return fake_db[user_id]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="사용자 생성",
)
def create_user(user: UserCreate):
    """Body 파라미터 (Pydantic 모델) 예시."""
    global next_id
    new_user = {"id": next_id, **user.model_dump()}
    fake_db[next_id] = new_user
    next_id += 1
    return new_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="사용자 수정",
    responses={404: {"description": "사용자를 찾을 수 없음"}},
)
def update_user(
    user: UserUpdate,
    user_id: int = Path(ge=1, description="사용자 ID"),
):
    """Path + Body 조합 예시."""
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    stored = fake_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    stored.update(update_data)
    return stored


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="사용자 삭제",
    responses={404: {"description": "사용자를 찾을 수 없음"}},
)
def delete_user(user_id: int = Path(ge=1)):
    """삭제 엔드포인트 예시."""
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    del fake_db[user_id]


@router.get(
    "/me/profile",
    response_model=dict,
    summary="현재 사용자 프로필 (의존성 체이닝 예시)",
)
def get_my_profile(current_user: CurrentUser):
    """의존성 체이닝 예시: get_current_user -> get_db."""
    return current_user
