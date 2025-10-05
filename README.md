# Pokémon Unite Meta Analysis

This project provides tools and scripts for analyzing the meta of Pokémon Unite, focusing on builds, strategies, and statistical insights. It is organized as a
Python package and uses Poetry for dependency management.

---

**Database Schema Notice (2025-10):**

> **The project now uses a single `builds` table for all weeks, with a `week` column to distinguish data from different scrapes.**
> - All build data is stored in the same table.
> - The `week` column (e.g., `Y2025m09d28`) identifies the data collection date.
> - This enables easier queries, trend analysis, and API filtering.
> - If you are migrating from an older version, see the migration script in `src/repository/`.

---

## Getting Started

- Python 3.13+
- [Poetry](https://python-poetry.org/)

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd pokemon_unite_meta_analysis
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests to verify setup:
   ```bash
   poetry run pytest
   ```
4. Start the development server:
   ```bash
   poetry run uvicorn api.main:app --reload
   ```
5. Access the API documentation at `http://localhost:8000/docs`

## Database Structure

- All builds are stored in a single table: `builds`
- The `week` column (string, e.g. `Y2025m09d28`) identifies the read date
- Each build has a unique `id` (autoincrement)
- To filter by week, use the `week` query parameter in the API

## API Endpoints Overview

The API provides several categories of endpoints:

### Core Data Endpoints
- **GET `/builds`** - Retrieve builds with filtering, sorting, and relevance options
- **GET `/pokemon`** - List all available Pokémon
- **GET `/pokemon/{name}`** - Get all builds for a specific Pokémon
- **GET `/weeks`** - List all available weeks
- **GET `/ids`** - List all build IDs
- **GET `/roles`** - List all available roles
- **GET `/roles/{role}`** - Get all Pokémon names for a specific role
- **GET `/items`** - List all available held items
- **GET `/items/{name}`** - Get all Pokémon names that use a specific item

### Metadata & Discovery Endpoints
- **GET `/relevance`** - List available relevance strategies
- **GET `/relevance/{strategy}`** - Get details about a specific relevance strategy
- **GET `/sort_by`** - List available sort criteria
- **GET `/sort_by/{criteria}`** - Get details about a specific sort criteria
- **GET `/filters`** - List available filter strategies
- **GET `/filters/{filter_name}`** - Get details about a specific filter

### System Endpoints
- **GET `/`** - API root with metadata
- **GET `/health`** - Health check endpoint
- **GET `/logs`** - API logs summary
- **GET `/docs`** - Interactive Swagger UI documentation
- **GET `/redoc`** - Alternative ReDoc documentation

## API: /builds Endpoint

### Request (Query Parameters)

All query parameters are documented and validated using Pydantic. Example:

```
GET /builds?week=Y2025m09d28&pokemon=pikachu&role=attacker&sort_by=moveset_item_true_pick_rate&sort_order=desc&top_n=5
```

| Parameter           | Type      | Description                                      |
|---------------------|-----------|--------------------------------------------------|
| id                  | int       | Build ID for direct lookup                       |
| week                | str       | Week identifier (e.g. `Y2025m09d28`) for filtering builds |
| relevance           | str       | Relevance strategy (any, moveset_item_true_pr, position_of_popularity) |
| relevance_threshold | float     | Threshold for relevance filtering                |
| sort_by             | str       | Field to sort by                                 |
| sort_order          | str       | Sort order: asc or desc                          |
| pokemon             | str       | Filter by Pokémon name                           |
| role                | str       | Filter by role                                   |
| item                | str       | Filter by item                                   |
| ignore_pokemon      | str       | Exclude Pokémon name                             |
| ignore_item         | str       | Exclude item                                     |
| ignore_role         | str       | Exclude role                                     |
| top_n               | int       | Limit to top N results                           |

### Example Response

The response is a list of build objects, each matching the `BuildResponse` Pydantic model:

```json
[
   {
      "id": 1,
      "week": "Y2025m09d28",
      "pokemon": "Pikachu",
      "role": "Attacker",
      "pokemon_win_rate": 55.5,
      "pokemon_pick_rate": 42.0,
      "move_1": "Thunderbolt",
      "move_2": "Electro Ball",
      "moveset_win_rate": 60.0,
      "moveset_pick_rate": 50.0,
      "moveset_true_pick_rate": 21.0,
      "item": "Potion",
      "moveset_item_win_rate": 62.0,
      "moveset_item_pick_rate": 10.0,
      "moveset_item_true_pick_rate": 2.1
   },
   // ... more builds
]
```

See `/docs` for full OpenAPI schema and interactive documentation.

## API Usage Examples

### Discover Available Resources

```bash
# List all available Pokémon
curl http://localhost:8000/pokemon

# List all available weeks
curl http://localhost:8000/weeks

# List all build IDs
curl http://localhost:8000/ids

# List available filter strategies
curl http://localhost:8000/filters

# Get details about the 'pokemon' filter
curl http://localhost:8000/filters/pokemon

# List available relevance strategies
curl http://localhost:8000/relevance

# Get details about the 'percentage' relevance strategy
curl http://localhost:8000/relevance/percentage

# List available sort criteria
curl http://localhost:8000/sort_by

# Get details about the 'pokemon_win_rate' sort criteria
curl http://localhost:8000/sort_by/pokemon_win_rate
```

### Query Builds with Filters

```bash
# Get all builds for Pikachu
curl "http://localhost:8000/builds?pokemon=pikachu"

# Get builds for multiple Pokémon
curl "http://localhost:8000/builds?pokemon=pikachu,charizard"

# Get builds filtered by role
curl "http://localhost:8000/builds?role=attacker"

# Get builds excluding specific Pokémon
curl "http://localhost:8000/builds?ignore_pokemon=pikachu"

# Get builds for a specific week
curl "http://localhost:8000/builds?week=Y2025m09d28"

# Combine multiple filters
curl "http://localhost:8000/builds?role=attacker&item=potion&sort_by=pokemon_win_rate&sort_order=desc&top_n=10"
```

### Use Relevance Strategies

```bash
# Get builds with pick rate >= 5%
curl "http://localhost:8000/builds?relevance=percentage&relevance_threshold=5.0"

# Get top 10 builds by pick rate
curl "http://localhost:8000/builds?relevance=top_n&relevance_threshold=10"

# Get builds until cumulative pick rate reaches 50%
curl "http://localhost:8000/builds?relevance=cumulative_coverage&relevance_threshold=50"

# Get builds from top quartile (top 25%)
curl "http://localhost:8000/builds?relevance=quartile&relevance_threshold=1"
```

### Check System Status

```bash
# Health check
curl http://localhost:8000/health

# View logs summary
curl http://localhost:8000/logs

# Get API metadata
curl http://localhost:8000/
```

## Testing

Run all tests:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=src --cov-report=html --cov-report=xml
```

Run specific test suites:
```bash
# Unit tests only
poetry run pytest tests/unit/

# Integration tests only
poetry run pytest tests/integration/

# Specific test file
poetry run pytest tests/integration/test_meta_endpoints.py -v
```

## Development

### Linting
```bash
poetry run ruff check .
```

### Running the API Server
```bash
# Development mode with auto-reload
poetry run uvicorn api.main:app --reload

# Production mode
poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000
```
