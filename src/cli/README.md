# Pokemon Unite Meta Analysis CLI

CLI client for querying Pokemon Unite meta analysis data.

## Installation

```bash
poetry install
```

## Usage

The CLI can be used in three ways:

### 1. As an installed script (recommended)
```bash
poetry run pkmn-unite-cli <command> [options]
```

### 2. As a Python module
```bash
poetry run python -m cli <command> [options]
```

### 3. Direct execution
```bash
poetry run python src/cli/main.py <command> [options]
```

## Available Commands

### Health Check
```bash
poetry run pkmn-unite-cli health
```

### Get Builds
```bash
poetry run pkmn-unite-cli get-builds [OPTIONS]
```

#### Options:
- `--pokemon TEXT` - Filter by Pokémon name
- `--role TEXT` - Filter by role (Support, Attacker, Speedster, Defender, All-Rounder)
- `--week TEXT` - Filter by week (format: Y2025m10d05)
- `--item TEXT` - Filter by held item name
- `--relevance CHOICE` - Relevance strategy (any, percentage, top_n, cumulative_coverage, quartile)
- `--relevance-threshold FLOAT` - Threshold for relevance strategy
- `--sort-by FIELD` - Sort builds by field
- `--include COLUMN [COLUMN ...]` - Columns to include in output
- `--exclude COLUMN [COLUMN ...]` - Columns to exclude from output

## Examples

```bash
# Get top 10 builds by pick rate
poetry run pkmn-unite-cli get-builds --week Y2025m10d05 --relevance top_n --relevance-threshold 10

# Get Support builds sorted by win rate
poetry run pkmn-unite-cli get-builds --role Support --sort-by moveset_item_win_rate

# Get builds with specific columns
poetry run pkmn-unite-cli get-builds --week Y2025m10d05 --include pokemon role moveset_item_win_rate

# Get builds excluding certain columns
poetry run pkmn-unite-cli get-builds --week Y2025m10d05 --exclude id week rank

# Combined filters with pipe to head
poetry run pkmn-unite-cli get-builds --week Y2025m10d05 --relevance percentage --relevance-threshold 5.0 --sort-by moveset_item_win_rate | head -20
```

## Features

- ✅ Colorized output by role
- ✅ Pandas DataFrame formatting
- ✅ Support for all API filters and parameters
- ✅ Relevance strategies (any, percentage, top_n, cumulative_coverage, quartile)
- ✅ Sorting by any field
- ✅ Column selection (include/exclude)
- ✅ Unix pipe support
- ✅ Clean logging (suppressed httpx INFO logs)

## Development

The CLI is located in `src/cli/`:
- `main.py` - Main CLI logic
- `__init__.py` - Module exports
- `__main__.py` - Module entry point
