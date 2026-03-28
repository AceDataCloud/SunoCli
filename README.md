# Suno CLI

[![PyPI version](https://img.shields.io/pypi/v/suno-cli.svg)](https://pypi.org/project/suno-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/suno-cli.svg)](https://pypi.org/project/suno-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/SunoCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/SunoCli/actions/workflows/ci.yaml)

A command-line tool for AI music generation using [Suno](https://suno.ai/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI music, lyrics, and manage audio projects directly from your terminal — no MCP client required.

## Features

- **Music Generation** — Generate from prompts, custom lyrics, extend, cover, remaster, concat
- **Lyrics** — Generate lyrics, mashup, optimize style descriptions
- **Media Conversion** — Get MP4, WAV, MIDI, timing, extract vocals
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping
- **File Input** — Read lyrics from files with `@filename` syntax

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to [Suno Audios API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9)
3. Click "Acquire" to get your token

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

### Utilities

| Command | Description |
|---------|-------------|
| `suno persona <audio_id>` | Create a saved voice style |
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
--model TEXT    Suno model version (default: chirp-v4-5)
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
| `chirp-v5-5` | V5.5 | 8 min | Latest, best quality |
| `chirp-v5` | V5 | 8 min | High quality |
| `chirp-v4-5-plus` | V4.5+ | 8 min | Enhanced quality |
| `chirp-v4-5` | V4.5 | 4 min | Vocal gender control (default) |
| `chirp-v4` | V4 | 150s | Stable |
| `chirp-v3-5` | V3.5 | 120s | Fast |
| `chirp-v3-0` | V3 | 120s | Legacy |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SUNO_DEFAULT_MODEL` | Default model | `chirp-v4-5` |
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

This tool wraps the [AceDataCloud Suno API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9):

- [Suno Audios API](https://platform.acedata.cloud/documents/4da95d9d-7722-4a72-857d-bf6be86036e9) — Music generation
- [Suno Lyrics API](https://platform.acedata.cloud/documents/514d82dc-f7ab-4638-9f21-8b9275916b08) — Lyrics generation
- [Suno Tasks API](https://platform.acedata.cloud/documents/b0dd9823-0e01-4c75-af83-5a6e2e05bfed) — Task queries
- [Suno Persona API](https://platform.acedata.cloud/documents/78bb6c62-6ce0-490f-a7df-e89d80ec0583) — Persona management

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

- [AceDataCloud Platform](https://platform.acedata.cloud/)
- [MCP Suno](https://github.com/AceDataCloud/SunoMCP) — MCP server version
- [Suno Official](https://suno.ai/)

---

Made with ❤️ by [AceDataCloud](https://platform.acedata.cloud/)
