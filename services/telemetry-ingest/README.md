# F1 Telemetry Ingest Service

High-performance C++ microservice for ingesting and processing F1 game telemetry data.

## Overview

This service listens for UDP telemetry packets from the F1 game, parses the binary data into structured formats, and publishes it via ZeroMQ for downstream processing.

## Features

- **Low-latency UDP packet reception** (port 20777)
- **Binary packet parsing** with strict type safety
- **Data validation and sanitization**
- **Human-readable field mapping** (numeric to string conversions)
- **ZeroMQ publisher** for real-time data streaming
- **Multi-threaded architecture** for optimal performance
- **Health monitoring** and graceful shutdown

## Architecture

```
F1 Game (UDP:20777) → UDP Listener → Packet Parser → Data Mapper → ZeroMQ Publisher (TCP:5555)
```

## Building

### Local Development

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install build-essential cmake libzmq3-dev

# Build
./build_and_run.sh
```

### Docker Build

```bash
# Production build
docker build --target runtime -t f1-telemetry-ingest:latest .

# Development build
docker build --target development -t f1-telemetry-ingest:dev .
```

## Configuration

Environment variables:

- `UDP_LISTEN_PORT` - UDP port for F1 telemetry (default: 20777)
- `ZMQ_PUBLISHER_ENDPOINT` - ZeroMQ publisher endpoint (default: tcp://*:5555)
- `LOG_LEVEL` - Logging level: debug, info, warning, error (default: info)

## Running

### Standalone

```bash
./build/telemetry-ingest
```

### Docker

```bash
docker run -p 20777:20777/udp -p 5555:5555 f1-telemetry-ingest:latest
```

### Docker Compose

```bash
docker-compose up telemetry-ingest
```

## Development

### Dev Container

Open this directory in VS Code with the Dev Containers extension to get a fully configured development environment.

### Debugging

```bash
# Build with debug symbols
cmake --preset=debug
cmake --build build --config Debug

# Run with GDB
gdb ./build/telemetry-ingest
```

### Memory Analysis

```bash
# Check for memory leaks
valgrind --leak-check=full ./build/telemetry-ingest
```

## Testing

The service includes comprehensive tests for:
- Packet parsing accuracy
- Data validation logic
- ZeroMQ message formatting
- Error handling and recovery

## Performance

- **Packet processing**: < 1ms average latency
- **Memory footprint**: ~50MB
- **CPU usage**: < 5% (single core)
- **Supports**: 60+ packets per second (F1 game max rate)

## Monitoring

Health check endpoint available via process monitoring:
```bash
pgrep -f telemetry-ingest
```

## Migration Notes

Future improvements:
- [ ] Replace ZeroMQ with Kafka for better scalability
- [ ] Add Prometheus metrics exporter
- [ ] Implement gRPC API for service-to-service communication
- [ ] Add distributed tracing (OpenTelemetry)
