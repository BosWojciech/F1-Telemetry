# Simulator Architecture: Backend & Frontend Communication

## Overview

The F1 Telemetry Simulator is split into two services:
- **telemetry-simulator-backend** (Python): Generates and sends F1 telemetry data
- **telemetry-simulator-frontend** (React + TypeScript): Control interface for managing simulations

## Communication Options

### Option 1: REST API (Recommended for MVP)

**Benefits:**
- Simple to implement
- No additional infrastructure
- Easy to debug and test
- Standard HTTP/JSON

**Implementation:**
Backend exposes REST endpoints:
```
POST /api/simulation/start
POST /api/simulation/stop
POST /api/simulation/pause
GET  /api/simulation/status
GET  /api/scenarios
POST /api/scenario/load
```

Frontend calls these endpoints via fetch/axios.

### Option 2: WebSocket (For Real-time Updates)

**Benefits:**
- Bi-directional real-time communication
- Push updates from backend to frontend
- Low latency

**Implementation:**
- Backend runs WebSocket server (already used for telemetry-processor)
- Frontend connects via WebSocket client
- Useful for showing live simulation stats, progress, etc.

### Option 3: DAPR (Distributed Application Runtime)

**Benefits:**
- Service invocation abstraction
- Built-in retry, timeout, tracing
- Pub/Sub support
- State management
- Multiple protocol support (HTTP, gRPC)

**Considerations:**
- Adds complexity (sidecar containers)
- Better suited for production microservices at scale
- Might be overkill for this simulator use case
- Requires DAPR CLI and runtime

**If using DAPR:**
```yaml
# docker-compose.yml additions
telemetry-simulator-backend:
  # ... existing config
  
telemetry-simulator-backend-dapr:
  image: "daprio/daprd:latest"
  command: [
    "./daprd",
    "-app-id", "simulator-backend",
    "-app-port", "8080",
    "-dapr-http-port", "3500",
    "-placement-host-address", "dapr-placement:50006"
  ]
  depends_on:
    - telemetry-simulator-backend
  network_mode: "service:telemetry-simulator-backend"

telemetry-simulator-frontend:
  # ... existing config

telemetry-simulator-frontend-dapr:
  image: "daprio/daprd:latest"
  command: [
    "./daprd",
    "-app-id", "simulator-frontend",
    "-app-port", "3001",
    "-dapr-http-port", "3500"
  ]
  depends_on:
    - telemetry-simulator-frontend
  network_mode: "service:telemetry-simulator-frontend"

dapr-placement:
  image: "daprio/dapr:latest"
  command: ["./placement", "-port", "50006"]
```

## Recommended Approach

### Phase 1: REST API (Current)
Start with a simple REST API in the backend:
- Fast to implement
- Easy to test
- Good for basic control (start/stop/configure)

### Phase 2: Add WebSocket (If needed)
Add WebSocket for real-time features:
- Live simulation progress
- Real-time statistics
- Live lap updates

### Phase 3: Consider DAPR (Future)
Only if you need:
- Complex microservices orchestration
- Service mesh features
- Multi-cloud deployment
- Advanced observability

## Implementation Checklist

### Backend (Python)
- [ ] Add Flask/FastAPI for REST endpoints
- [ ] Implement simulation control logic
- [ ] Add scenario management
- [ ] Optional: Add WebSocket server for updates

### Frontend (React)
- [x] Install dependencies: `cd services/telemetry-simulator-frontend && npm install`
- [x] Generate protobuf types: `make proto` (uses ts-proto for TypeScript)
- [ ] Create UI for simulation controls
- [ ] Add scenario selector/loader
- [ ] Implement API client (fetch/axios)
- [ ] Display simulation status
- [ ] Optional: WebSocket client for real-time updates

### Docker
- [x] Update docker-compose.yml
- [x] Update docker-compose.dev.yml
- [ ] Add backend API port exposure (e.g., 8080)
- [ ] Configure environment variables

### Documentation
- [x] Update README.md
- [x] Update DEVELOPMENT.md
- [x] Update service-specific READMEs
- [ ] Add API documentation (OpenAPI/Swagger)

## Example Backend API (Flask)

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    # Start simulation logic
    return jsonify({"status": "started"})

@app.route('/api/simulation/status', methods=['GET'])
def get_status():
    return jsonify({
        "running": True,
        "scenario": "race_simulation",
        "lap": 5,
        "total_laps": 20
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Example Frontend API Client

```typescript
class SimulatorAPI {
  private baseURL = 'http://localhost:8080/api';

  async startSimulation() {
    const response = await fetch(`${this.baseURL}/simulation/start`, {
      method: 'POST',
    });
    return response.json();
  }

  async getStatus() {
    const response = await fetch(`${this.baseURL}/simulation/status`);
    return response.json();
  }
}
```

## Conclusion

**For this project, I recommend starting with REST API + WebSocket** for the following reasons:
1. Simple and familiar patterns
2. No additional infrastructure (DAPR sidecars, placement service)
3. Easy to debug and test
4. REST for control, WebSocket for real-time updates
5. Can always migrate to DAPR later if needed

DAPR would be beneficial if you plan to:
- Scale to many microservices
- Deploy across multiple clouds
- Need advanced service mesh features
- Require sophisticated retry/circuit breaker patterns
