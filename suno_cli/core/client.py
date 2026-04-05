"""HTTP client for Suno API."""

from typing import Any

import httpx

from suno_cli.core.config import settings
from suno_cli.core.exceptions import SunoAPIError, SunoAuthError, SunoTimeoutError


class SunoClient:
    """HTTP client for AceDataCloud Suno API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        if not self.api_token:
            raise SunoAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "content-type": "application/json",
        }

    def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Suno API.

        Args:
            endpoint: API endpoint path (e.g., "/suno/audios")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        # Remove None values from payload
        payload = {k: v for k, v in payload.items() if v is not None}

        with httpx.Client() as http_client:
            try:
                response = http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                if response.status_code == 401:
                    raise SunoAuthError("Invalid API token")

                if response.status_code == 403:
                    raise SunoAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()
                return response.json()  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                raise SunoTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except SunoAuthError:
                raise

            except httpx.HTTPStatusError as e:
                raise SunoAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                if isinstance(e, SunoAPIError | SunoTimeoutError):
                    raise
                raise SunoAPIError(message=str(e)) from e

    # Convenience methods
    def generate_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Generate audio using the audios endpoint."""
        return self.request("/suno/audios", kwargs)

    def generate_lyrics(self, **kwargs: Any) -> dict[str, Any]:
        """Generate lyrics using the lyrics endpoint."""
        return self.request("/suno/lyrics", kwargs)

    def create_persona(self, **kwargs: Any) -> dict[str, Any]:
        """Create a persona using the persona endpoint."""
        return self.request("/suno/persona", kwargs)

    def get_mp4(self, **kwargs: Any) -> dict[str, Any]:
        """Get MP4 video for a song."""
        return self.request("/suno/mp4", kwargs)

    def get_timing(self, **kwargs: Any) -> dict[str, Any]:
        """Get timing/subtitle data for a song."""
        return self.request("/suno/timing", kwargs)

    def get_vox(self, **kwargs: Any) -> dict[str, Any]:
        """Extract vocals from a song."""
        return self.request("/suno/vox", kwargs)

    def get_wav(self, **kwargs: Any) -> dict[str, Any]:
        """Get WAV format of a song."""
        return self.request("/suno/wav", kwargs)

    def get_midi(self, **kwargs: Any) -> dict[str, Any]:
        """Get MIDI data of a song."""
        return self.request("/suno/midi", kwargs)

    def get_style(self, **kwargs: Any) -> dict[str, Any]:
        """Optimize a style prompt."""
        return self.request("/suno/style", kwargs)

    def mashup_lyrics(self, **kwargs: Any) -> dict[str, Any]:
        """Generate mashup lyrics from two sets of lyrics."""
        return self.request("/suno/mashup-lyrics", kwargs)

    def upload_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Upload audio from a URL."""
        return self.request("/suno/upload", kwargs)

    def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        return self.request("/suno/tasks", kwargs)


def get_client(token: str | None = None) -> SunoClient:
    """Get a SunoClient instance, optionally overriding the token."""
    if token:
        return SunoClient(api_token=token)
    return SunoClient()
