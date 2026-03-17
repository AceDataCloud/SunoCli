"""Task tracking commands."""

import time

import click

from suno_cli.core.client import get_client
from suno_cli.core.exceptions import SunoError
from suno_cli.core.output import console, print_error, print_json, print_task_result


@click.command()
@click.argument("task_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def task(ctx: click.Context, task_id: str, output_json: bool) -> None:
    """Query a single task status.

    TASK_ID is the ID of the task to query.

    Examples:

      suno task abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(id=task_id)
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("tasks")
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def tasks_batch(ctx: click.Context, task_ids: tuple[str, ...], output_json: bool) -> None:
    """Query multiple tasks at once.

    TASK_IDS are the IDs of the tasks to query (space-separated).

    Examples:

      suno tasks abc123 def456 ghi789
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.query_task(ids=list(task_ids))
        if output_json:
            print_json(result)
        else:
            print_task_result(result)
    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("task_id")
@click.option(
    "--interval",
    type=float,
    default=10.0,
    help="Polling interval in seconds (default: 10).",
)
@click.option(
    "--timeout",
    type=float,
    default=600.0,
    help="Max wait time in seconds (default: 600).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def wait(
    ctx: click.Context,
    task_id: str,
    interval: float,
    timeout: float,
    output_json: bool,
) -> None:
    """Wait for a task to complete, polling periodically.

    TASK_ID is the ID of the task to wait for.

    Examples:

      suno wait abc123 --interval 5 --timeout 300
    """
    client = get_client(ctx.obj.get("token"))
    start = time.time()

    try:
        with console.status(f"[bold]Waiting for task {task_id}...") as status:
            while True:
                elapsed = time.time() - start
                if elapsed > timeout:
                    print_error(f"Timeout after {timeout}s")
                    raise SystemExit(1)

                result = client.query_task(id=task_id)
                data = result.get("data", {})

                if isinstance(data, list) and data:
                    data = data[0]

                task_status = data.get("status", "unknown") if data else "unknown"
                status.update(f"[bold]Task {task_id}: {task_status} ({elapsed:.0f}s elapsed)")

                if task_status in ("completed", "complete"):
                    if output_json:
                        print_json(result)
                    else:
                        print_task_result(result)
                    return

                if task_status == "failed":
                    print_error(f"Task failed: {data.get('error', 'unknown error')}")
                    if output_json:
                        print_json(result)
                    raise SystemExit(1)

                time.sleep(interval)

    except SunoError as e:
        print_error(e.message)
        raise SystemExit(1) from e
