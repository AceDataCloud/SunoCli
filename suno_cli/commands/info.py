"""Info and utility commands."""

import click

from suno_cli.core.output import console, print_models


@click.command()
def models() -> None:
    """List available Suno models."""
    print_models()


@click.command()
def actions() -> None:
    """List available API actions."""
    from rich.table import Table

    table = Table(title="Available Actions")
    table.add_column("Action", style="cyan")
    table.add_column("Description")

    action_list = [
        ("generate", "Generate music from a text prompt (Inspiration Mode)"),
        ("custom", "Generate with custom lyrics, title, and style"),
        ("extend", "Extend an existing song from a timestamp"),
        ("cover", "Create a cover/remix version"),
        ("concat", "Merge extended segments into complete audio"),
        ("remaster", "Remaster a song to improve quality"),
        ("stems", "Separate a song into vocal + instrumental stems"),
        ("all_stems", "Separate a song into all individual stems"),
        ("replace_section", "Replace a time range with new content"),
        ("upload_extend", "Extend uploaded audio"),
        ("upload_cover", "Cover uploaded audio"),
        ("mashup", "Blend multiple songs together"),
        ("artist_consistency", "Generate music using a saved persona (CLI: generate-persona)"),
        (
            "artist_consistency_vox",
            "Generate using a persona's vocal style (CLI: generate-persona-vox)",
        ),
        ("underpainting", "Add AI accompaniment to uploaded audio"),
        ("overpainting", "Add AI vocals to uploaded audio"),
        ("samples", "Add AI samples to uploaded audio"),
    ]
    for action, desc in action_list:
        table.add_row(action, desc)

    console.print(table)


@click.command()
def lyric_format() -> None:
    """Show the lyrics formatting guide."""
    guide = """
[bold]Lyrics Format Guide[/bold]

Use section markers to structure your lyrics:

  [bold cyan][Verse 1][/bold cyan]
  Your verse lyrics here
  Second line of verse

  [bold cyan][Pre-Chorus][/bold cyan]
  Building up to the chorus

  [bold cyan][Chorus][/bold cyan]
  The main hook of your song
  Repeatable and catchy

  [bold cyan][Verse 2][/bold cyan]
  More story or emotion

  [bold cyan][Bridge][/bold cyan]
  A contrasting section

  [bold cyan][Outro][/bold cyan]
  Closing of the song

[bold]Available Markers:[/bold]
  [Intro], [Verse], [Pre-Chorus], [Chorus],
  [Post-Chorus], [Bridge], [Outro], [Break],
  [Instrumental], [Hook]

[bold]Tips:[/bold]
  • Keep verses 4-8 lines
  • Choruses should be memorable and repeatable
  • Use [Instrumental] for music-only sections
  • Number verses: [Verse 1], [Verse 2], etc.
  • chirp-v4-5: max 3000 chars, chirp-v5: max 5000 chars
"""
    console.print(guide)


@click.command()
def config() -> None:
    """Show current configuration."""
    from rich.table import Table

    from suno_cli.core.config import settings

    table = Table(title="Configuration", show_header=False)
    table.add_column("Key", style="bold")
    table.add_column("Value")

    table.add_row("API Base URL", settings.api_base_url)
    table.add_row(
        "API Token",
        f"{settings.api_token[:8]}...{settings.api_token[-4:]}"
        if len(settings.api_token) > 12
        else ("(not set)" if not settings.api_token else settings.api_token),
    )
    table.add_row("Default Model", settings.default_model)
    table.add_row("Request Timeout", f"{settings.request_timeout}s")

    console.print(table)
