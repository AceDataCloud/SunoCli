"""Music generation commands."""

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import (
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
@click.option(
    "--variation-category",
    default=None,
    type=click.Choice(["high", "normal", "subtle"]),
    help="Variation level (v5+ only).",
)
@click.option("--weirdness", type=float, default=None, help="Weirdness level (custom mode only).")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    instrumental: bool,
    variation_category: str | None,
    weirdness: float | None,
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
            variation_category=variation_category,
            weirdness=weirdness,
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
@click.option(
    "--variation-category",
    default=None,
    type=click.Choice(["high", "normal", "subtle"]),
    help="Variation level (v5+ only).",
)
@click.option("--weirdness", type=float, default=None, help="Weirdness level (advanced custom mode).")
@click.option("--style-influence", type=float, default=None, help="Style influence strength (advanced custom mode).")
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
    variation_category: str | None,
    weirdness: float | None,
    style_influence: float | None,
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
            variation_category=variation_category,
            weirdness=weirdness,
            style_influence=style_influence,
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
@click.option("--audio-weight", type=float, default=None, help="Audio weight for the cover (advanced).")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def cover(
    ctx: click.Context,
    audio_id: str,
    style: str,
    model: str,
    audio_weight: float | None,
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
            audio_weight=audio_weight,
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
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def remaster(
    ctx: click.Context,
    audio_id: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Remaster an existing song to improve audio quality.

    AUDIO_ID is the ID of the song to remaster.

    Examples:

      suno remaster abc123

      suno remaster abc123 --model chirp-v5
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="remaster",
            audio_id=audio_id,
            model=model,
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
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def concat(
    ctx: click.Context,
    audio_id: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Merge extended segments into complete audio.

    AUDIO_ID is the ID of the last segment of an extended song chain.
    Suno will automatically find and merge all connected segments.

    Examples:

      suno concat abc123
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="concat",
            audio_id=audio_id,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("generate-persona")
@click.argument("audio_id")
@click.option("--persona-id", required=True, help="ID of the persona to use.")
@click.option("-p", "--prompt", required=True, help="Description of the music to generate.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate_persona(
    ctx: click.Context,
    audio_id: str,
    persona_id: str,
    prompt: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate music using a saved persona (voice style).

    AUDIO_ID is the ID of a reference audio to base the generation on.

    Examples:

      suno generate-persona abc123 --persona-id per456 -p "A rock ballad"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="artist_consistency",
            audio_id=audio_id,
            persona_id=persona_id,
            prompt=prompt,
            model=model,
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
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def stems(
    ctx: click.Context,
    audio_id: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Separate a song into individual stems (vocals + instrumental).

    AUDIO_ID is the ID of the song to separate.

    Examples:

      suno stems abc123
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="stems",
            audio_id=audio_id,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("replace-section")
@click.argument("audio_id")
@click.option("--start", "section_start", required=True, type=float, help="Start time in seconds.")
@click.option("--end", "section_end", required=True, type=float, help="End time in seconds.")
@click.option("-l", "--lyric", default=None, help="New lyrics for the replaced section.")
@click.option("-s", "--style", default=None, help="Music style for the replacement.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def replace_section(
    ctx: click.Context,
    audio_id: str,
    section_start: float,
    section_end: float,
    lyric: str | None,
    style: str | None,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Replace a time range in a song with new content.

    AUDIO_ID is the ID of the song to modify.

    Examples:

      suno replace-section abc123 --start 30 --end 60 -l "[Chorus]\\nNew lyrics" -s "rock"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "replace_section",
        "audio_id": audio_id,
        "replace_section_start": section_start,
        "replace_section_end": section_end,
        "model": model,
        "callback_url": callback_url,
    }
    if lyric:
        payload["lyric"] = lyric
        payload["custom"] = True
    if style:
        payload["style"] = style

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("upload-extend")
@click.argument("audio_id")
@click.option("-l", "--lyric", required=True, help="Lyrics for the extension.")
@click.option(
    "--continue-at",
    type=float,
    required=True,
    help="Timestamp in seconds to extend from.",
)
@click.option("-s", "--style", default=None, help="Music style for the extension.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upload_extend(
    ctx: click.Context,
    audio_id: str,
    lyric: str,
    continue_at: float,
    style: str | None,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Extend uploaded audio with AI-generated continuation.

    AUDIO_ID is the ID of the uploaded audio (from 'suno upload').

    Examples:

      suno upload-extend abc123 -l "[Verse]\\nNew verse" --continue-at 60
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "upload_extend",
        "audio_id": audio_id,
        "lyric": lyric,
        "continue_at": continue_at,
        "custom": True,
        "model": model,
        "callback_url": callback_url,
    }
    if style:
        payload["style"] = style

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("upload-cover")
@click.argument("audio_id")
@click.option("-s", "--style", default=None, help="Target music style for the cover.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--audio-weight", type=float, default=None, help="Audio weight for the cover (advanced).")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upload_cover(
    ctx: click.Context,
    audio_id: str,
    style: str | None,
    model: str,
    audio_weight: float | None,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Create a cover of uploaded audio in a different style.

    AUDIO_ID is the ID of the uploaded audio (from 'suno upload').

    Examples:

      suno upload-cover abc123 --style "jazz, smooth piano"
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "action": "upload_cover",
        "audio_id": audio_id,
        "model": model,
        "callback_url": callback_url,
    }
    if style:
        payload["style"] = style
    if audio_weight is not None:
        payload["audio_weight"] = audio_weight

    try:
        result = client.generate_audio(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("audio_ids", nargs=-1, required=True)
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def mashup(
    ctx: click.Context,
    audio_ids: tuple[str, ...],
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Blend multiple songs together into a mashup.

    AUDIO_IDS are the IDs of 2 or more songs to mashup (space-separated).

    Examples:

      suno mashup abc123 def456

      suno mashup abc123 def456 ghi789 --model chirp-v5
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="mashup",
            mashup_audio_ids=list(audio_ids),
            model=model,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("generate-persona-vox")
@click.argument("audio_id")
@click.option("--persona-id", required=True, help="ID of the persona to use.")
@click.option("-p", "--prompt", required=True, help="Description of the music to generate.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate_persona_vox(
    ctx: click.Context,
    audio_id: str,
    persona_id: str,
    prompt: str,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate music using a persona's vocal style (vox mode).

    AUDIO_ID is the ID of a reference audio to base the generation on.

    Examples:

      suno generate-persona-vox abc123 --persona-id per456 -p "A jazz ballad"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="artist_consistency_vox",
            audio_id=audio_id,
            persona_id=persona_id,
            prompt=prompt,
            model=model,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("all-stems")
@click.argument("audio_id")
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def all_stems(
    ctx: click.Context,
    audio_id: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Separate a song into all individual stems.

    AUDIO_ID is the ID of the song to separate.

    Examples:

      suno all-stems abc123
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="all_stems",
            audio_id=audio_id,
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
@click.option("--start", "underpainting_start", type=float, default=None, help="Start time in seconds (default: 0).")
@click.option("--end", "underpainting_end", type=float, default=None, help="End time in seconds.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def underpainting(
    ctx: click.Context,
    audio_id: str,
    underpainting_start: float | None,
    underpainting_end: float | None,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Add AI-generated accompaniment to an uploaded song.

    AUDIO_ID is the ID of the uploaded audio (from 'suno upload').

    Examples:

      suno underpainting abc123 --end 60
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="underpainting",
            audio_id=audio_id,
            underpainting_start=underpainting_start,
            underpainting_end=underpainting_end,
            model=model,
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
@click.option("--start", "overpainting_start", type=float, default=None, help="Start time in seconds (default: 0).")
@click.option("--end", "overpainting_end", type=float, default=None, help="End time in seconds.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def overpainting(
    ctx: click.Context,
    audio_id: str,
    overpainting_start: float | None,
    overpainting_end: float | None,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Add AI-generated vocals to an uploaded song.

    AUDIO_ID is the ID of the uploaded audio (from 'suno upload').

    Examples:

      suno overpainting abc123 --end 60
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="overpainting",
            audio_id=audio_id,
            overpainting_start=overpainting_start,
            overpainting_end=overpainting_end,
            model=model,
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
@click.option("--start", "samples_start", type=float, default=None, help="Start time in seconds (default: 0).")
@click.option("--end", "samples_end", type=float, default=None, help="End time in seconds.")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SUNO_MODELS),
    default=DEFAULT_MODEL,
    help="Suno model version.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def samples(
    ctx: click.Context,
    audio_id: str,
    samples_start: float | None,
    samples_end: float | None,
    model: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Add AI-generated samples to an uploaded song.

    AUDIO_ID is the ID of the uploaded audio (from 'suno upload').

    Examples:

      suno samples abc123 --end 30
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_audio(
            action="samples",
            audio_id=audio_id,
            samples_start=samples_start,
            samples_end=samples_end,
            model=model,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_audio_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
