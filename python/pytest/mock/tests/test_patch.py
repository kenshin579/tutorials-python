"""@patch, patch.object, patch.dict 사용법."""

import os
from unittest.mock import patch

from app.service import UserService, fetch_posts


class TestPatchDecorator:
    """@patch 데코레이터 방식."""

    @patch("app.service.requests.get")
    def test_patch_데코레이터로_requests_mock(self, mock_get):
        """@patch로 requests.get을 mock으로 교체."""
        mock_get.return_value.json.return_value = {"id": 1, "name": "Frank"}
        mock_get.return_value.raise_for_status.return_value = None

        service = UserService()
        user = service.get_user(1)

        assert user["name"] == "Frank"
        mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/users/1")

    @patch("app.service.requests.get")
    def test_patch_모듈_레벨_함수(self, mock_get):
        """모듈 레벨 함수도 동일하게 패치 가능."""
        mock_get.return_value.json.return_value = [{"id": 1, "title": "post1"}]
        mock_get.return_value.raise_for_status.return_value = None

        posts = fetch_posts(limit=1)

        assert len(posts) == 1
        assert posts[0]["title"] == "post1"


class TestPatchContextManager:
    """with patch() 컨텍스트 매니저 방식."""

    def test_patch_context_manager(self):
        """컨텍스트 매니저로 패치하면 블록 끝에서 자동 복원."""
        with patch("app.service.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}
            mock_get.return_value.raise_for_status.return_value = None

            service = UserService()
            user = service.get_user(1)

            assert user["name"] == "Alice"

    def test_patch_object(self):
        """patch.object로 특정 객체의 메서드를 패치."""
        service = UserService()

        with patch.object(service, "get_user", return_value={"name": "Bob", "email": "bob@test.com"}):
            result = service.process_user(1)
            assert result == "Bob (bob@test.com)"


class TestPatchDict:
    """patch.dict로 딕셔너리 패치."""

    @patch.dict(os.environ, {"API_URL": "https://test.api.com"})
    def test_patch_dict_환경변수(self):
        """os.environ 딕셔너리를 패치."""
        assert os.environ["API_URL"] == "https://test.api.com"

    @patch.dict(os.environ, {"NEW_KEY": "new_value"}, clear=False)
    def test_patch_dict_기존값_유지(self):
        """clear=False면 기존 환경변수를 유지하면서 추가."""
        assert os.environ["NEW_KEY"] == "new_value"
        # 기존 PATH 등은 그대로 유지
        assert "PATH" in os.environ


class TestPatchPathRule:
    """patch 대상 경로 규칙: '사용하는 곳'을 패치해야 한다."""

    @patch("app.service.requests.get")
    def test_사용하는_곳을_패치(self, mock_get):
        """app.service에서 import한 requests.get을 패치.

        주의: 'requests.get'이 아니라 'app.service.requests.get'을 패치해야 한다.
        패치 대상은 항상 "사용되는 모듈 경로"를 기준으로 한다.
        """
        mock_get.return_value.json.return_value = {"id": 1, "name": "Test"}
        mock_get.return_value.raise_for_status.return_value = None

        service = UserService()
        user = service.get_user(1)

        assert user["name"] == "Test"
