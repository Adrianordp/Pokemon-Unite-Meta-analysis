# ── base: shared setup ────────────────────────────────────────────────────────
FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --locked --no-install-project --group api --group dashboard

COPY src ./src

RUN uv sync --locked --no-dev --group api --group dashboard

# ── api ────────────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS api
WORKDIR /app

RUN useradd -m appuser
RUN chown -R appuser:appuser /app

COPY --from=base --chown=appuser:appuser /app /app
COPY builds.db ./

ENV PYTHONPATH=/app/.venv/bin:$PATH
ENV PYTHONBUFFERED=1
ENV API_HOST=localhost
ENV API_PORT=8050

EXPOSE 8050

# Start FastAPI using uvicorn from the project virtualenv.
CMD ["/bin/sh", "-c", "exec /app/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port \"${API_PORT}\" --proxy-headers --forwarded-allow-ips='*'"]

# ── dashboard ──────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS dashboard
WORKDIR /app

RUN useradd -m appuser
RUN chown -R appuser:appuser /app

COPY --from=base --chown=appuser:appuser /app /app

ENV PYTHONPATH=/app/.venv/bin:$PATH
ENV PYTHONBUFFERED=1
ENV API_HOST=localhost
ENV API_PORT=8050

EXPOSE 8501

CMD ["/bin/sh", "-c", \
    "exec /app/.venv/bin/streamlit run src/dashboard/dashboard.py --server.address=0.0.0.0 --server.port=8501" \
    ]
