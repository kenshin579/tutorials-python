"""uv 데모: httpx와 rich를 사용한 간단한 API 호출 예제."""

import httpx
from rich import print
from rich.table import Table


def fetch_github_info(username: str) -> dict:
    """GitHub 사용자 정보를 가져온다."""
    response = httpx.get(f"https://api.github.com/users/{username}")
    response.raise_for_status()
    return response.json()


def display_user_info(user: dict) -> None:
    """사용자 정보를 테이블로 출력한다."""
    table = Table(title=f"GitHub User: {user['login']}")
    table.add_column("항목", style="cyan")
    table.add_column("값", style="green")

    table.add_row("이름", user.get("name", "N/A"))
    table.add_row("회사", user.get("company", "N/A"))
    table.add_row("위치", user.get("location", "N/A"))
    table.add_row("공개 레포", str(user.get("public_repos", 0)))
    table.add_row("팔로워", str(user.get("followers", 0)))

    print(table)


if __name__ == "__main__":
    user = fetch_github_info("astral-sh")
    display_user_info(user)
