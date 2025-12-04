# F1 Telemetry Processor Service

Python-based middleware service for processing and routing F1 telemetry data.

## Overview

This service acts as the central hub between the telemetry ingest service and frontend clients, providing real-time data streaming and optional data collection capabilities.

## Features

- **ZeroMQ subscriber** for receiving telemetry data from ingest service
- **WebSocket server** for real-time frontend communication
- **Dual operation modes**:
  - `passthrough`: Real-time data forwarding
  - `datacollection`: Data deduplication and storage
- **Async/await architecture** for high concurrency
- **Structured logging** with JSON output
- **Graceful shutdown** handling
- **Health monitoring** endpoint

## Architecture

```
ZeroMQ (TCP:5555) → Data Processor → WebSocket Server (TCP:8765) → Frontend Clients
                    ↓
              [Optional] Data Storage
```

## Installation

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Build

```bash
# Production build
docker build --target runtime -t f1-telemetry-processor:latest .

# Development build
docker build --target development -t f1-telemetry-processor:dev .
```

## Configuration

Environment variables:

- `ZMQ_SUBSCRIBER_ENDPOINT` - ZeroMQ subscriber endpoint (default: tcp://telemetry-ingest:5555)
- `WEBSOCKET_HOST` - WebSocket server host (default: 0.0.0.0)
- `WEBSOCKET_PORT` - WebSocket server port (default: 8765)
- `MODE` - Operation mode: passthrough or datacollection (default: passthrough)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

## Running

### Standalone

```bash
# Passthrough mode
python main.py --mode passthrough

# Data collection mode
python main.py --mode datacollection

# With debug logging
python main.py --mode passthrough --log-level DEBUG
```

### Docker

```bash
docker run -p 8765:8765 -e MODE=passthrough f1-telemetry-processor:latest
```

### Docker Compose

```bash
docker-compose up telemetry-processor
```

## Development

### Dev Container

Open this directory in VS Code with the Dev Containers extension for a fully configured Python development environment.

### Debugging

The service supports remote debugging with `debugpy`:

```bash
# In dev mode, debugger listens on port 5678
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py --mode passthrough
```

Configure VS Code launch.json:
```json
{
    "name": "Attach to Processor",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    }
}
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test/test_zmq_client.py
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8 .

# Type checking
mypy .
```

## API

### WebSocket Protocol

Connect to `ws://localhost:8765`

Messages are JSON-formatted telemetry packets:
```json
{
    "packetType": "SessionData",
    "timestamp": 1234567890,
    "data": { ... }
}
```

## Operation Modes

### Passthrough Mode
- Forwards all telemetry data in real-time
- Minimal processing overhead
- Best for live monitoring

### Data Collection Mode
- Deduplicates similar packets
- Stores meaningful state changes
- Suitable for post-race analysis and ML training

## Performance

- **Message throughput**: 1000+ messages/second
- **WebSocket clients**: Supports 100+ concurrent connections
- **Memory footprint**: ~100MB
- **CPU usage**: < 10% (single core)

## Monitoring

### Health Check
```bash
curl http://localhost:8765/health
```

### Logs
Structured JSON logs are written to stdout:
```json
{
    "event": "telemetry_received",
    "timestamp": "2025-12-04T10:30:00Z",
    "level": "info",
    "packet_type": "CarTelemetry"
}
```

## Migration Notes

Future improvements:
- [ ] Replace ZeroMQ with Kafka consumer
- [ ] Add InfluxDB integration for time-series storage
- [ ] Implement Graylog logging
- [ ] Add Prometheus metrics
- [ ] GraphQL API for historical data queries
- [ ] Redis caching layer
