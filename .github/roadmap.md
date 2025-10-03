# Roadmap

## Feature Branches & Tasks

> This section tracks feature branches and tasks, grouped to match the "Planned: REST API & Web Features" roadmap.

### API Foundation (`feature/api-foundation`)
- [x] Create branch `feature/api-foundation`
- [x] Set up FastAPI server in `src/api/`
- [x] Implement health check endpoint
- [x] Add environment variable support for API config
- [x] Write integration tests for server startup and health check

### Build Retrieval, Filtering & Sorting Endpoints (`feature/builds-endpoint`)
- [x] Create branch `feature/builds-endpoint`
- [x] Implement `/builds` endpoint with all query parameters
- [x] Implement filtering, sorting, and relevance logic
- [x] Write integration tests for `/builds` endpoint
- [x] Document API request/response models (Pydantic)

### Swagger/OpenAPI Documentation (`feature/setup-swagger-documentation`)
- [x] Create branch `feature/setup-swagger-documentation`
- [x] Implement Swagger/OpenAPI documentation for all endpoints
- [x] Ensure docs are accessible at `/docs` and `/redoc`
- [x] Write tests to verify documentation generation
- [x] Document API usage examples in README

### Database Refactor (`refactor/Migrate-to-single-builds-table`)
- [x] Migrate from per-week tables to a single `builds` table with a `week` column
- [x] Update all API endpoints, repository, and tests to use the new schema
- [x] Add migration script and documentation
- [x] Ensure all new features use the unified schema

### Champion Data Endpoints (`feature/champion-endpoints`)
- [x] Create branch `feature/champion-endpoints`
- [ ] Implement `/pokemon`, `/pokemon/{name}` endpoints
- [ ] Implement champion data endpoints (FastAPI)
- [ ] Write integration tests for champion endpoints
- [ ] Document endpoints

### Metagame Analysis Endpoints (`feature/metagame-analysis-endpoint`)
- [ ] Create branch `feature/metagame-analysis-endpoint`
- [ ] Implement analysis endpoints (`/relevance`, `/relevance/{strategy}`, `/sort_by`, `/sort_by/{criteria}`)
- [ ] Write integration tests for analysis endpoints
- [ ] Document endpoints

### IDs, Weeks, Filters, Logs Endpoints (`feature-meta-endpoints`)
- [ ] Create branch `feature-meta-endpoints`
- [ ] Implement `/ids`, `/weeks`, `/filters`, `/filters/{filter_name}`, `/logs` endpoints
- [ ] Write integration tests for these endpoints
- [ ] Document endpoints

### Continuous Integration/Deployment (`feature-api-ci-cd`)
- [ ] Create branch `feature-api-ci-cd`
- [ ] Add API tests and linting to CI workflow
- [ ] Ensure coverage enforcement for API code
- [ ] Set up CD pipeline for deployment (optional/when ready)
- [ ] Document CI/CD setup

### Documentation & Linting (`feature-api-docs`)
- [ ] Create branch `feature-api-docs`
- [ ] Ensure Swagger/OpenAPI docs are generated and complete
- [ ] Update README with API usage examples
- [ ] Ensure code quality and linting for API code (ruff, black)

### Data Models & Validation (`feature-api-models`)
- [ ] Create branch `feature-api-models`
- [ ] Implement Pydantic models for request/response validation
- [ ] Add tests for model validation
- [ ] Document models

### Error Handling (`feature-api-errors`)
- [ ] Create branch `feature-api-errors`
- [ ] Implement FastAPI exception handling for invalid queries
- [ ] Add tests for error cases
- [ ] Document error handling

### User Management & Data Visualization (`feature-future-enhancements`)
- [ ] Create branch `feature-future-enhancements`
- [ ] Plan and test user management features (authentication, authorization)
- [ ] Plan and test data visualization endpoints (charts, plots)
- [ ] Consider migration from SQLite to PostgreSQL for production
- [ ] Add support for external data sources (future integrations)

