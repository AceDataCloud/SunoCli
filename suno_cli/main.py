#!/usr/bin/env python3
"""
Suno CLI - AI Music Generation via AceDataCloud API.

A command-line tool for generating AI music using Suno
through the AceDataCloud platform.
"""

from importlib import metadata

import click
from dotenv import load_dotenv

from suno_cli.commands.generate import (
    all_stems,
    concat,
    cover,
    custom,
    extend,
    generate,
    generate_persona,
    generate_persona_vox,
    mashup,
    overpainting,
    remaster,
    replace_section,
    samples,
    stems,
    underpainting,
    upload_cover,
    upload_extend,
)
from suno_cli.commands.info import actions, config, lyric_format, models
from suno_cli.commands.lyrics import lyrics, mashup_lyrics, optimize_style
from suno_cli.commands.media import extract_vocals, midi, mp4, timing, wav
from suno_cli.commands.persona import persona, upload
from suno_cli.commands.task import task, tasks_batch, wait

load_dotenv()


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("suno-cli")
    except metadata.PackageNotFoundError:
        return "dev"


@click.group()
@click.version_option(version=get_version(), prog_name="suno-cli")
@click.option(
    "--token",
    envvar="ACEDATACLOUD_API_TOKEN",
    help="API token (or set ACEDATACLOUD_API_TOKEN env var).",
)
@click.pass_context
def cli(ctx: click.Context, token: str | None) -> None:
    """Suno CLI - AI Music Generation powered by AceDataCloud.

    Generate AI music, lyrics, and manage audio projects from the command line.

    Get your API token at https://platform.acedata.cloud

    \b
    Examples:
      suno generate "A happy birthday song"
      suno custom -l "[Verse]\\nHello" -t "Hello" -s "pop"
      suno lyrics "A love song about the ocean"
      suno task abc123-def456
      suno wait abc123 --interval 5

    Set your token:
      export ACEDATACLOUD_API_TOKEN=your_token
    """
    ctx.ensure_object(dict)
    ctx.obj["token"] = token


# Register commands — generation
cli.add_command(generate)
cli.add_command(custom)
cli.add_command(extend)
cli.add_command(cover)
cli.add_command(remaster)
cli.add_command(concat)
cli.add_command(generate_persona)
cli.add_command(generate_persona_vox)
cli.add_command(stems)
cli.add_command(all_stems)
cli.add_command(replace_section)
cli.add_command(upload_extend)
cli.add_command(upload_cover)
cli.add_command(mashup)
cli.add_command(underpainting)
cli.add_command(overpainting)
cli.add_command(samples)

# Register commands — lyrics
cli.add_command(lyrics)
cli.add_command(mashup_lyrics)
cli.add_command(optimize_style)

# Register commands — media
cli.add_command(mp4)
cli.add_command(wav)
cli.add_command(midi)
cli.add_command(timing)
cli.add_command(extract_vocals)

# Register commands — tasks
cli.add_command(task)
cli.add_command(tasks_batch)
cli.add_command(wait)

# Register commands — persona & upload
cli.add_command(persona)
cli.add_command(upload)

# Register commands — info
cli.add_command(models)
cli.add_command(actions)
cli.add_command(lyric_format)
cli.add_command(config)


if __name__ == "__main__":
    cli()
