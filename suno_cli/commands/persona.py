"""Persona management commands."""

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import print_error, print_json, print_success


@click.command()
@click.argument("audio_id")
@click.option("-n", "--name", required=True, help="Name for the persona.")
@click.option("--vox-audio-id", default=None, help="Audio ID for the vocal reference.")
@click.option("--vocal-start", type=float, default=None, help="Start time of the vocal in the audio (seconds).")
@click.option("--vocal-end", type=float, default=None, help="End time of the vocal in the audio (seconds).")
@click.option("--description", default=None, help="Description of the singer's style.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def persona(
    ctx: click.Context,
    audio_id: str,
    name: str,
    vox_audio_id: str | None,
    vocal_start: float | None,
    vocal_end: float | None,
    description: str | None,
    output_json: bool,
) -> None:
    """Create a persona (saved voice style) from an existing song.

    AUDIO_ID is the ID of the song to create the persona from.

    Examples:

      suno persona abc123 --name "My Voice Style"

      suno persona abc123 --name "My Voice Style" --vox-audio-id vox456 --vocal-start 10 --vocal-end 30
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.create_persona(
            audio_id=audio_id,
            name=name,
            vox_audio_id=vox_audio_id,
            vocal_start=vocal_start,
            vocal_end=vocal_end,
            description=description,
        )
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            persona_id = data.get("id", "")
            if persona_id:
                print_success(f"Persona created: {name} (ID: {persona_id})")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("upload")
@click.argument("audio_url")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upload(
    ctx: click.Context,
    audio_url: str,
    output_json: bool,
) -> None:
    """Upload an external audio file for use in subsequent operations.

    AUDIO_URL is the URL of the audio file to upload.

    Examples:

      suno upload "https://example.com/my-song.mp3"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upload_audio(audio_url=audio_url)
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            upload_id = data.get("id", "")
            if upload_id:
                print_success(f"Uploaded: {upload_id}")
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
