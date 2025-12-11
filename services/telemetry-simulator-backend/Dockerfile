# Multi-stage Dockerfile for F1 Telemetry Simulator FastAPI Backend

# ============================================
# Base Stage - Install Poetry
# ============================================
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# ============================================
# Dependencies Stage
# ============================================
FROM base AS dependencies

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main

# ============================================
# Development Stage
# ============================================
FROM base AS development

# Copy pyproject.toml and install all dependencies (including dev)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Production Stage
# ============================================
FROM base AS production

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY main.py ./
COPY proto/ proto/

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/app/.venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"]

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
