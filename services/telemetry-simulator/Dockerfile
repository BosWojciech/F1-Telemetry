# Multi-stage build for Python Telemetry Simulator Service

# ============================================
# Stage 1: Base Stage
# ============================================
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ============================================
# Stage 2: Dependencies Stage
# ============================================
FROM base AS dependencies

COPY requirements.txt .

RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

# ============================================
# Stage 3: Development Stage
# ============================================
FROM base AS development

# Install development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY . .

# Install development dependencies
RUN /app/.venv/bin/pip install debugpy pytest black flake8 mypy

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 5679

CMD ["python", "simulator.py"]

# ============================================
# Stage 4: Runtime Stage (Production)
# ============================================
FROM base AS runtime

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY simulator.py .
COPY packet_generator.py .
COPY config/ config/

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.close()" || exit 1

CMD ["python", "simulator.py"]
