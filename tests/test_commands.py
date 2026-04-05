"""Tests for CLI commands."""

import json
import os
import tempfile

import pytest
import respx
from click.testing import CliRunner
from httpx import Response

from suno_cli.main import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ─── Version / Help ────────────────────────────────────────────────────────


class TestGlobalCommands:
    """Tests for global CLI options."""

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "suno-cli" in result.output

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "custom" in result.output
        assert "lyrics" in result.output
        assert "task" in result.output
        assert "wait" in result.output

    def test_help_generate(self, runner):
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "PROMPT" in result.output
        assert "--model" in result.output
        assert "--instrumental" in result.output

    def test_help_custom(self, runner):
        result = runner.invoke(cli, ["custom", "--help"])
        assert result.exit_code == 0
        assert "--lyric" in result.output
        assert "--title" in result.output
        assert "--style" in result.output


# ─── Generation Commands ───────────────────────────────────────────────────


class TestGenerateCommands:
    """Tests for music generation commands."""

    @respx.mock
    def test_generate_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A happy song", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"

    @respx.mock
    def test_generate_rich_output(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "generate", "A happy song"])
        assert result.exit_code == 0
        assert "test-task-123" in result.output

    @respx.mock
    def test_generate_with_model(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "test", "--model", "chirp-v5", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_instrumental(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "generate", "test", "--instrumental", "--json"]
        )
        assert result.exit_code == 0

    def test_generate_no_token(self, runner):
        result = runner.invoke(cli, ["--token", "", "generate", "test"])
        assert result.exit_code != 0

    @respx.mock
    def test_custom_json(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "custom",
                "-l",
                "[Verse]\nHello world",
                "-t",
                "Hello",
                "-s",
                "pop",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @respx.mock
    def test_custom_lyrics_from_file(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("[Verse]\nHello from a file\n[Chorus]\nFile song")
            f.flush()
            try:
                result = runner.invoke(
                    cli,
                    [
                        "--token",
                        "test-token",
                        "custom",
                        "-l",
                        f"@{f.name}",
                        "-t",
                        "File Song",
                        "-s",
                        "rock",
                        "--json",
                    ],
                )
                assert result.exit_code == 0
            finally:
                os.unlink(f.name)

    def test_custom_lyrics_file_not_found(self, runner):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "custom",
                "-l",
                "@nonexistent_file.txt",
                "-t",
                "Test",
                "-s",
                "pop",
            ],
        )
        assert result.exit_code != 0

    @respx.mock
    def test_extend(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "extend", "audio-123", "--continue-at", "120", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_cover(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "cover", "audio-123", "-s", "jazz, smooth", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_remaster(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "remaster", "audio-123", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_concat(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "concat", "audio-123", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_generate_persona(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate-persona",
                "audio-123",
                "--persona-id",
                "persona-456",
                "-p",
                "A rock ballad",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_stems(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "stems", "audio-123", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_replace_section(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "replace-section",
                "audio-123",
                "--start",
                "30",
                "--end",
                "60",
                "-l",
                "[Chorus]\nNew lyrics",
                "-s",
                "rock",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_upload_extend(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "upload-extend",
                "audio-123",
                "-l",
                "[Verse]\nNew verse",
                "--continue-at",
                "60",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_upload_cover(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "upload-cover",
                "audio-123",
                "-s",
                "jazz, smooth piano",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_mashup(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "mashup", "audio-1", "audio-2", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_remaster_with_model(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "remaster", "audio-123", "--model", "chirp-v5", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_concat_with_callback(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "concat",
                "audio-123",
                "--callback-url",
                "https://example.com/callback",
                "--json",
            ],
        )
        assert result.exit_code == 0


# ─── Lyrics Commands ──────────────────────────────────────────────────────


class TestLyricsCommands:
    """Tests for lyrics commands."""

    @respx.mock
    def test_lyrics_json(self, runner, mock_lyrics_response):
        respx.post("https://api.acedata.cloud/suno/lyrics").mock(
            return_value=Response(200, json=mock_lyrics_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "lyrics", "A love song", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["task_id"] == "lyrics-task-123"

    @respx.mock
    def test_lyrics_rich_output(self, runner, mock_lyrics_response):
        respx.post("https://api.acedata.cloud/suno/lyrics").mock(
            return_value=Response(200, json=mock_lyrics_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "lyrics", "A love song"])
        assert result.exit_code == 0
        assert "lyrics-task-123" in result.output

    @respx.mock
    def test_mashup_lyrics(self, runner, mock_lyrics_response):
        respx.post("https://api.acedata.cloud/suno/mashup-lyrics").mock(
            return_value=Response(200, json=mock_lyrics_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "mashup-lyrics",
                "--lyrics-a",
                "verse A text",
                "--lyrics-b",
                "verse B text",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_optimize_style(self, runner, mock_style_response):
        respx.post("https://api.acedata.cloud/suno/style").mock(
            return_value=Response(200, json=mock_style_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "optimize-style", "rock music", "--json"]
        )
        assert result.exit_code == 0

    @respx.mock
    def test_optimize_style_rich(self, runner, mock_style_response):
        respx.post("https://api.acedata.cloud/suno/style").mock(
            return_value=Response(200, json=mock_style_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "optimize-style", "rock music"])
        assert result.exit_code == 0
        assert "upbeat pop rock" in result.output


# ─── Media Commands ───────────────────────────────────────────────────────


class TestMediaCommands:
    """Tests for media conversion commands."""

    @respx.mock
    def test_mp4(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/mp4").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "mp4", "audio-123"])
        assert result.exit_code == 0
        assert "video_url" in result.output or "mp4" in result.output.lower()

    @respx.mock
    def test_wav(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/wav").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "wav", "audio-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_midi(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/midi").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "midi", "audio-123"])
        assert result.exit_code == 0

    @respx.mock
    def test_timing(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/timing").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "timing", "audio-123", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_vocals(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/vox").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "vocals", "audio-123"])
        assert result.exit_code == 0


# ─── Task Commands ────────────────────────────────────────────────────────


class TestTaskCommands:
    """Tests for task management commands."""

    @respx.mock
    def test_task_json(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/suno/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-abc", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"][0]["id"] == "task-123"

    @respx.mock
    def test_task_rich_output(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/suno/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "task", "task-abc"])
        assert result.exit_code == 0
        assert "task-123" in result.output

    @respx.mock
    def test_tasks_batch(self, runner, mock_task_response):
        respx.post("https://api.acedata.cloud/suno/tasks").mock(
            return_value=Response(200, json=mock_task_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "tasks", "task-1", "task-2", "--json"]
        )
        assert result.exit_code == 0


# ─── Persona & Upload Commands ────────────────────────────────────────────


class TestPersonaCommands:
    """Tests for persona and upload commands."""

    @respx.mock
    def test_persona(self, runner, mock_persona_response):
        respx.post("https://api.acedata.cloud/suno/persona").mock(
            return_value=Response(200, json=mock_persona_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "persona", "audio-123", "-n", "My Voice"]
        )
        assert result.exit_code == 0
        assert "persona-id-456" in result.output

    @respx.mock
    def test_upload(self, runner, mock_upload_response):
        respx.post("https://api.acedata.cloud/suno/upload").mock(
            return_value=Response(200, json=mock_upload_response)
        )
        result = runner.invoke(
            cli, ["--token", "test-token", "upload", "https://example.com/audio.mp3"]
        )
        assert result.exit_code == 0
        assert "upload-id-789" in result.output


# ─── Info Commands ────────────────────────────────────────────────────────


class TestInfoCommands:
    """Tests for informational commands."""

    def test_models(self, runner):
        result = runner.invoke(cli, ["models"])
        assert result.exit_code == 0
        assert "chirp-v5-5" in result.output
        assert "chirp-v5" in result.output
        assert "chirp-v4-5" in result.output
        assert "chirp-v3-0" in result.output

    def test_actions(self, runner):
        result = runner.invoke(cli, ["actions"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "extend" in result.output
        assert "cover" in result.output
        assert "concat" in result.output

    def test_lyric_format(self, runner):
        result = runner.invoke(cli, ["lyric-format"])
        assert result.exit_code == 0
        assert "Verse" in result.output
        assert "Chorus" in result.output
        assert "Bridge" in result.output

    def test_config(self, runner):
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "API Base URL" in result.output
        assert "acedata.cloud" in result.output


# ─── New Commands (API Sync) ──────────────────────────────────────────────


class TestNewGenerateCommands:
    """Tests for newly added generation commands."""

    @respx.mock
    def test_generate_persona_vox(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate-persona-vox",
                "audio-123",
                "--persona-id",
                "per-456",
                "-p",
                "A jazz ballad",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_all_stems(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(cli, ["--token", "test-token", "all-stems", "audio-123", "--json"])
        assert result.exit_code == 0

    @respx.mock
    def test_underpainting(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "underpainting",
                "audio-123",
                "--end",
                "60",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_overpainting(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "overpainting",
                "audio-123",
                "--start",
                "10",
                "--end",
                "60",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_samples(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            ["--token", "test-token", "samples", "audio-123", "--end", "30", "--json"],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_generate_with_variation_category(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "generate",
                "A happy song",
                "--variation-category",
                "high",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_custom_with_advanced_params(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "custom",
                "-l",
                "[Verse]\nHello",
                "-t",
                "Hello",
                "-s",
                "pop",
                "--weirdness",
                "0.5",
                "--style-influence",
                "0.8",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_cover_with_audio_weight(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "cover",
                "audio-123",
                "-s",
                "jazz",
                "--audio-weight",
                "0.7",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_upload_cover_with_audio_weight(self, runner, mock_audio_response):
        respx.post("https://api.acedata.cloud/suno/audios").mock(
            return_value=Response(200, json=mock_audio_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "upload-cover",
                "audio-123",
                "-s",
                "jazz",
                "--audio-weight",
                "0.7",
                "--json",
            ],
        )
        assert result.exit_code == 0


class TestUpdatedMediaCommands:
    """Tests for updated media commands with new parameters."""

    @respx.mock
    def test_wav_with_callback(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/wav").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "wav",
                "audio-123",
                "--callback-url",
                "https://example.com/cb",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_midi_with_callback(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/midi").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "midi",
                "audio-123",
                "--callback-url",
                "https://example.com/cb",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_vocals_with_time_range(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/vox").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "vocals",
                "audio-123",
                "--vocal-start",
                "10",
                "--vocal-end",
                "60",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_vocals_with_callback(self, runner, mock_media_response):
        respx.post("https://api.acedata.cloud/suno/vox").mock(
            return_value=Response(200, json=mock_media_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "vocals",
                "audio-123",
                "--callback-url",
                "https://example.com/cb",
                "--json",
            ],
        )
        assert result.exit_code == 0


class TestUpdatedPersonaCommand:
    """Tests for updated persona command with new parameters."""

    @respx.mock
    def test_persona_with_vox_audio_id(self, runner, mock_persona_response):
        respx.post("https://api.acedata.cloud/suno/persona").mock(
            return_value=Response(200, json=mock_persona_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "persona",
                "audio-123",
                "--name",
                "My Voice",
                "--vox-audio-id",
                "vox-456",
                "--json",
            ],
        )
        assert result.exit_code == 0

    @respx.mock
    def test_persona_with_time_range(self, runner, mock_persona_response):
        respx.post("https://api.acedata.cloud/suno/persona").mock(
            return_value=Response(200, json=mock_persona_response)
        )
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "persona",
                "audio-123",
                "--name",
                "My Voice",
                "--vocal-start",
                "5",
                "--vocal-end",
                "30",
                "--description",
                "Smooth male voice",
                "--json",
            ],
        )
        assert result.exit_code == 0
