"""main 모듈 테스트."""

from unittest.mock import patch

from main import fetch_github_info


def test_fetch_github_info():
    """GitHub API 호출 테스트 (mock)."""
    mock_response = {
        "login": "test-user",
        "name": "Test User",
        "public_repos": 10,
        "followers": 100,
    }

    with patch("main.httpx.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        result = fetch_github_info("test-user")

        assert result["login"] == "test-user"
        assert result["public_repos"] == 10
        mock_get.assert_called_once_with("https://api.github.com/users/test-user")
