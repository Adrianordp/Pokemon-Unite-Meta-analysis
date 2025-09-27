# Copilot Instructions for Pokemon Unite Meta Analysis

## Project Overview
- **Type**: Python3.13 + FastAPI backend
- **Build Tool**: Poetry
- **Purpose**: Analyze Pokémon Unite meta (builds, strategies, stats)
- **API**: RESTful API described in `api_route_instructions.md`
- **Testing**: Pytest
- **Linting**: Ruff
- **Roadmap**: See `roadmap.md` for planned features and tasks

## Architecture & Patterns
- **Overview**: Modular, maintainable, testable codebase
- **Functions**: Small, single-responsibility functions
- **Classes**: Each file should contain a single class
- **Modules**: Group related classes/functions into modules
- **Packages**: Group related modules into packages
- **Layers**: Separate layers for models, services, and API routes
- **Dependencies**: Use dependency injection where applicable
- **Design Patterns**: Follow standard class-based design patterns
- **Framework**: FastAPI for building the API
- **Project Structure**: Follow standard FastAPI project layout
- **ORM**: Use SQLAlchemy for database interactions
- **Data Validation**: Use Pydantic models for request/response validation
- **Queries**: Use SQLAlchemy ORM queries
- **Testing**: Unit tests for all functions, integration tests for API endpoints
- **Error Handling**: Use FastAPI's exception handling
- **Clean Architecture**: Separate layers for models, services, and API routes
- **Dependency Injection**: Use FastAPI's dependency injection for services
- **Configuration**: Use environment variables for configuration (e.g., database
URL)

## Software Development Methodology
- **Incremental Development**: Perform a single small task at a time.
- **Testing**: Write tests first for new features and bug fixes.
- **Documentation**: Update documentation (e.g., README, roadmap) as needed
- **Version Control**: Use Git for version control, commit frequently with clear
messages
- **Code Reviews**: If applicable, request code reviews for significant changes
- **Refactoring**: Regularly refactor code for readability and maintainability
- **Continuous Integration**: If applicable, set up CI/CD pipelines for
automated testing and deployment
- **Feedback Loop**: Regularly seek feedback on code quality and project
direction

## Developer Workflows
- **Start Dev Server**: `poetry run uvicorn main:app --reload`
- **Run Unit Tests**: `poetry run pytest tests/unit`
- **Run Integration Tests**: `poetry run pytest tests/integration`
- **Run E2E Tests**: `poetry run pytest tests/e2e`
- **Run All Tests with Coverage**: `poetry run task coverage`
- **Build**: `poetry build`
- **Lint**: `poetry run ruff check .`

## Project-Specific Conventions
- **Line Length**: Keep lines under 80 characters where possible
- **Type Hints**: Use type hints for all functions and methods
- **Logging**: Use custom Python's logging module for logging

## Integration Points
- **Database**: PostgreSQL (connection via SQLAlchemy)
- **External APIs**: If applicable, interact with external APIs using `httpx`

## Remarks
- **Incremental Changes**: Prioritize small, incremental changes that can be
easily tested and reviewed.
- **Testing Coverage**: Always ensure new features are covered by tests.
- **Replanning**: Suggest changes in the roadmap if new features or changes
are needed.

---
If you are unsure about a pattern, check the corresponding component, context,
or test file for examples. When adding new features, follow the structure and
conventions above for consistency.