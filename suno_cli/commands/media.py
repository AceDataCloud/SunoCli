"""Media conversion commands."""

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import print_error, print_json, print_success


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def mp4(ctx: click.Context, audio_id: str, output_json: bool) -> None:
    """Get an MP4 video version of a generated song.

    AUDIO_ID is the ID of the song.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_mp4(audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            url = result.get("data", {}).get("video_url", "")
            if url:
                print_success(f"MP4 URL: {url}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def wav(ctx: click.Context, audio_id: str, callback_url: str | None, output_json: bool) -> None:
    """Get lossless WAV format of a generated song.

    AUDIO_ID is the ID of the song.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_wav(audio_id=audio_id, callback_url=callback_url)
        if output_json:
            print_json(result)
        else:
            url = result.get("data", {}).get("audio_url", "")
            if url:
                print_success(f"WAV URL: {url}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def midi(ctx: click.Context, audio_id: str, callback_url: str | None, output_json: bool) -> None:
    """Get MIDI data extracted from a generated song.

    AUDIO_ID is the ID of the song.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_midi(audio_id=audio_id, callback_url=callback_url)
        if output_json:
            print_json(result)
        else:
            url = result.get("data", {}).get("midi_url", "")
            if url:
                print_success(f"MIDI URL: {url}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def timing(ctx: click.Context, audio_id: str, output_json: bool) -> None:
    """Get timing and subtitle data for a generated song.

    AUDIO_ID is the ID of the song.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_timing(audio_id=audio_id)
        if output_json:
            print_json(result)
        else:
            print_json(result.get("data", result))
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("vocals")
@click.argument("audio_id")
@click.option(
    "--vocal-start",
    type=float,
    default=None,
    help="Start time of the vocal in the audio (seconds).",
)
@click.option(
    "--vocal-end", type=float, default=None, help="End time of the vocal in the audio (seconds)."
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def extract_vocals(
    ctx: click.Context,
    audio_id: str,
    vocal_start: float | None,
    vocal_end: float | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extract the vocal track from a generated song.

    AUDIO_ID is the ID of the song.
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_vox(
            audio_id=audio_id,
            vocal_start=vocal_start,
            vocal_end=vocal_end,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            url = result.get("data", {}).get("audio_url", "")
            if url:
                print_success(f"Vocals URL: {url}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
