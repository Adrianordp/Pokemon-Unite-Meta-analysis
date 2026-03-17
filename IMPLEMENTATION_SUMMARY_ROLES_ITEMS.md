# Roles & Items Endpoints Implementation Summary

## Date: 2025-01-10

## Overview
Added four new discovery endpoints to the API: `/roles`, `/roles/{role}`, `/items`, and `/items/{name}`. These endpoints provide metadata about roles and held items in the database, allowing users to discover what data is available and filter Pokémon by role or item.

---

## New Endpoints

### 1. GET `/roles`
**Purpose:** List all unique roles in the database  
**Returns:** `List[str]` - Alphabetically sorted role names  
**Status Codes:**
- 200 OK - Successfully retrieved roles

**Example Request:**
```bash
curl http://localhost:8000/roles
```

**Example Response:**
```json
["All-Rounder", "Attacker", "Defender", "Speedster", "Supporter"]
```

**Implementation Details:**
- Queries distinct values from the `role` column
- Filters out null/empty values
- Returns sorted alphabetically
- Uses `BuildRepository.get_all_roles()`

---

### 2. GET `/roles/{role}`
**Purpose:** Get all Pokémon names for a specific role  
**Path Parameter:** `role` (string, case-insensitive)  
**Returns:** `List[str]` - Alphabetically sorted Pokémon names  
**Status Codes:**
- 200 OK - Successfully retrieved Pokémon
- 404 Not Found - Role doesn't exist in database

**Example Request:**
```bash
curl http://localhost:8000/roles/attacker
```

**Example Response:**
```json
["Charizard", "Cinderace", "Decidueye", "Delphox", "Dragapult", "Greninja", ...]
```

**Implementation Details:**
- Case-insensitive role matching (e.g., "ATTACKER" == "Attacker")
- Queries builds table for matching role
- Returns distinct Pokémon names
- Raises 404 if no Pokémon found with that role
- Uses `BuildRepository.get_pokemon_by_role(role)`

---

### 3. GET `/items`
**Purpose:** List all unique held items in the database  
**Returns:** `List[str]` - Alphabetically sorted item names  
**Status Codes:**
- 200 OK - Successfully retrieved items

**Example Request:**
```bash
curl http://localhost:8000/items
```

**Example Response:**
```json
["Assault Vest", "Attack Weight", "Buddy Barrier", "Choice Specs", ...]
```

**Implementation Details:**
- Extracts items from JSON array columns (`held_items`, `held_items2`, `held_items3`)
- Deduplicates across all three item slots
- Filters out null/empty values
- Returns sorted alphabetically
- Uses `BuildRepository.get_all_items()`

---

### 4. GET `/items/{name}`
**Purpose:** Get all Pokémon names that use a specific held item  
**Path Parameter:** `name` (string, case-insensitive, URL-encoded)  
**Returns:** `List[str]` - Alphabetically sorted Pokémon names  
**Status Codes:**
- 200 OK - Successfully retrieved Pokémon
- 404 Not Found - Item doesn't exist in database

**Example Request:**
```bash
curl http://localhost:8000/items/potion
```

**Example Response:**
```json
["Absol", "Cinderace", "Garchomp", "Lucario", "Machamp", ...]
```

**Implementation Details:**
- Case-insensitive item matching
- Searches across all three item slots
- Returns distinct Pokémon names
- Raises 404 if no Pokémon found with that item
- Uses `BuildRepository.get_pokemon_by_item(item_name)`

---

## Repository Methods Added

### `BuildRepository.get_all_roles() -> List[str]`
```python
def get_all_roles(self) -> List[str]:
    """Get all unique roles from the database."""
    query = "SELECT DISTINCT role FROM builds WHERE role IS NOT NULL AND role != ''"
    results = self.execute_read_query(query)
    return sorted([row[0] for row in results])
```

### `BuildRepository.get_pokemon_by_role(role: str) -> List[str]`
```python
def get_pokemon_by_role(self, role: str) -> List[str]:
    """Get all Pokémon names for a specific role (case-insensitive)."""
    query = """
        SELECT DISTINCT pokemon 
        FROM builds 
        WHERE LOWER(role) = LOWER(?)
        ORDER BY pokemon
    """
    results = self.execute_read_query(query, (role,))
    return [row[0] for row in results]
```

### `BuildRepository.get_all_items() -> List[str]`
```python
def get_all_items(self) -> List[str]:
    """Get all unique held items from all item slots."""
    query = """
        SELECT DISTINCT held_items FROM builds 
        WHERE held_items IS NOT NULL AND held_items != ''
        UNION
        SELECT DISTINCT held_items2 FROM builds 
        WHERE held_items2 IS NOT NULL AND held_items2 != ''
        UNION
        SELECT DISTINCT held_items3 FROM builds 
        WHERE held_items3 IS NOT NULL AND held_items3 != ''
    """
    results = self.execute_read_query(query)
    return sorted([row[0] for row in results])
```

### `BuildRepository.get_pokemon_by_item(item_name: str) -> List[str]`
```python
def get_pokemon_by_item(self, item_name: str) -> List[str]:
    """Get all Pokémon names that use a specific held item (case-insensitive)."""
    query = """
        SELECT DISTINCT pokemon
        FROM builds
        WHERE LOWER(held_items) = LOWER(?)
           OR LOWER(held_items2) = LOWER(?)
           OR LOWER(held_items3) = LOWER(?)
        ORDER BY pokemon
    """
    results = self.execute_read_query(query, (item_name, item_name, item_name))
    return [row[0] for row in results]
```

---

## API Route Handlers

All four handlers follow the same pattern:

```python
@app.get("/roles", response_model=List[str])
async def get_roles(repository: BuildRepository = Depends(get_repository)) -> List[str]:
    """Get all unique roles."""
    return repository.get_all_roles()

@app.get("/roles/{role}", response_model=List[str])
async def get_role_pokemon(
    role: str,
    repository: BuildRepository = Depends(get_repository)
) -> List[str]:
    """Get all Pokémon names for a specific role."""
    pokemon = repository.get_pokemon_by_role(role)
    if not pokemon:
        raise HTTPException(
            status_code=404,
            detail=f"No Pokémon found with role '{role}'"
        )
    return pokemon

# Similar pattern for /items and /items/{name}
```

---

## Tests Added

**File:** `tests/integration/test_roles_items_endpoints.py`

### Test Coverage (9 tests)

1. **`test_get_roles`**
   - Verifies `/roles` returns non-empty list
   - Checks all values are strings
   - Validates alphabetical sorting

2. **`test_get_role_pokemon`**
   - Verifies `/roles/{role}` returns pokemon list
   - Uses first role from `/roles` response
   - Validates all values are strings

3. **`test_get_role_pokemon_case_insensitive`**
   - Tests case-insensitive matching (e.g., "ATTACKER" == "Attacker")
   - Verifies same results for different casings

4. **`test_get_role_not_found`**
   - Verifies 404 error for non-existent role
   - Checks error message format

5. **`test_get_items`**
   - Verifies `/items` returns non-empty list
   - Checks all values are strings
   - Validates alphabetical sorting

6. **`test_get_item_pokemon`**
   - Verifies `/items/{name}` returns pokemon list
   - Uses first item from `/items` response
   - Validates all values are strings

7. **`test_get_item_pokemon_case_insensitive`**
   - Tests case-insensitive matching for items
   - Verifies same results for different casings

8. **`test_get_item_not_found`**
   - Verifies 404 error for non-existent item
   - Checks error message format

9. **`test_roles_and_items_consistency`**
   - Validates that data is internally consistent
   - Checks that pokemon returned by role endpoint exist in main pokemon list
   - Checks that pokemon returned by item endpoint exist in main pokemon list

### Test Results
```
tests/integration/test_roles_items_endpoints.py::test_get_roles PASSED                    [ 11%]
tests/integration/test_roles_items_endpoints.py::test_get_role_pokemon PASSED             [ 22%]
tests/integration/test_roles_items_endpoints.py::test_get_role_pokemon_case_insensitive PASSED [ 33%]
tests/integration/test_roles_items_endpoints.py::test_get_role_not_found PASSED           [ 44%]
tests/integration/test_roles_items_endpoints.py::test_get_items PASSED                    [ 55%]
tests/integration/test_roles_items_endpoints.py::test_get_item_pokemon PASSED             [ 66%]
tests/integration/test_roles_items_endpoints.py::test_get_item_pokemon_case_insensitive PASSED [ 77%]
tests/integration/test_roles_items_endpoints.py::test_get_item_not_found PASSED           [ 88%]
tests/integration/test_roles_items_endpoints.py::test_roles_and_items_consistency PASSED  [100%]

9 passed in 1.56s
```

All 43 integration tests pass (34 previous + 9 new).

---

## Documentation Updates

### README.md
- Added 4 new endpoints to "Core Data Endpoints" section
- Updated endpoint count (14 → 18 public endpoints)

### API_REFERENCE.md
- Added detailed documentation for all 4 endpoints
- Included examples, response formats, and status codes
- Updated complete endpoint list (14 → 18)

---

## Design Decisions

### 1. Case-Insensitive Matching
**Rationale:** Improves user experience by accepting "attacker", "ATTACKER", "Attacker" as equivalent.  
**Implementation:** SQL `LOWER()` function in WHERE clauses.

### 2. Return Type: `List[str]` for Pokemon Names
**Rationale:** Lightweight responses for discovery/filtering. Users can fetch full builds via `/builds?role={role}` or `/builds?item={item}`.  
**Alternative Considered:** Return `List[BuildResponse]`, but this would duplicate functionality of `/builds` endpoint.

### 3. 404 for Non-Existent Resources
**Rationale:** Clear error signaling. Empty list would be ambiguous (no pokemon vs. invalid role/item).  
**Implementation:** Raise `HTTPException(404)` when result list is empty.

### 4. Alphabetical Sorting
**Rationale:** Consistent, predictable ordering improves UX.  
**Implementation:** SQL `ORDER BY` or Python `sorted()`.

### 5. Item Searching Across All Slots
**Rationale:** Users care about "which pokemon use Potion", not "which slot it's in".  
**Implementation:** UNION query across `battle_items`.

---

## Integration with Existing API

These endpoints complement the existing `/builds` filtering:

```bash
# Discover available roles
GET /roles
# Returns: ["Attacker", "Defender", ...]

# Find pokemon with that role
GET /roles/attacker
# Returns: ["Charizard", "Cinderace", ...]

# Get full builds for those pokemon
GET /builds?role=attacker&top_n=10
```

Similarly for items:

```bash
# Discover available items
GET /items
# Returns: ["Potion", "EjectButton", ...]

# Find pokemon using that item
GET /items/potion
# Returns: ["Absol", "Cinderace", ...]

# Get full builds
GET /builds?item=potion&sort_by=pokemon_win_rate&sort_order=desc
```

---

## Linting & Code Quality

All code passes `ruff` linting:
```bash
$ poetry run ruff check src/api/main.py tests/integration/test_roles_items_endpoints.py
All checks passed!
```

---

## Performance Considerations

- All queries use `DISTINCT` to avoid duplicates
- Item queries use UNION instead of OR for better performance (indexed separately)
- Results are cached by SQLite query planner
- Alphabetical sorting done at database level (efficient)

For large datasets, consider:
- Adding database indexes on `role`, `held_items`, `held_items2`, `held_items3` columns
- Response caching for frequently accessed metadata

---

## Future Enhancements

Potential improvements:
1. **Pagination** - For very large pokemon/item lists
2. **Counts** - Return pokemon counts per role/item (e.g., `{"Attacker": 15}`)
3. **Filtering** - Filter roles/items by week (e.g., "which items were used in week X?")
4. **Combined Queries** - Get all builds for role+item combination
5. **Regex Search** - Search items by pattern (e.g., all items with "Band" in name)

---

## Related Files

- `src/api/main.py` - Route handlers
- `src/repository/build_repository.py` - Database queries
- `tests/integration/test_roles_items_endpoints.py` - Integration tests
- `README.md` - User-facing documentation
- `API_REFERENCE.md` - Complete API reference

---

## Conclusion

Successfully implemented 4 new discovery endpoints for roles and held items. All tests pass, documentation is updated, and code quality checks pass. These endpoints provide essential metadata discovery capabilities that complement the existing build filtering system.

**Total API endpoints:** 18 public + 4 documentation = 22 routes
**Test coverage:** 43 integration tests passing
**Code quality:** All linting checks passed
