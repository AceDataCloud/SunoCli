# SunoCli

Command-line tool for Suno AI music generation via AceDataCloud API.

## Project Structure

```
suno_cli/
  __init__.py    — Package init
  cli.py         — Main Click CLI group
  commands/      — Click command modules (generate, lyrics, media, task, etc.)
  models.py      — Pydantic models for API responses
  client.py      — HTTP client for AceDataCloud API
  config.py      — Settings (API token, base URL)
  utils.py       — Output formatting, Rich tables
tests/           — pytest tests
```

## Sync from Docs

When working on an auto-sync issue (labeled `auto-sync`), follow these rules:

1. **Compare commands** — Each API endpoint in the Docs OpenAPI spec should have a corresponding CLI command. Add new commands for new endpoints.
2. **Compare parameters** — CLI flags/options should match API request parameters. Add `--new-param` flags for new API parameters.
3. **Model choices** — Update model choice lists (Click's `type=click.Choice([...])`) to match the OpenAPI spec's model enum.
4. **Help text** — Update command help text to match API documentation.
5. **README** — Keep the command reference and model table current.
6. **Tests** — Add test cases for new commands.
7. **PR title** — Use format: `sync: <description> [auto-sync]`

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```
