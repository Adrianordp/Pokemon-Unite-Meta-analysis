# ── base: shared setup ────────────────────────────────────────────────────────
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src

# ── api ────────────────────────────────────────────────────────────────────────
FROM base AS api

RUN poetry install --only main,api --no-root

COPY builds.db ./

ENV API_HOST=localhost \
    API_PORT=8050

EXPOSE 8050

CMD [ \
    "poetry", "run", \
    "python", "-m", "api.main" \
    ]

# ── dashboard ──────────────────────────────────────────────────────────────────
FROM base AS dashboard

RUN poetry install --only main,dashboard --no-root

ENV API_HOST=localhost \
    API_PORT=8050

EXPOSE 8501

CMD [ \
    "poetry", "run", \
    "streamlit", "run", "src/dashboard/dashboard.py", \
    "--server.address=0.0.0.0", \
    "--server.port=8501" \
    ]
