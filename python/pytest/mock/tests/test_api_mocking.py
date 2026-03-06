"""외부 API 호출 mocking - responses, respx 라이브러리 활용."""

import httpx
import pytest
import requests
import responses
import respx

from app.service import UserService


class TestMockerPatchAPI:
    """mocker.patch로 requests/httpx mock."""

    def test_requests_get_mock(self, mocker, sample_user_dict):
        """mocker.patch로 requests.get 응답 mock."""
        mock_get = mocker.patch("app.service.requests.get")
        mock_get.return_value.json.return_value = sample_user_dict
        mock_get.return_value.raise_for_status.return_value = None

        service = UserService()
        user = service.get_user(1)

        assert user["name"] == "Frank Oh"


class TestResponsesLibrary:
    """responses 라이브러리: requests용 HTTP mock."""

    @responses.activate
    def test_responses_기본(self):
        """@responses.activate로 HTTP 응답 등록."""
        responses.add(
            responses.GET,
            "https://jsonplaceholder.typicode.com/users/1",
            json={"id": 1, "name": "Frank Oh", "email": "frank@example.com"},
            status=200,
        )

        service = UserService()
        user = service.get_user(1)

        assert user["name"] == "Frank Oh"
        assert len(responses.calls) == 1

    @responses.activate
    def test_responses_상태코드_404(self):
        """404 응답 시뮬레이션."""
        responses.add(
            responses.GET,
            "https://jsonplaceholder.typicode.com/users/999",
            json={"error": "Not Found"},
            status=404,
        )

        service = UserService()
        with pytest.raises(requests.exceptions.HTTPError):
            service.get_user(999)

    @responses.activate
    def test_responses_다중_응답(self):
        """같은 URL에 여러 응답 등록 (순차 반환)."""
        responses.add(
            responses.GET,
            "https://jsonplaceholder.typicode.com/users/1",
            json={"error": "Server Error"},
            status=500,
        )
        responses.add(
            responses.GET,
            "https://jsonplaceholder.typicode.com/users/1",
            json={"id": 1, "name": "Frank Oh"},
            status=200,
        )

        service = UserService()

        # 첫 번째 호출: 500 에러
        with pytest.raises(requests.exceptions.HTTPError):
            service.get_user(1)

        # 두 번째 호출: 200 성공 (재시도 성공 시나리오)
        user = service.get_user(1)
        assert user["name"] == "Frank Oh"


class TestRespxLibrary:
    """respx 라이브러리: httpx용 HTTP mock."""

    @respx.mock
    def test_respx_기본(self):
        """@respx.mock으로 httpx 응답 mock."""
        respx.get("https://jsonplaceholder.typicode.com/users/1").mock(
            return_value=httpx.Response(
                200,
                json={"id": 1, "name": "Frank Oh", "email": "frank@example.com"},
            )
        )

        service = UserService()
        user = service.get_user_httpx(1)

        assert user["name"] == "Frank Oh"

    @respx.mock
    def test_respx_상태코드_에러(self):
        """httpx 에러 응답 시뮬레이션."""
        respx.get("https://jsonplaceholder.typicode.com/users/999").mock(
            return_value=httpx.Response(404, json={"error": "Not Found"})
        )

        service = UserService()
        with pytest.raises(httpx.HTTPStatusError):
            service.get_user_httpx(999)
