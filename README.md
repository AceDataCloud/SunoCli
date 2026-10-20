# Suno by Ace Data Cloud — CLI

## Install the Ace integration

This integration is maintained by **Ace Data Cloud** and uses your Ace API key. It is not an official client published by the model owner. Check the [PyPI package](https://pypi.org/project/suno-cli/) and its AceDataCloud repository before installing.

```bash
python -m pip install suno-cli
suno --help
suno models
```

The commands above show local help/reference information and do not submit a generation. Then follow **Get API Token** below: register/sign in, initialize General application if needed, create/copy an application key, and store it in the terminal's `ACEDATACLOUD_API_TOKEN` environment variable. Do not use a platform management token.

Generation follows your account's current service access, balance and pricing. Save the returned task ID and query that **same ID**; do not repeat generation while a task is pending.

```text
suno task <task-id>
suno wait <task-id> --interval 5
```

A successful command or running preview does not prove a completed media result. Check the task's terminal outcome and returned media link. [中文首次使用指南](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES_zh-CN.md) · [Service-name package directory](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES.md)


[![PyPI version](https://img.shields.io/pypi/v/suno-cli.svg)](https://pypi.org/project/suno-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/suno-cli.svg)](https://pypi.org/project/suno-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/SunoCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/SunoCli/actions/workflows/ci.yaml)

A command-line tool for AI music generation using [Suno](https://suno.ai/) through the [AceDataCloud API](https://platform.acedata.cloud/?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_platform).

Generate AI music, lyrics, and manage audio projects directly from your terminal — no MCP client required.

## Features

- **Music Generation** — Generate from prompts, custom lyrics, extend, cover, remaster, concat
- **Lyrics** — Generate lyrics, mashup, optimize style descriptions
- **Media Conversion** — Get MP4, WAV, MIDI, timing, extract vocals
- **Task Management** — Query tasks, batch query, wait with polling
- **Custom Models** — Train, inspect, generate with, and archive custom music models
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping
- **File Input** — Read lyrics from files with `@filename` syntax

## Quick Start

### 1. Get API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

### 2. Install

```bash
# Install with pip
pip install suno-cli

# Or with uv (recommended)
uv pip install suno-cli

# Or from source
git clone https://github.com/AceDataCloud/SunoCli.git
cd SunoCli
pip install -e .
```

### 3. Configure

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Or use .env file
cp .env.example .env
# Edit .env with your token
```

### 4. Use

```bash
# Generate music from a prompt
suno generate "A happy birthday song with acoustic guitar"

# Generate with custom lyrics
suno custom -l "[Verse]\nHello world\n[Chorus]\nLa la la" -t "Hello" -s "pop, upbeat"

# Read lyrics from a file
suno custom -l @lyrics.txt -t "My Song" -s "rock, powerful"

# Generate lyrics
suno lyrics "A love song about the ocean at sunset"

# Check task status
suno task <task-id>

# Wait for completion with polling
suno wait <task-id> --interval 5

# Get MP4 video
suno mp4 <audio-id>

# List available models
suno models
```

## Commands

### Music Generation

| Command | Description |
|---------|-------------|
| `suno generate <prompt>` | Generate music from a text prompt (Inspiration Mode) |
| `suno custom` | Generate with custom lyrics, title, and style |
| `suno extend <audio_id>` | Extend an existing song from a timestamp |
| `suno cover <audio_id>` | Create a cover/remix version |
| `suno remaster <audio_id>` | Remaster a song to improve quality |
| `suno concat <audio_id>` | Merge extended segments into complete audio |
| `suno generate-persona <audio_id>` | Generate music using a saved persona |
| `suno generate-persona-vox <audio_id>` | Generate music using a persona's vocal style |
| `suno stems <audio_id>` | Separate a song into vocals + instrumental |
| `suno all-stems <audio_id>` | Separate a song into all individual stems |
| `suno replace-section <audio_id>` | Replace a time range with new content |
| `suno upload-extend <audio_id>` | Extend uploaded audio with AI continuation |
| `suno upload-cover <audio_id>` | Create a cover of uploaded audio |
| `suno mashup <id1> <id2>...` | Blend multiple songs into a mashup |
| `suno underpainting <audio_id>` | Add AI accompaniment to uploaded audio |
| `suno overpainting <audio_id>` | Add AI vocals to uploaded audio |
| `suno samples <audio_id>` | Add AI samples to uploaded audio |
| `suno inspo <audio_id>` | Generate a new song inspired by an existing audio |

### Audio ID processing failures

An `audio_id` identifies reference music for operations such as cover, extend and stem separation. A downloadable audio file does not guarantee that its ID remains available for further processing.

| HTTP status | Error code | Meaning |
|-------------|------------|---------|
| 500 | `suno_processing_unavailable` | Music processing is unavailable. |
| 500 | `suno_model_unavailable` | The selected model is unavailable for this operation. |
| 500 | `suno_processing_failed` | Music processing returned no audio. |

If one of these errors occurs, retain the original `task_id` (when available) and the error's `trace_id`, and contact support. The CLI displays the HTTP error body and exits nonzero; it does not automatically resubmit the operation. Do not treat a working download link as evidence that another processing attempt will succeed.

### Lyrics

| Command | Description |
|---------|-------------|
| `suno lyrics <prompt>` | Generate song lyrics from a prompt |
| `suno mashup-lyrics` | Generate mashup lyrics from two sources |
| `suno optimize-style <prompt>` | Optimize a style description |

### Media Conversion

| Command | Description |
|---------|-------------|
| `suno mp4 <audio_id>` | Get MP4 video version |
| `suno wav <audio_id>` | Get lossless WAV format |
| `suno midi <audio_id>` | Get MIDI data |
| `suno timing <audio_id>` | Get timing/subtitle data |
| `suno vocals <audio_id>` | Extract vocal track |

### Task Management

| Command | Description |
|---------|-------------|
| `suno task <task_id>` | Query a single task status |
| `suno tasks <id1> <id2>...` | Query multiple tasks at once |
| `suno wait <task_id>` | Wait for task completion with polling |

### Custom Models

| Command | Description |
|---------|-------------|
| `suno custom-model-create` | Train a model from 6–24 authorized audio URLs |
| `suno custom-model <model_id>` | Retrieve a custom model |
| `suno custom-models` | List custom models for the current application |
| `suno custom-model-generate <model_id>` | Generate a song with a ready custom model |
| `suno custom-model-delete <model_id>` | Archive a custom model |

### Utilities

| Command | Description |
|---------|-------------|
| `suno persona <audio_id>` | Create a saved voice style |
| `suno personas` | List saved voice styles |
| `suno persona-delete <persona_id>` | Delete a saved voice style |
| `suno voice <audio_url>` | Create a voice style from an external voice recording |
| `suno upload <audio_url>` | Upload external audio for processing |
| `suno models` | List available Suno models |
| `suno actions` | List available API actions |
| `suno lyric-format` | Show lyrics formatting guide |
| `suno config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--model TEXT    Suno model version (default: chirp-v6)
```

The `generate` and `custom` commands also support:

```
--duration INT  Target track length in seconds
```

`--negative-style` maps to the API's `negative_tags` field and takes effect only in custom mode (`suno custom`, which sends `custom: true`). There is currently no fixed character limit for this field, but overly long input may still fail; keep it concise. The option on `suno generate` is preserved, but that command does not enable custom mode.

```bash
suno custom -l @lyrics.txt -t "My Song" -s "pop, upbeat" --negative-style "metal, harsh vocals"
```

## Scripting & Piping

The `--json` flag outputs machine-readable JSON suitable for piping:

```bash
# Generate and extract task ID
TASK_ID=$(suno generate "rock song" --json | jq -r '.task_id')

# Wait for completion and get audio URL
suno wait $TASK_ID --json | jq -r '.data[0].audio_url'

# Batch generate from a file of prompts
while IFS= read -r prompt; do
  suno generate "$prompt" --json >> results.jsonl
done < prompts.txt
```

## Available Models

| Model | Version | Max Duration | Notes |
|-------|---------|-------------|-------|
| `chirp-v6` | V6 | — | Latest, best quality (default) |
| `chirp-v6-wild` | V6 Wild | — | V6 wild variant |
| `chirp-v6-mini` | V6 Mini | — | V6 compact variant |
| `chirp-v5-5` | V5.5 | 8 min | High quality |
| `chirp-v5` | V5 | 8 min | High quality |
| `chirp-v4-5-plus` | V4.5+ | 8 min | Enhanced quality |
| `chirp-v4-5` | V4.5 | 4 min | Vocal gender control |
| `chirp-v4` | V4 | 150s | Stable |
| `chirp-v3-5` | V3.5 | 120s | Fast |
| `chirp-v3-0` | V3 | 120s | Legacy |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SUNO_DEFAULT_MODEL` | Default model | `chirp-v6` |
| `SUNO_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/SunoCli.git
cd SunoCli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=suno_cli

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy suno_cli
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/suno-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/suno-cli generate "A happy song"

# Or use docker-compose
docker compose run --rm suno-cli generate "A happy song"
```

## Project Structure

```
SunoCli/
├── suno_cli/               # Main package
│   ├── __init__.py
│   ├── __main__.py        # python -m suno_cli entry point
│   ├── main.py            # CLI entry point
│   ├── core/              # Core modules
│   │   ├── client.py      # HTTP client for Suno API
│   │   ├── config.py      # Configuration management
│   │   ├── exceptions.py  # Custom exceptions
│   │   └── output.py      # Rich terminal formatting
│   └── commands/          # CLI command groups
│       ├── generate.py    # Music generation commands (12 commands)
│       ├── lyrics.py      # Lyrics & style commands
│       ├── media.py       # Media conversion commands
│       ├── persona.py     # Persona & upload commands
│       ├── task.py        # Task management commands
│       └── info.py        # Info & utility commands
├── tests/                  # Test suite (80+ tests)
├── .github/workflows/      # CI/CD (lint, test, publish to PyPI)
├── Dockerfile             # Container image
├── deploy/                # Kubernetes deployment configs
├── .env.example           # Environment template
├── pyproject.toml         # Project configuration
└── README.md
```

## Suno CLI vs MCP Suno

| Feature | Suno CLI | MCP Suno |
|---------|----------|----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install suno-cli` | `pip install mcp-suno` |

Both tools use the same AceDataCloud API and share the same API token.

## API Reference

This tool wraps the [AceDataCloud Suno API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_documents_4da95d9d_7722_4a72_857d_bf6be86036e9):

- [Suno Audios API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_documents_4da95d9d_7722_4a72_857d_bf6be86036e9) — Music generation
- [Suno Lyrics API](https://platform.acedata.cloud/documents/514d82dc-f7ab-4638-9f21-8b9275916b08?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_documents_514d82dc_f7ab_4638_9f21_8b9275916b08) — Lyrics generation
- [Suno Tasks API](https://platform.acedata.cloud/documents/b0dd9823-0e01-4c75-af83-5a6e2e05bfed?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_documents_b0dd9823_0e01_4c75_af83_5a6e2e05bfed) — Task queries
- [Suno Persona API](https://platform.acedata.cloud/documents/78bb6c62-6ce0-490f-a7df-e89d80ec0583?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_documents_78bb6c62_6ce0_490f_a7df_e89d80ec0583) — Persona management

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud/?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_platform)
- [MCP Suno](https://github.com/AceDataCloud/SunoMCP) — MCP server version
- [Suno Official](https://suno.ai/)

---

Made with ❤️ by [AceDataCloud](https://platform.acedata.cloud/?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_cli_readme_platform)
