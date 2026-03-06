"""pytest-mock (mocker fixture) 사용법."""

from app.service import UserService


class TestMockerPatch:
    """mocker.patch()로 깔끔하게 패칭."""

    def test_mocker_patch_기본(self, mocker):
        """mocker.patch는 fixture scope에 따라 자동 정리된다."""
        mock_get = mocker.patch("app.service.requests.get")
        mock_get.return_value.json.return_value = {"id": 1, "name": "Frank"}
        mock_get.return_value.raise_for_status.return_value = None

        service = UserService()
        user = service.get_user(1)

        assert user["name"] == "Frank"
        mock_get.assert_called_once()

    def test_mocker_patch_return_value(self, mocker):
        """mocker.patch에서 직접 return_value 지정."""
        mocker.patch.object(
            UserService,
            "get_user",
            return_value={"name": "Alice", "email": "alice@test.com"},
        )

        service = UserService()
        result = service.process_user(1)
        assert result == "Alice (alice@test.com)"


class TestMockerSpy:
    """mocker.spy()로 실제 실행 + 호출 기록."""

    def test_mocker_spy(self, mocker):
        """spy는 실제 메서드를 실행하면서 호출 기록을 남긴다."""
        service = UserService()
        spy = mocker.spy(service, "get_user_name")

        # get_user를 mock으로 교체하되, get_user_name은 spy로 실제 실행
        mocker.patch.object(
            service,
            "get_user",
            return_value={"name": "Frank"},
        )

        result = service.get_user_name(1)
        assert result == "Frank"

        # spy로 호출 여부 확인
        spy.assert_called_once_with(1)


class TestMockerStub:
    """mocker.stub()으로 빈 stub 생성."""

    def test_mocker_stub(self, mocker):
        """stub은 호출 기록만 남기는 빈 callable."""
        callback = mocker.stub(name="on_complete")
        callback.return_value = "done"

        result = callback("task1")
        assert result == "done"
        callback.assert_called_once_with("task1")
