"""Output formatting utilities for Suno CLI."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()
error_console = Console(stderr=True)

# Suno model versions
SUNO_MODELS = [
    "chirp-v3-0",
    "chirp-v3-5",
    "chirp-v4",
    "chirp-v4-5",
    "chirp-v4-5-plus",
    "chirp-v5",
    "chirp-v5-5",
]

DEFAULT_MODEL = "chirp-v4-5"


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print_json(json.dumps(data, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    error_console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_audio_result(data: dict[str, Any]) -> None:
    """Print audio generation result in a nice format."""
    task_id = data.get("task_id")
    if task_id:
        print_success(f"Task created: {task_id}")

    items = data.get("data", [])
    if not isinstance(items, list):
        print_json(data)
        return

    for item in items:
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Key", style="bold cyan", width=16)
        table.add_column("Value")

        if "title" in item:
            table.add_row("Title", item["title"])
        if "style" in item:
            table.add_row("Style", item["style"])
        if "duration" in item:
            table.add_row("Duration", f"{item['duration']:.1f}s")
        if "model_name" in item:
            table.add_row("Model", item["model_name"])
        if "audio_url" in item:
            table.add_row("Audio URL", item["audio_url"])
        if "video_url" in item:
            table.add_row("Video URL", item["video_url"])
        if "image_url" in item:
            table.add_row("Cover", item["image_url"])
        if "id" in item:
            table.add_row("Audio ID", item["id"])

        lyric = item.get("lyric", "")
        if lyric:
            # Truncate long lyrics
            lines = lyric.strip().split("\n")
            preview = "\n".join(lines[:6])
            if len(lines) > 6:
                preview += f"\n... ({len(lines) - 6} more lines)"
            table.add_row("Lyrics", preview)

        console.print(Panel(table, title="[bold]Generated Song[/bold]", expand=False))


def print_lyrics_result(data: dict[str, Any]) -> None:
    """Print lyrics generation result."""
    task_id = data.get("task_id")
    if task_id:
        print_success(f"Task created: {task_id}")

    items = data.get("data", [])
    if not isinstance(items, list):
        print_json(data)
        return

    for item in items:
        title = item.get("title", "Untitled")
        text = item.get("text", "")
        console.print(Panel(text, title=f"[bold]{title}[/bold]", expand=False))


def print_task_result(data: dict[str, Any]) -> None:
    """Print task query result."""
    items = data.get("data", [])
    if not isinstance(items, list):
        items = [data.get("data", data)]

    table = Table(title="Tasks")
    table.add_column("Task ID", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Progress")
    table.add_column("Audio URL")

    for item in items:
        if not item:
            continue
        status = item.get("status", "unknown")
        style = {
            "completed": "green",
            "processing": "yellow",
            "pending": "dim",
            "failed": "red",
        }.get(status, "white")

        audio_url = item.get("audio_url", "-")
        if audio_url and len(audio_url) > 50:
            audio_url = audio_url[:50] + "..."

        table.add_row(
            item.get("id", "-"),
            Text(status, style=style),
            item.get("progress", "-"),
            audio_url,
        )

    console.print(table)


def print_models() -> None:
    """Print available models."""
    table = Table(title="Available Suno Models")
    table.add_column("Model", style="cyan")
    table.add_column("Version", style="bold")
    table.add_column("Max Duration")
    table.add_column("Notes")

    models = [
        ("chirp-v5-5", "V5.5", "8 min", "Latest, best quality"),
        ("chirp-v5", "V5", "8 min", "High quality"),
        ("chirp-v4-5-plus", "V4.5+", "8 min", "Enhanced quality"),
        ("chirp-v4-5", "V4.5", "4 min", "Vocal gender control (default)"),
        ("chirp-v4", "V4", "150s", "Stable"),
        ("chirp-v3-5", "V3.5", "120s", "Fast"),
        ("chirp-v3-0", "V3", "120s", "Legacy"),
    ]
    for model, version, duration, notes in models:
        table.add_row(model, version, duration, notes)

    console.print(table)
