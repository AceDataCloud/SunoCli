"""Integration tests for SunoCli — requires a real API token.

Set ACEDATACLOUD_API_TOKEN in your environment or .env file.
These tests are skipped automatically if the token is not configured.

Run with: pytest tests/test_integration.py -m integration -v
"""

import json

import pytest
from click.testing import CliRunner

from suno_cli.main import cli

pytestmark = pytest.mark.integration

requires_api_token = pytest.mark.skipif(
    "not config.getoption('--run-integration', default=False)",
    reason="Integration tests require --run-integration flag",
)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def conftest_addoption(parser):
    """Hook to add --run-integration CLI option to pytest."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (requires ACEDATACLOUD_API_TOKEN)",
    )


class TestGenerateIntegration:
    """Integration tests for audio generation."""

    @pytest.mark.slow
    def test_generate_real_api(self, runner, api_token):
        """Test real audio generation (creates a task)."""
        result = runner.invoke(
            cli,
            ["--token", api_token, "generate", "A short test melody", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "task_id" in data

    @pytest.mark.slow
    def test_lyrics_real_api(self, runner, api_token):
        """Test real lyrics generation."""
        result = runner.invoke(
            cli,
            ["--token", api_token, "lyrics", "A song about coding", "--json"],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "task_id" in data


class TestInfoIntegration:
    """Integration tests for info commands (no API calls needed)."""

    def test_models_no_token(self, runner):
        """Models command should work without a token."""
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "chirp" in result.output

    def test_actions_no_token(self, runner):
        """Actions command should work without a token."""
        result = runner.invoke(cli, ["actions"])
        assert result.exit_code == 0
        assert "generate" in result.output

    def test_lyric_format_no_token(self, runner):
        """Lyric format command should work without a token."""
        result = runner.invoke(cli, ["lyric-format"])
        assert result.exit_code == 0
        assert "Verse" in result.output

    def test_config_display(self, runner):
        """Config command should show settings."""
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Base URL" in result.output
