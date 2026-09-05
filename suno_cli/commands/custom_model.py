"""Custom music model management commands."""

from typing import Any

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import print_error, print_json, print_success


def _request(
    ctx: click.Context,
    payload: dict[str, Any],
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    client = get_client(ctx.obj.get("token"))
    try:
        return client.custom_models(idempotency_key=idempotency_key, **payload)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("custom-model-create")
@click.option("-n", "--name", required=True, help="Name for the custom model.")
@click.option(
    "--audio-url",
    "audio_urls",
    multiple=True,
    required=True,
    help="Authorized training audio URL. Repeat 6 to 24 times.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option(
    "--idempotency-key",
    default=None,
    help="Unique key to reuse when retrying this creation request.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def custom_model_create(
    ctx: click.Context,
    name: str,
    audio_urls: tuple[str, ...],
    callback_url: str | None,
    idempotency_key: str | None,
    output_json: bool,
) -> None:
    """Create a custom model from 6 to 24 audio files."""
    if not 6 <= len(audio_urls) <= 24:
        raise click.BadParameter(
            "must be provided between 6 and 24 times.",
            param_hint="--audio-url",
        )

    result = _request(
        ctx,
        {
            "action": "create",
            "name": name,
            "audio_urls": list(audio_urls),
            "callback_url": callback_url,
        },
        idempotency_key,
    )
    if output_json:
        print_json(result)
        return

    data = result.get("data", result)
    model_id = data.get("id") if isinstance(data, dict) else None
    if model_id:
        print_success(f"Custom model creation started: {model_id}")
    else:
        print_json(result)


@click.command("custom-model")
@click.argument("model_id")
@click.pass_context
def custom_model(ctx: click.Context, model_id: str) -> None:
    """Retrieve a custom model by ID."""
    print_json(_request(ctx, {"action": "retrieve", "id": model_id}))


@click.command("custom-models")
@click.option("--limit", type=click.IntRange(min=1), default=20, show_default=True)
@click.option("--offset", type=click.IntRange(min=0), default=0, show_default=True)
@click.option("--status", default=None, help="Filter models by status.")
@click.pass_context
def custom_models(
    ctx: click.Context,
    limit: int,
    offset: int,
    status: str | None,
) -> None:
    """Retrieve custom models for the current application."""
    print_json(
        _request(
            ctx,
            {
                "action": "retrieve_batch",
                "limit": limit,
                "offset": offset,
                "status": status,
            },
        )
    )


@click.command("custom-model-generate")
@click.argument("model_id")
@click.option("-t", "--title", required=True, help="Song title.")
@click.option("-l", "--lyric", required=True, help="Song lyrics.")
@click.option("-s", "--style", required=True, help="Musical style.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def custom_model_generate(
    ctx: click.Context,
    model_id: str,
    title: str,
    lyric: str,
    style: str,
    output_json: bool,
) -> None:
    """Generate a song with a ready custom model."""
    result = _request(
        ctx,
        {
            "action": "generate",
            "id": model_id,
            "title": title,
            "lyric": lyric,
            "style": style,
        },
    )
    if output_json:
        print_json(result)
        return

    task_id = result.get("task_id")
    if task_id:
        print_success(f"Task created: {task_id}")
    else:
        print_json(result)


@click.command("custom-model-delete")
@click.argument("model_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def custom_model_delete(ctx: click.Context, model_id: str, output_json: bool) -> None:
    """Archive a custom model and prevent further use."""
    result = _request(ctx, {"action": "delete", "id": model_id})
    if output_json:
        print_json(result)
    else:
        print_success(f"Custom model archived: {model_id}")
