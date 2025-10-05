# Quick Reference: API Endpoints

## Base URL
```
http://localhost:8000
```

## Core Data
```bash
GET /builds              # Get builds (with filters/sorting)
GET /pokemon             # List all Pokémon
GET /pokemon/{name}      # Get builds for Pokémon
GET /weeks               # List available weeks
GET /ids                 # List all build IDs
```

## Metadata
```bash
GET /relevance                # List relevance strategies
GET /relevance/{strategy}     # Relevance strategy details
GET /sort_by                  # List sort criteria
GET /sort_by/{criteria}       # Sort criteria details
GET /filters                  # List filter strategies
GET /filters/{filter_name}    # Filter details
```

## System
```bash
GET /                    # API root
GET /health              # Health check
GET /logs                # Logs summary
GET /docs                # Swagger UI
GET /redoc               # ReDoc UI
```

## Quick Examples

### Get top builds for Pikachu
```bash
curl "http://localhost:8000/builds?pokemon=pikachu&sort_by=moveset_item_win_rate&sort_order=desc&top_n=5"
```

### Get builds with >5% pick rate
```bash
curl "http://localhost:8000/builds?relevance=percentage&relevance_threshold=5.0"
```

### Get attackers excluding common picks
```bash
curl "http://localhost:8000/builds?role=attacker&ignore_pokemon=pikachu,charizard"
```

### Discover available filters
```bash
curl http://localhost:8000/filters
```

### Check what you can sort by
```bash
curl http://localhost:8000/sort_by
```

## Common Query Parameters for /builds

| Parameter | Type | Example |
|-----------|------|---------|
| `week` | string | `Y2025m09d28` |
| `pokemon` | string | `pikachu,charizard` |
| `role` | string | `attacker,speedster` |
| `item` | string | `potion,ejectbutton` |
| `ignore_pokemon` | string | `pikachu` |
| `ignore_role` | string | `defender` |
| `ignore_item` | string | `potion` |
| `relevance` | string | `percentage`, `top_n`, `quartile` |
| `relevance_threshold` | float | `5.0`, `10`, `1` |
| `sort_by` | string | `pokemon_win_rate` |
| `sort_order` | string | `asc`, `desc` |
| `top_n` | integer | `10`, `20` |

## Relevance Strategies

| Strategy | Threshold | Description |
|----------|-----------|-------------|
| `any` | ignored | All builds |
| `percentage` | 0-100 | Pick rate >= threshold % |
| `top_n` | integer | Top N builds |
| `cumulative_coverage` | 0-100 | Until cumulative % reached |
| `quartile` | 1-4 | Top N quartiles |

## Sort Criteria

- `pokemon` - Pokémon name (asc)
- `role` - Role name (asc)
- `pokemon_win_rate` - Pokémon win rate (desc)
- `pokemon_pick_rate` - Pokémon pick rate (desc)
- `moveset_win_rate` - Moveset win rate (desc)
- `moveset_pick_rate` - Moveset pick rate (desc)
- `moveset_true_pick_rate` - Moveset true pick rate (desc)
- `item` - Item name (asc)
- `moveset_item_win_rate` - Moveset+item win rate (desc)
- `moveset_item_pick_rate` - Moveset+item pick rate (desc)
- `moveset_item_true_pick_rate` - Moveset+item true pick rate (desc)

## Filter Types

### Include Filters
- `pokemon` - Include specific Pokémon
- `role` - Include specific roles
- `item` - Include specific items

### Exclude Filters
- `ignore_pokemon` - Exclude specific Pokémon
- `ignore_role` - Exclude specific roles
- `ignore_item` - Exclude specific items

## Testing

```bash
# All tests
poetry run pytest

# Integration only
poetry run pytest tests/integration/

# Specific test file
poetry run pytest tests/integration/test_meta_endpoints.py -v

# With coverage
poetry run pytest --cov=src --cov-report=html
```

## Development

```bash
# Start dev server
poetry run uvicorn api.main:app --reload

# Lint code
poetry run ruff check .

# Access docs
open http://localhost:8000/docs
```
