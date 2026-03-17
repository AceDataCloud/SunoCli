"""Unit tests for HTTP client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from suno_cli.core.client import SunoClient, get_client
from suno_cli.core.exceptions import SunoAPIError, SunoAuthError, SunoTimeoutError


@pytest.fixture
def client() -> SunoClient:
    return SunoClient(api_token="test-token", base_url="https://api.test.local")


class TestSunoClient:
    """Tests for SunoClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = SunoClient(api_token="my-token", base_url="https://custom.api.com")
        assert client.api_token == "my-token"
        assert client.base_url == "https://custom.api.com"

    def test_get_headers(self, client):
        """Test that headers are correctly generated."""
        headers = client._get_headers()
        assert headers["accept"] == "application/json"
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        """Test that missing token raises auth error."""
        client = SunoClient(api_token="", base_url="https://api.test.local")
        with pytest.raises(SunoAuthError, match="not configured"):
            client._get_headers()

    @pytest.mark.parametrize(
        "endpoint,method",
        [
            ("/suno/audios", "generate_audio"),
            ("/suno/lyrics", "generate_lyrics"),
            ("/suno/persona", "create_persona"),
            ("/suno/mp4", "get_mp4"),
            ("/suno/wav", "get_wav"),
            ("/suno/midi", "get_midi"),
            ("/suno/timing", "get_timing"),
            ("/suno/vox", "get_vox"),
            ("/suno/style", "get_style"),
            ("/suno/mashup-lyrics", "mashup_lyrics"),
            ("/suno/upload", "upload_audio"),
            ("/suno/tasks", "query_task"),
        ],
    )
    def test_convenience_methods(self, client, endpoint, method):
        """Test all convenience methods call the correct endpoints."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            fn = getattr(client, method)
            result = fn(test_param="value")

            assert result == {"success": True}
            call_args = mock_instance.post.call_args
            assert endpoint in call_args[0][0]


class TestRequestErrors:
    """Tests for error handling in requests."""

    def test_request_auth_error_401(self, client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            with pytest.raises(SunoAuthError, match="Invalid API token"):
                client.request("/suno/audios", {})

    def test_request_forbidden_403(self, client):
        """Test 403 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 403

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            with pytest.raises(SunoAuthError, match="Access denied"):
                client.request("/suno/audios", {})

    def test_request_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_http.return_value.__enter__.return_value = mock_instance

            with pytest.raises(SunoTimeoutError, match="timed out"):
                client.request("/suno/audios", {})

    def test_request_http_error_500(self, client):
        """Test HTTP 500 error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 200  # initial check passes
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error",
            request=MagicMock(),
            response=MagicMock(status_code=500, text="Internal Server Error"),
        )

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            with pytest.raises(SunoAPIError):
                client.request("/suno/audios", {})

    def test_request_removes_none_values(self, client):
        """Test that None values are stripped from payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}

        with patch("httpx.Client") as mock_http:
            mock_instance = MagicMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__enter__.return_value = mock_instance

            client.request("/suno/audios", {"a": "b", "c": None, "d": "e"})
            call_kwargs = mock_instance.post.call_args
            sent_json = call_kwargs[1]["json"]
            assert "c" not in sent_json
            assert sent_json == {"a": "b", "d": "e"}


class TestGetClient:
    """Tests for get_client factory function."""

    def test_get_client_with_token(self):
        """Test creating client with explicit token."""
        client = get_client("custom-token")
        assert client.api_token == "custom-token"

    def test_get_client_without_token(self):
        """Test creating client uses settings token."""
        client = get_client(None)
        assert isinstance(client, SunoClient)
