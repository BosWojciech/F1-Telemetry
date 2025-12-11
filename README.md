# F1 Telemetry System

[![CI](https://github.com/BosWojciech/F1-Telemetry/workflows/CI/badge.svg)](https://github.com/BosWojciech/F1-Telemetry/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-%3E50%25-brightgreen.svg)](https://codecov.io)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Professional, production-ready microservices architecture for real-time F1 game telemetry processing, analysis, and visualization. Fully tested with 50%+ code coverage.

## 🏎️ Overview

A production-ready, multi-layer telemetry pipeline designed to ingest, process, and visualize real-time F1 game data. Built with scalability, maintainability, and developer experience in mind.

## 🏗️ Architecture

The system consists of three microservices communicating via ZeroMQ (with future Kafka migration planned):

```
┌─────────────────────┐
│   F1 Game (UDP)    │
└──────────┬──────────┘
           │ UDP:20777
           ▼
┌─────────────────────┐
│ Telemetry Ingest    │  ← C++ UDP listener & parser
│   (Service 1)       │
└──────────┬──────────┘
           │ ZeroMQ (TCP:5555)
           ▼
┌─────────────────────┐
│ Telemetry Processor │  ← Python middleware
│   (Service 2)       │
└──────────┬──────────┘
           │ WebSocket (TCP:8765)
           ▼
┌─────────────────────┐
│ Telemetry Frontend  │  ← React dashboard
│   (Service 3)       │
└─────────────────────┘
```

### Services

| Service | Technology | Port(s) | Description |
|---------|-----------|---------|-------------|
| **telemetry-ingest** | C++17, ZeroMQ | 20777/udp, 5555 | High-performance UDP packet receiver and binary parser |
| **telemetry-processor** | Python 3.11, AsyncIO | 8765 | Middleware for data processing and WebSocket streaming |
| **telemetry-frontend** | React 18, TypeScript, Redux | 3000 | Real-time telemetry dashboard with F1-style UI |

## 🚀 Quick Start

### Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- Make (optional, for convenience commands)

### Running the System

```bash
# Clone the repository
git clone https://github.com/BosWojciech/F1-Telemetry.git
cd F1-Telemetry

# Initialize environment
make init

# Start all services (production mode)
make up

# Or start in development mode with hot-reload
make dev-up
```

Access the dashboard at:
- **Production**: http://localhost:3000
- **Development**: http://localhost:5173

### Available Commands

```bash
make help              # Show all available commands
make build             # Build all services
make up                # Start production services
make down              # Stop all services
make logs              # View logs from all services
make ps                # List running services
make health            # Check service health status
```

## 💻 Development

### Dev Containers

Each service has a dedicated dev container configuration for isolated development:

1. **Open a service in VS Code**
   ```bash
   code services/telemetry-ingest
   ```

2. **Reopen in Container**
   - Press `F1` → "Dev Containers: Reopen in Container"
   - Or click the notification to reopen in container

3. **Start coding!**
   - All dependencies pre-installed
   - Debugging configured
   - Extensions ready

### Protobuf Setup

The project uses Protocol Buffers for data definitions. To generate the necessary code:

1.  **Install Dependencies**:
    ```bash
    make setup-proto
    ```

2.  **Generate Code**:
    ```bash
    make proto
    ```
    This will generate Python code in `services/telemetry-simulator/proto`.

    You can specify the F1 game version (default is 23):
    ```bash
    make proto F1_GAME_VERSION=23
    ```

### Local Development Setup

#### Telemetry Ingest (C++)

```bash
cd services/telemetry-ingest
./build_and_run.sh
```

#### Telemetry Processor (Python)

```bash
cd services/telemetry-processor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --mode passthrough
```

#### Telemetry Frontend (React)

```bash
cd services/telemetry-frontend
npm install
npm run dev
```

## 📊 Monitoring & Observability

Start the monitoring stack:

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

Access monitoring tools:
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8080

### Available Metrics

- Container resource usage (CPU, memory, network)
- Service health and uptime
- Request rates and latencies
- Custom application metrics (when instrumented)

## 🧪 Testing

The project has comprehensive test coverage (50%+ minimum) across all services.

### Run All Tests

```bash
# Run all tests at once
make test-all

# Or run individual service tests
make test-cpp         # C++ telemetry-ingest tests (Google Test)
make test-processor   # Python processor tests (pytest)
make test-simulator   # Python simulator tests (pytest)
make test-frontend    # React frontend tests (Vitest)
make test-e2e        # End-to-end integration tests
```

### Test Coverage

```bash
# Generate coverage reports for all services
make test-coverage

# View reports
open services/telemetry-processor/htmlcov/index.html
open services/telemetry-simulator/htmlcov/index.html
open services/telemetry-frontend/coverage/index.html
```

### Test Statistics

| Service | Test Framework | Test Cases | Coverage |
|---------|---------------|-----------|----------|
| **telemetry-ingest** | Google Test | 9 | >50% |
| **telemetry-processor** | pytest | 32 | >50% |
| **telemetry-simulator** | pytest | 29 | >50% |
| **telemetry-frontend** | Vitest | 21 | >50% |
| **E2E Tests** | pytest | 7 | N/A |

### CI/CD Testing

All tests run automatically on push/PR:
- ✅ Unit tests for all services
- ✅ Coverage enforcement (50% minimum)
- ✅ Multi-version testing (Python 3.10-3.12, Node 18-20)
- ✅ E2E integration tests
- ✅ Docker build verification

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed testing documentation.

## 🔒 Security

- All services run as non-root users
- Security headers configured in Nginx
- Container vulnerability scanning via Trivy
- Dependency updates automated via Dependabot
- Secrets managed via environment variables

## 🚢 Deployment

### Container Registry

Images are automatically built and pushed to GitHub Container Registry on `main` branch:

```bash
docker pull ghcr.io/boswojciech/f1-telemetry/telemetry-ingest:latest
docker pull ghcr.io/boswojciech/f1-telemetry/telemetry-processor:latest
docker pull ghcr.io/boswojciech/f1-telemetry/telemetry-frontend:latest
```

### Kubernetes (Future)

Helm charts and Kubernetes manifests coming soon.

## 📝 Configuration

All services are configured via environment variables. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Key configuration options:
- `UDP_LISTEN_PORT`: F1 game telemetry port (default: 20777)
- `ZMQ_PUBLISHER_ENDPOINT`: ZeroMQ publisher endpoint
- `WEBSOCKET_PORT`: WebSocket server port (default: 8765)
- `MODE`: Processor mode (passthrough/datacollection)
- `LOG_LEVEL`: Logging verbosity (debug/info/warning/error)

## 🛣️ Roadmap

### Short-term (v2.0)
- [ ] Migrate from ZeroMQ to Kafka
- [ ] Add Prometheus metrics exporters to all services
- [ ] Implement InfluxDB for time-series data storage
- [ ] Add comprehensive unit and integration tests
- [ ] Create Grafana dashboards for telemetry visualization

### Mid-term (v3.0)
- [ ] gRPC service-to-service communication
- [ ] OpenTelemetry distributed tracing
- [ ] GraphQL API for historical data
- [ ] Redis caching layer
- [ ] Multi-game support (F1 24, F1 25)

### Long-term (v4.0)
- [ ] Machine learning models for race strategy optimization
- [ ] Real-time race simulation and prediction
- [ ] Multi-user support with authentication
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] Mobile applications (iOS/Android)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

- **Wojciech Bos** - *Initial work* - [GitHub](https://github.com/BosWojciech) | [LinkedIn](https://www.linkedin.com/in/wbos/)

## 🙏 Acknowledgments

- F1 game telemetry specification
- Open source libraries and tools used in this project
- The F1 and sim racing community

## 📞 Support

- **Documentation**: [/docs](./docs)
- **Issues**: [GitHub Issues](https://github.com/BosWojciech/F1-Telemetry/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BosWojciech/F1-Telemetry/discussions)

---

**Note**: This system is designed for F1 game telemetry data and is not affiliated with Formula 1, the FIA, or any F1 teams.
