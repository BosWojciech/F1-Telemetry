# Multi-stage build for Python Telemetry Processor Service

# ============================================
# Stage 1: Base Stage
# ============================================
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libzmq3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ============================================
# Stage 2: Dependencies Stage
# ============================================
FROM base AS dependencies

# Copy requirements
COPY requirements.txt .

# Create virtual environment and install dependencies
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
RUN /app/.venv/bin/pip install debugpy pytest pytest-asyncio pytest-cov black flake8 mypy

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 8765
EXPOSE 5678

CMD ["python", "main.py", "--mode", "passthrough"]

# ============================================
# Stage 4: Runtime Stage (Production)
# ============================================
FROM base AS runtime

# Copy virtual environment from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy application code
COPY main.py .
COPY zmq_client/ zmq_client/
COPY websocket_server/ websocket_server/

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash telemetry && \
    mkdir -p /app/data /app/logs && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 8765

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8765)); s.close()" || exit 1

CMD ["python", "main.py", "--mode", "passthrough"]
