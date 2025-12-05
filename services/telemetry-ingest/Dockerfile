# Multi-stage build for C++ Telemetry Ingest Service

# ============================================
# Stage 1: Build Stage
# ============================================
FROM ubuntu:24.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libzmq3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy CMake configuration and source files
COPY CMakeLists.txt CMakePresets.json ./
COPY include/ include/
COPY src/ src/

# Build the application
RUN cmake --preset=default \
    && cmake --build build --config Release

# ============================================
# Stage 2: Development Stage
# ============================================
FROM ubuntu:24.04 AS development

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gdb \
    git \
    libzmq3-dev \
    pkg-config \
    valgrind \
    libgtest-dev \
    googletest \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Don't build during image creation - let postCreateCommand handle it
# This allows the devcontainer to build with the mounted source code

EXPOSE 20777/udp
EXPOSE 5555

CMD ["bash"]

# ============================================
# Stage 3: Runtime Stage (Production)
# ============================================
FROM ubuntu:24.04 AS runtime

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libzmq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash telemetry

WORKDIR /app

# Copy built binary from builder stage
COPY --from=builder /app/build/telemetry-ingest /app/telemetry-ingest
COPY --from=builder /app/build/*.so* /app/

# Create logs directory
RUN mkdir -p /app/logs && chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 20777/udp
EXPOSE 5555

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f telemetry-ingest || exit 1

CMD ["./telemetry-ingest"]
