"""Lyrics commands."""

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import print_error, print_json, print_lyrics_result


@click.command()
@click.argument("prompt")
@click.option(
    "--model",
    type=click.Choice(["default", "remi-v1"]),
    default="default",
    help="Lyrics model version.",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def lyrics(
    ctx: click.Context,
    prompt: str,
    model: str,
    output_json: bool,
) -> None:
    """Generate song lyrics from a prompt.

    PROMPT is a description of the lyrics to generate.

    Examples:

      suno lyrics "A love song about the ocean at sunset"

      suno lyrics "Funny rap about programming bugs" --model remi-v1
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_lyrics(prompt=prompt, model=model)
        if output_json:
            print_json(result)
        else:
            print_lyrics_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("mashup-lyrics")
@click.option("--lyrics-a", required=True, help="First set of lyrics.")
@click.option("--lyrics-b", required=True, help="Second set of lyrics.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def mashup_lyrics(
    ctx: click.Context,
    lyrics_a: str,
    lyrics_b: str,
    output_json: bool,
) -> None:
    """Generate mashup lyrics by combining two sets of lyrics.

    Examples:

      suno mashup-lyrics --lyrics-a "verse 1 text" --lyrics-b "verse 2 text"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.mashup_lyrics(lyrics_a=lyrics_a, lyrics_b=lyrics_b)
        if output_json:
            print_json(result)
        else:
            print_lyrics_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("optimize-style")
@click.argument("prompt")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def optimize_style(
    ctx: click.Context,
    prompt: str,
    output_json: bool,
) -> None:
    """Optimize a style description for better generation results.

    PROMPT is the style description to optimize.

    Examples:

      suno optimize-style "rock music with guitar"
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.get_style(prompt=prompt)
        if output_json:
            print_json(result)
        else:
            data = result.get("data", {})
            if isinstance(data, dict) and "text" in data:
                from rich.panel import Panel

                from suno_cli.core.output import console

                console.print(
                    Panel(data["text"], title="[bold]Optimized Style[/bold]", expand=False)
                )
            else:
                print_json(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
