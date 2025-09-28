# API Route Implementation Instructions
The API follows RESTful principles and provides endpoints for managing builds.

## Documentation
- **Swagger UI**: Automatically generated API documentation available at `/docs`
- **OpenAPI**: API specification format used for documentation

## General Principles
- All endpoints are **read-only** (GET).
- Use **query parameters** for filtering, sorting, and selecting relevance strategies.
- No endpoints should modify the database.

## Routes to Implement

### 1. `/builds`
- **GET**: Returns the list of builds.

Supports query parameters:
  - `week` (e.g., specific week number; default: current week).
  - `id` (e.g., specific build ID).
  - `relevance` (e.g., `percentage`, `quartile`, `top_n`, `cumulative_coverage`; default: `percentage`).
  - `relevance_threshold` (e.g., minimum relevance score; default: dependent on `relevance`).
  - `sort_by` (e.g., `win_rate`, `usage`, `relevance`; default: `win_rate`).
  - `sort_order` (e.g., `asc`, `desc`; default: dependent on `sort_by`).
  - `pokemon` (e.g., comma-separated list of specific Pokémon names; default: all Pokémon).
  - `role` (e.g., comma-separated list of specific roles; default: all roles).
  - `item` (e.g., comma-separated list of specific item names; default: all items).
  - `ignore_pokemon` (e.g., comma-separated list of Pokémon to ignore; default: none).
  - `ignore_item` (e.g., comma-separated list of items to ignore; default: none).
  - `ignore_role` (e.g., comma-separated list of roles to ignore; default: none).

**Notes:**
- `id` cannot be used with any other filter except `week`.
- `pokemon`, `role`, and `item` can be used together to filter builds.
- Parameters pairs `ignore_pokemon`/`keep_pokemon`, `ignore_items`/`keep_items`, and `ignore_roles`/`keep_roles` cannot be used together to filter builds.

### 2. `/filters`
- **GET**: Returns the current filters applied to the builds.
- **GET `/filters/{filter_name}`**: Returns detailed information about a specific filter.

### 3. `/ids`
- **GET**: Returns a list of available build IDs.

### 4. `/weeks`
- **GET**: Returns a list of available weeks for which builds are stored.

### 5. `/relevance`
- **GET**: Returns a list of strategies to determine relevance.
- **GET `/relevance/{strategy}`**: Returns detailed information about a specific strategy.

### 6. `/sort_by`
- **GET**: Returns sorted builds or strategies by specified criteria (e.g., `win_rate`, `usage`, `relevance`).
- **GET `/sort_by/{criteria}`**: Returns detailed information about the specified sorting criteria.

### 7. `/pokemon`
- **GET**: Returns a list of available Pokémon.
- **GET `/pokemon/{name}`**: Returns detailed information about a specific Pokémon.

### 8. `/roles`
- **GET**: Returns a list of available roles.
- **GET `/roles/{role}`**: Returns detailed information about a specific role.

### 9. `/items`
- **GET**: Returns a list of available items.
- **GET `/items/{name}`**: Returns detailed information about a specific item.

### 10. `/logs`
- **GET**: Returns logs or summaries of analysis operations (if needed for frontend display).

---

**Implementation Notes:**
- All filtering, sorting, and relevance selection should be handled via query parameters.
- No POST, PUT, PATCH, or DELETE endpoints.
- Ensure endpoints are documented for frontend integration.

---

You can refer to these instructions during implementation to maintain consistency and clarity.
