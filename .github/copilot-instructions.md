# Copilot Instructions for SunoCli

## Sync from Docs

When working on a sync task (issue labeled `auto-sync`), follow these rules:

1. **Source of truth** — Clone/checkout `AceDataCloud/Docs` and read `openapi/suno.json` (the OpenAPI spec).
2. **Compare parameters** — CLI command parameters in `suno_cli/commands/` should match the corresponding OpenAPI endpoint's request body schema.
3. **Compare endpoints** — Each endpoint in the spec should have a corresponding CLI command. Add commands for new endpoints if needed.
4. **Update client** — If API endpoints change, update `suno_cli/core/client.py` accordingly.
5. **Update README** — Keep the feature list and usage examples in `README.md` current.
6. **Add tests** — For new commands or parameters, add test cases in `tests/`.
7. **PR title** — Use format: `sync: <description> [auto-sync]`
8. **No changes needed** — If everything is already in sync, close the issue with a comment.

## Project Structure

```
suno_cli/
  commands/    — Click CLI command modules
  core/
    client.py     — httpx HTTP client for api.acedata.cloud
    config.py     — Settings
    exceptions.py — Error classes
    output.py     — Output formatting
tests/           — pytest tests
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```
