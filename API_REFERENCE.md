# Complete API Reference

## Overview

The Pokémon Unite Meta Analysis API provides comprehensive endpoints for querying and analyzing Pokémon Unite build data. All endpoints are read-only (GET) and return JSON responses.

**Base URL:** `http://localhost:8000` (development)  
**Documentation:** `/docs` (Swagger UI) or `/redoc` (ReDoc)

---

## Endpoint Categories

### 📊 Core Data Endpoints

#### GET `/builds`
Retrieve builds with advanced filtering, sorting, and relevance options.

**Query Parameters:**
- `week` (string) - Filter by week identifier (e.g., `Y2025m09d28`)
- `id` (integer) - Direct lookup by build ID
- `relevance` (string) - Relevance strategy: `any`, `percentage`, `top_n`, `cumulative_coverage`, `quartile`
- `relevance_threshold` (float) - Threshold for relevance filtering
- `sort_by` (string) - Sort field (see `/sort_by` for options)
- `sort_order` (string) - `asc` or `desc`
- `pokemon` (string) - Include Pokémon (comma-separated)
- `role` (string) - Include roles (comma-separated)
- `item` (string) - Include items (comma-separated)
- `ignore_pokemon` (string) - Exclude Pokémon (comma-separated)
- `ignore_role` (string) - Exclude roles (comma-separated)
- `ignore_item` (string) - Exclude items (comma-separated)
- `top_n` (integer) - Limit results to top N

**Response:** Array of `BuildResponse` objects

**Example:**
```bash
GET /builds?pokemon=pikachu&role=attacker&sort_by=pokemon_win_rate&sort_order=desc&top_n=10
```

#### GET `/pokemon`
List all available Pokémon names.

**Response:** Array of strings (Pokémon names, sorted alphabetically)

**Example:**
```bash
GET /pokemon
# Response: ["Charizard", "Greninja", "Pikachu", ...]
```

#### GET `/pokemon/{name}`
Get all builds for a specific Pokémon.

**Path Parameters:**
- `name` (string) - Pokémon name (case-insensitive)

**Response:** Array of `BuildResponse` objects

**Example:**
```bash
GET /pokemon/pikachu
```

#### GET `/weeks`
List all available weeks.

**Response:** Array of strings (week identifiers, sorted descending)

**Example:**
```bash
GET /weeks
# Response: ["Y2025m10d03", "Y2025m09d28", ...]
```

#### GET `/ids`
List all build IDs.

**Response:** Array of integers (build IDs)

**Example:**
```bash
GET /ids
# Response: [1, 2, 3, ..., 7854]
```

---

### 🔍 Metadata & Discovery Endpoints

#### GET `/relevance`
List available relevance strategies.

**Response:** Array of strategy objects with `name` and `description`

**Example:**
```bash
GET /relevance
```

**Response:**
```json
[
  {
    "name": "any",
    "description": "Returns all builds without filtering."
  },
  {
    "name": "percentage",
    "description": "Filters builds with moveset_item_true_pick_rate >= threshold (0-100)."
  },
  ...
]
```

#### GET `/relevance/{strategy}`
Get detailed information about a specific relevance strategy.

**Path Parameters:**
- `strategy` (string) - Strategy name: `any`, `percentage`, `top_n`, `cumulative_coverage`, `quartile`

**Response:** Strategy details object

**Example:**
```bash
GET /relevance/percentage
```

**Response:**
```json
{
  "name": "percentage",
  "description": "Filters builds with moveset_item_true_pick_rate >= threshold.",
  "threshold_type": "percentage",
  "threshold_description": "Threshold should be a value between 0 and 100..."
}
```

#### GET `/sort_by`
List available sort criteria.

**Response:** Array of criteria objects with `name`, `description`, and `default_order`

**Example:**
```bash
GET /sort_by
```

**Response:**
```json
[
  {
    "name": "pokemon",
    "description": "Sort by Pokémon name (alphabetically).",
    "default_order": "asc"
  },
  {
    "name": "pokemon_win_rate",
    "description": "Sort by Pokémon win rate.",
    "default_order": "desc"
  },
  ...
]
```

#### GET `/sort_by/{criteria}`
Get detailed information about a specific sort criteria.

**Path Parameters:**
- `criteria` (string) - Criteria name (e.g., `pokemon`, `pokemon_win_rate`, `moveset_item_true_pick_rate`)

**Response:** Criteria details object

**Example:**
```bash
GET /sort_by/pokemon_win_rate
```

**Response:**
```json
{
  "name": "pokemon_win_rate",
  "description": "Sort builds by Pokémon win rate (percentage).",
  "field_type": "float",
  "default_order": "desc"
}
```

#### GET `/filters`
List available filter strategies.

**Response:** Array of filter objects with `name`, `description`, `type`, and `example`

**Example:**
```bash
GET /filters
```

**Response:**
```json
[
  {
    "name": "pokemon",
    "description": "Filter builds by Pokémon name(s). Accepts comma-separated list.",
    "type": "include",
    "example": "pikachu,charizard"
  },
  {
    "name": "ignore_pokemon",
    "description": "Exclude builds with specific Pokémon name(s). Accepts comma-separated list.",
    "type": "exclude",
    "example": "pikachu,charizard"
  },
  ...
]
```

#### GET `/filters/{filter_name}`
Get detailed information about a specific filter.

**Path Parameters:**
- `filter_name` (string) - Filter name: `pokemon`, `role`, `item`, `ignore_pokemon`, `ignore_role`, `ignore_item`

**Response:** Filter details object

**Example:**
```bash
GET /filters/pokemon
```

**Response:**
```json
{
  "name": "pokemon",
  "description": "Filter builds by Pokémon name(s).",
  "type": "include",
  "parameter": "pokemon",
  "value_format": "comma-separated string",
  "example": "pikachu,charizard,greninja",
  "usage": "Use this filter to include only builds for specific Pokémon..."
}
```

---

### ⚙️ System Endpoints

#### GET `/`
API root with metadata.

**Response:** API information object

**Example:**
```bash
GET /
```

**Response:**
```json
{
  "message": "Pokemon Unite Meta Analysis API is running.",
  "debug": true,
  "host": "localhost",
  "port": 8000
}
```

#### GET `/health`
Health check endpoint.

**Response:** Health status object

**Example:**
```bash
GET /health
# Response: {"status": "ok"}
```

#### GET `/logs`
API logs summary.

**Response:** Logs information object with available log files

**Example:**
```bash
GET /logs
```

**Response:**
```json
{
  "available_logs": [
    {
      "name": "log_api.log",
      "path": "/path/to/log_api.log",
      "size_bytes": 12345,
      "last_entries": ["...", "..."]
    }
  ],
  "description": "API logging information",
  "note": "Log files are stored in the project root directory"
}
```

---

## Data Models

### BuildResponse

The main data model for build information:

```json
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
}
```

**Fields:**
- `id` (integer) - Unique build identifier
- `week` (string) - Week identifier
- `pokemon` (string) - Pokémon name
- `role` (string) - Pokémon role
- `pokemon_win_rate` (float) - Overall Pokémon win rate %
- `pokemon_pick_rate` (float) - Overall Pokémon pick rate %
- `move_1` (string) - First move/ability
- `move_2` (string) - Second move/ability
- `moveset_win_rate` (float) - Moveset-specific win rate %
- `moveset_pick_rate` (float) - Moveset-specific pick rate %
- `moveset_true_pick_rate` (float) - True pick rate for this moveset %
- `item` (string) - Battle item
- `moveset_item_win_rate` (float) - Win rate with this moveset+item %
- `moveset_item_pick_rate` (float) - Pick rate with this moveset+item %
- `moveset_item_true_pick_rate` (float) - True pick rate for moveset+item %

---

## Common Use Cases

### 1. Find Top Builds for a Pokémon
```bash
curl "http://localhost:8000/builds?pokemon=pikachu&sort_by=moveset_item_win_rate&sort_order=desc&top_n=5"
```

### 2. Analyze Meta Trends by Week
```bash
# Get available weeks
curl http://localhost:8000/weeks

# Get builds for a specific week
curl "http://localhost:8000/builds?week=Y2025m09d28&relevance=percentage&relevance_threshold=5.0"
```

### 3. Compare Roles
```bash
# Get top attackers
curl "http://localhost:8000/builds?role=attacker&sort_by=pokemon_win_rate&sort_order=desc&top_n=10"

# Get top defenders
curl "http://localhost:8000/builds?role=defender&sort_by=pokemon_win_rate&sort_order=desc&top_n=10"
```

### 4. Find Alternative Builds
```bash
# Get builds excluding the most common Pokémon
curl "http://localhost:8000/builds?ignore_pokemon=pikachu,charizard,greninja&relevance=top_n&relevance_threshold=20"
```

### 5. Discover API Capabilities
```bash
# What filters are available?
curl http://localhost:8000/filters

# What relevance strategies exist?
curl http://localhost:8000/relevance

# How do I sort builds?
curl http://localhost:8000/sort_by
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- **200 OK** - Successful request
- **404 Not Found** - Resource not found (invalid strategy/criteria/filter name)
- **400 Bad Request** - Invalid query parameters
- **500 Internal Server Error** - Server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. This is a development/local API.

---

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

---

## Interactive Documentation

- **Swagger UI:** `http://localhost:8000/docs`
  - Interactive API explorer
  - Try out endpoints directly in browser
  - View request/response schemas

- **ReDoc:** `http://localhost:8000/redoc`
  - Alternative documentation format
  - Clean, organized view
  - Better for reading/reference

---

## Complete Endpoint List

Total: 14 public endpoints

1. `GET /` - API root
2. `GET /health` - Health check
3. `GET /builds` - Get builds with filters
4. `GET /pokemon` - List Pokémon
5. `GET /pokemon/{name}` - Get Pokémon builds
6. `GET /weeks` - List weeks
7. `GET /ids` - List build IDs
8. `GET /relevance` - List relevance strategies
9. `GET /relevance/{strategy}` - Relevance strategy details
10. `GET /sort_by` - List sort criteria
11. `GET /sort_by/{criteria}` - Sort criteria details
12. `GET /filters` - List filters
13. `GET /filters/{filter_name}` - Filter details
14. `GET /logs` - Logs summary
