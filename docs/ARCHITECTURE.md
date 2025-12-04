# Service Architecture Documentation

## Overview

The F1 Telemetry System is built using a microservices architecture, with each service responsible for a specific domain of functionality.

## Services

### 1. Telemetry Ingest Service

**Technology**: C++17, CMake, ZeroMQ

**Responsibilities**:
- Listen for UDP telemetry packets from F1 game
- Parse binary packet data into structured formats
- Validate packet integrity
- Map numeric codes to human-readable values
- Publish processed data via ZeroMQ

**Key Components**:
- `udpClient.h/cpp`: UDP socket listener
- `PacketHandlers.h/cpp`: Packet parsing logic
- `TelemetryProcessor.h/cpp`: Main processing pipeline
- `DataMaps.h`: Lookup tables for value mapping
- `zmqPublisher.h/cpp`: ZeroMQ message publisher

**Performance Characteristics**:
- Latency: < 1ms per packet
- Throughput: 60+ packets/second
- Memory: ~50MB
- CPU: < 5% (single core)

### 2. Telemetry Processor Service

**Technology**: Python 3.11, AsyncIO, ZeroMQ, WebSockets

**Responsibilities**:
- Subscribe to telemetry data from ingest service
- Process and filter data based on mode
- Manage WebSocket connections
- Stream data to frontend clients
- (Optional) Store data for analysis

**Key Components**:
- `main.py`: Service orchestrator
- `zmq_client/zmq_client.py`: ZeroMQ subscriber
- `websocket_server/websocket_server.py`: WebSocket server

**Operation Modes**:
- **Passthrough**: Real-time forwarding
- **Data Collection**: Deduplication and storage

**Performance Characteristics**:
- Throughput: 1000+ messages/second
- Concurrent clients: 100+
- Memory: ~100MB
- CPU: < 10% (single core)

### 3. Telemetry Frontend Service

**Technology**: React 18, TypeScript, Redux, Vite, Nginx

**Responsibilities**:
- Display real-time telemetry data
- Manage WebSocket connection
- Render F1-style MFD interface
- Handle user interactions
- State management with Redux

**Key Components**:
- `App.tsx`: Main application component
- `redux/store.ts`: State management
- `redux/packetDispatcher.ts`: Packet routing
- `socket/socketService.ts`: WebSocket client
- `PacketTypes.ts`: Type definitions

**Performance Characteristics**:
- Bundle size: ~500KB (gzipped)
- Initial load: < 2s
- Frame rate: 60 FPS
- WebSocket latency: < 50ms

## Communication Patterns

### Inter-Service Communication

```
Ingest → ZeroMQ (PUB/SUB) → Processor → WebSocket → Frontend
```

**Current**: ZeroMQ (TCP)
**Future**: Apache Kafka

### Data Flow

1. F1 game sends UDP packets (20777/udp)
2. Ingest service receives and parses packets
3. Ingest publishes JSON to ZeroMQ (5555)
4. Processor subscribes to ZeroMQ feed
5. Processor filters/processes data
6. Processor broadcasts via WebSocket (8765)
7. Frontend receives and displays data

## Deployment Architecture

### Development

```
Developer
    ↓
Dev Container (VS Code)
    ↓
Docker Compose (Dev Mode)
    ↓
Hot Reload & Debugging
```

### Production

```
Docker Host
    ↓
Docker Compose
    ├── telemetry-ingest
    ├── telemetry-processor
    └── telemetry-frontend (Nginx)
    ↓
Monitoring Stack (Prometheus, Grafana, Loki)
```

### Future: Kubernetes

```
Ingress Controller
    ↓
Services
    ├── telemetry-ingest (Deployment)
    ├── telemetry-processor (Deployment)
    └── telemetry-frontend (Deployment)
    ↓
Persistent Storage (StatefulSets)
Message Broker (Kafka)
```

## Scalability Considerations

### Horizontal Scaling

- **Ingest**: Single instance (UDP listener)
- **Processor**: Multiple instances with load balancing
- **Frontend**: Multiple instances behind Nginx/CDN

### Vertical Scaling

- Ingest: CPU-bound (single-threaded)
- Processor: I/O-bound (async)
- Frontend: Static assets (CDN recommended)

## Security

### Network Isolation

- Services communicate within Docker network
- Only necessary ports exposed to host
- Reverse proxy for external access

### Container Security

- Non-root users
- Read-only filesystems where possible
- Minimal base images
- Regular vulnerability scans

### Secrets Management

- Environment variables
- Docker secrets (production)
- External secret managers (future)

## Monitoring & Observability

### Metrics

- Container metrics (cAdvisor)
- System metrics (Node Exporter)
- Application metrics (Prometheus exporters - future)

### Logging

- Structured JSON logs
- Centralized aggregation (Loki)
- Log levels: DEBUG, INFO, WARNING, ERROR

### Tracing (Future)

- OpenTelemetry instrumentation
- Distributed tracing
- Service dependency mapping

## Migration Path

### Phase 1: Current State
- ZeroMQ messaging
- Docker Compose deployment
- Manual scaling

### Phase 2: Enhanced Observability
- Prometheus metrics
- Distributed tracing
- Advanced dashboards

### Phase 3: Cloud-Native
- Kafka messaging
- Kubernetes orchestration
- Auto-scaling
- Multi-region deployment

### Phase 4: Advanced Features
- Machine learning integration
- Real-time analytics
- Multi-game support
- Mobile applications
