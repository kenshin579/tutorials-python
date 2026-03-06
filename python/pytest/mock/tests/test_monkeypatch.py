"""monkeypatch fixture 사용법."""

import os
import sys

from app.config import get_api_url, get_database_url, get_debug_mode
from app.service import UserService


class TestMonkeypatchSetattr:
    """monkeypatch.setattr()로 속성/메서드 교체."""

    def test_setattr_메서드_교체(self, monkeypatch):
        """클래스 메서드를 간단한 함수로 교체."""

        def fake_get_user(self, user_id):
            return {"id": user_id, "name": "Mocked User"}

        monkeypatch.setattr(UserService, "get_user", fake_get_user)

        service = UserService()
        user = service.get_user(42)
        assert user["name"] == "Mocked User"
        assert user["id"] == 42

    def test_setattr_모듈_함수_교체(self, monkeypatch):
        """모듈 레벨 함수를 교체."""
        monkeypatch.setattr("app.config.os.environ.get", lambda key, default=None: {
            "API_URL": "https://mock.api.com",
            "DEBUG": "true",
        }.get(key, default))

        assert get_api_url() == "https://mock.api.com"
        assert get_debug_mode() is True


class TestMonkeypatchEnv:
    """monkeypatch.setenv() / delenv()로 환경변수 조작."""

    def test_setenv(self, monkeypatch):
        """환경변수 설정."""
        monkeypatch.setenv("API_URL", "https://test.api.com")
        monkeypatch.setenv("DEBUG", "true")

        assert get_api_url() == "https://test.api.com"
        assert get_debug_mode() is True

    def test_delenv(self, monkeypatch):
        """환경변수 삭제."""
        monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
        assert get_database_url() == "sqlite:///test.db"

        monkeypatch.delenv("DATABASE_URL")
        try:
            get_database_url()
            assert False, "RuntimeError가 발생해야 한다"
        except RuntimeError:
            pass

    def test_delenv_raising_false(self, monkeypatch):
        """존재하지 않는 환경변수 삭제 시 raising=False로 에러 방지."""
        monkeypatch.delenv("NON_EXISTENT_VAR", raising=False)
        # 에러 없이 통과


class TestMonkeypatchChdir:
    """monkeypatch.chdir()로 작업 디렉토리 변경."""

    def test_chdir(self, monkeypatch, tmp_path):
        """작업 디렉토리를 변경하고 테스트 후 자동 복원."""
        original_dir = os.getcwd()

        monkeypatch.chdir(tmp_path)
        assert os.getcwd() == str(tmp_path)

        # 테스트 종료 후 원래 디렉토리로 자동 복원


class TestMonkeypatchSyspath:
    """monkeypatch.syspath_prepend()로 sys.path 수정."""

    def test_syspath_prepend(self, monkeypatch, tmp_path):
        """sys.path 앞에 경로를 추가."""
        monkeypatch.syspath_prepend(str(tmp_path))

        assert str(tmp_path) == sys.path[0]
        # 테스트 종료 후 sys.path 자동 복원
