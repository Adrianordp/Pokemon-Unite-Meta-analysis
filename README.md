# Pokémon Unite Meta Analysis

This project provides tools and scripts for analyzing the meta of Pokémon Unite, focusing on builds, strategies, and statistical insights. It is organized as a
Python package and uses Poetry for dependency management.

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
   poetry run uvicorn main:app --reload
   ```
5. Access the API documentation at `http://localhost:8000/docs`
