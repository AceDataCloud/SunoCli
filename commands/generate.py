"""Music generation commands."""

import click

from core.client import get_client
from core.exceptions import SunoError
from core.output import (
    DEFAULT_MODEL,
    SUNO_MODELS,
    print_audio_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option(
    "--instrumental",
    is_flag=True,
    default=False,
    help="Generate instrumental music without vocals.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    instrumental: bool,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate music from a text prompt (Inspiration Mode).

    PROMPT is a description of the music to generate. Be descriptive about genre,
    mood, instruments, and theme.

    Examples:

      suno generate "A happy birthday song with acoustic guitar"

      suno generate "Epic orchestral battle music" --model chirp-v5

      suno generate "Chill lo-fi beat for studying" --instrumental
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="generate",
            prompt=prompt,
            model=model,
            instrumental=instrumental,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.option("-l", "--lyric", required=True, help="Song lyrics with section markers.")
@click.option("-t", "--title", required=True, help="Title of the song.")
@click.option(
    "-s",
    "--style",
    required=True,
    help="Music style (e.g., 'upbeat pop rock, energetic drums').",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option(
    "--gender",
    type=click.Choice(["", "f", "m"]),
    default="",
    help="Vocal gender (v4.5+ only). f=female, m=male.",
)
@click.option("--negative-style", default=None, help="Styles to avoid.")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def custom(
    ctx: click.Context,
    lyric: str,
    title: str,
    style: str,
    model: str,
    gender: str,
    negative_style: str | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate music with custom lyrics, title, and style.

    Examples:

      suno custom -l "[Verse]\\nHello world" -t "Hello" -s "pop, upbeat"

      suno custom --lyric @lyrics.txt --title "My Song" --style "rock"
    """
    # Support reading lyrics from file with @filename syntax
    if lyric.startswith("@"):
        filepath = lyric[1:]
        try:
            with open(filepath) as f:
                lyric = f.read()
        except FileNotFoundError as e:
            print_error(f"File not found: {filepath}")
            raise SystemExit(1) from e

    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="custom",
            lyric=lyric,
            title=title,
            style=style,
            model=model,
            vocal_gender=gender or None,
            negative_style=negative_style,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "--continue-at",
    type=float,
    default=0.0,
    help="Timestamp in seconds to extend from.",
)
@click.option("-l", "--lyric", default=None, help="Lyrics for the extension.")
@click.option("-s", "--style", default=None, help="Style for the extension.")
@click.option("-t", "--title", default=None, help="Title for the extension.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extend(
    ctx: click.Context,
    audio_id: str,
    continue_at: float,
    lyric: str | None,
    style: str | None,
    title: str | None,
    model: str,
    output_json: bool,
) -> None:
    """Extend an existing song from a timestamp.

    AUDIO_ID is the ID of the song to extend.

    Examples:

      suno extend abc123 --continue-at 120 --lyric "[Bridge]\\nNew section"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="extend",
            audio_id=audio_id,
            continue_at=continue_at,
            lyric=lyric,
            style=style,
            title=title,
            model=model,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option(
    "-s",
    "--style",
    required=True,
    help="New style for the cover version.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def cover(
    ctx: click.Context,
    audio_id: str,
    style: str,
    model: str,
    output_json: bool,
) -> None:
    """Create a cover/remix of an existing song.

    AUDIO_ID is the ID of the song to cover.

    Examples:

      suno cover abc123 --style "jazz, smooth, piano"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="cover",
            audio_id=audio_id,
            style=style,
            model=model,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def remaster(
    ctx: click.Context,
    audio_id: str,
    output_json: bool,
) -> None:
    """Remaster an existing song to improve audio quality.

    AUDIO_ID is the ID of the song to remaster.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(action="remaster", audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def concat(
    ctx: click.Context,
    audio_id: str,
    output_json: bool,
) -> None:
    """Merge extended segments into complete audio.

    AUDIO_ID is the ID of the root song to concatenate.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(action="concat", audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
