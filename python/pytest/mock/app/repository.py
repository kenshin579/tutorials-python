from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository:
    """DB 접근 계층 (Repository 패턴)."""

    def find_by_id(self, user_id: int) -> User | None:
        """사용자 조회 (실제 구현에서는 DB 접근)."""
        raise NotImplementedError("DB 연결 필요")

    def find_all(self) -> list[User]:
        """전체 사용자 조회."""
        raise NotImplementedError("DB 연결 필요")

    def save(self, user: User) -> User:
        """사용자 저장."""
        raise NotImplementedError("DB 연결 필요")

    def delete(self, user_id: int) -> bool:
        """사용자 삭제."""
        raise NotImplementedError("DB 연결 필요")


class UserServiceWithRepo:
    """Repository를 사용하는 서비스 클래스."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_display_name(self, user_id: int) -> str:
        """사용자 표시 이름 반환."""
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return f"{user.name} <{user.email}>"

    def get_all_user_names(self) -> list[str]:
        """전체 사용자 이름 목록 반환."""
        users = self.repository.find_all()
        return [user.name for user in users]

    def create_user(self, name: str, email: str) -> User:
        """새 사용자 생성."""
        user = User(id=0, name=name, email=email)
        return self.repository.save(user)
