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
