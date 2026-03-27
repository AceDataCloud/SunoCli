"""Unit tests for output formatting module."""

import json

from suno_cli.core.output import (
    DEFAULT_MODEL,
    SUNO_MODELS,
    print_audio_result,
    print_error,
    print_json,
    print_lyrics_result,
    print_models,
    print_success,
    print_task_result,
)


class TestConstants:
    """Tests for module constants."""

    def test_suno_models_count(self):
        assert len(SUNO_MODELS) >= 4

    def test_default_model_in_models(self):
        assert DEFAULT_MODEL in SUNO_MODELS

    def test_models_include_all_versions(self):
        for model in ["chirp-v3-0", "chirp-v4", "chirp-v4-5", "chirp-v5", "chirp-v5-5"]:
            assert model in SUNO_MODELS


class TestPrintJson:
    """Tests for JSON output."""

    def test_print_json_dict(self, capsys):
        print_json({"key": "value", "num": 42})
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["key"] == "value"
        assert data["num"] == 42

    def test_print_json_unicode(self, capsys):
        print_json({"title": "音乐测试"})
        captured = capsys.readouterr()
        assert "音乐测试" in captured.out

    def test_print_json_nested(self, capsys):
        print_json({"data": [{"id": "a"}, {"id": "b"}]})
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["data"]) == 2


class TestPrintMessages:
    """Tests for error and success message output."""

    def test_print_error(self, capsys):
        print_error("something went wrong")
        captured = capsys.readouterr()
        assert "something went wrong" in captured.err

    def test_print_success(self, capsys):
        print_success("operation completed")
        captured = capsys.readouterr()
        assert "operation completed" in captured.out


class TestPrintAudioResult:
    """Tests for audio result formatting."""

    def test_print_audio_result(self, capsys, mock_audio_response):
        print_audio_result(mock_audio_response)
        captured = capsys.readouterr()
        assert "test-task-123" in captured.out
        assert "Test Song" in captured.out

    def test_print_audio_result_empty_data(self, capsys):
        print_audio_result({"success": True, "task_id": "t-1", "data": []})
        captured = capsys.readouterr()
        assert "t-1" in captured.out


class TestPrintLyricsResult:
    """Tests for lyrics result formatting."""

    def test_print_lyrics_result(self, capsys, mock_lyrics_response):
        print_lyrics_result(mock_lyrics_response)
        captured = capsys.readouterr()
        assert "lyrics-task-123" in captured.out
        assert "Test Song Title" in captured.out

    def test_print_lyrics_result_empty_data(self, capsys):
        print_lyrics_result({"success": True, "task_id": "l-1", "data": []})
        captured = capsys.readouterr()
        assert "l-1" in captured.out


class TestPrintTaskResult:
    """Tests for task result formatting."""

    def test_print_task_result(self, capsys, mock_task_response):
        print_task_result(mock_task_response)
        captured = capsys.readouterr()
        assert "task-123" in captured.out
        assert "completed" in captured.out.lower()


class TestPrintModels:
    """Tests for model listing."""

    def test_print_models(self, capsys):
        print_models()
        captured = capsys.readouterr()
        assert "chirp-v5-5" in captured.out
        assert "chirp-v5" in captured.out
        assert "chirp-v4-5" in captured.out
        assert "chirp-v3-0" in captured.out
