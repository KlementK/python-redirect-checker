# python-redirect-checker

IT JUST WORKS.

## Prerequisites

- Python >= 3.13
- uv

## Install

```bash
uv venv
uv sync
```

## Usage

1. Add your redirects to `data/urls.csv`:

```csv
INITIAL_URL,EXPECTED_REDIRECT
https://example.com/old,https://example.com/new
```

2. Run:

```bash
python -m src.cli
```

## Dev

```bash
uv sync
ruff check .
mypy src/
```

## Features

- 3 concurrent requests
- 0.75s delay between requests
- Protocol-agnostic comparison (http/https ignored)
- 30s timeout per request
