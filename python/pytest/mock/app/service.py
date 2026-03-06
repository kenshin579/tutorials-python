import httpx
import requests


class UserService:
    """외부 API를 호출하는 서비스 클래스."""

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """requests로 사용자 정보 조회."""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def get_user_httpx(self, user_id: int) -> dict:
        """httpx로 사용자 정보 조회."""
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()

    def get_user_name(self, user_id: int) -> str:
        """사용자 이름만 반환."""
        user = self.get_user(user_id)
        return user["name"]

    def process_user(self, user_id: int) -> str:
        """사용자 정보를 가공하여 반환."""
        user = self.get_user(user_id)
        return f"{user['name']} ({user['email']})"


def fetch_posts(limit: int = 10) -> list[dict]:
    """게시글 목록 조회 (모듈 레벨 함수)."""
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"_limit": limit},
    )
    response.raise_for_status()
    return response.json()
