# F1 Telemetry System - Development Guide

Complete guide for setting up, developing, and deploying the F1 Telemetry microservices platform.

## Table of Contents

- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Development Environment Setup](#development-environment-setup)
- [Service Development](#service-development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Git** 2.30+
- For local development:
  - C++17 compiler (GCC 9+, Clang 10+)
  - Python 3.10+
  - Node.js 18+
  - CMake 3.20+

### Running the Full System

```bash
# Clone the repository
git clone https://github.com/BosWojciech/F1-Telemetry.git
cd F1-Telemetry

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access frontend
open http://localhost:3000
```

### Running with Test Simulator

```bash
# Start services with simulator
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Simulator will send test packets to UDP port 20777
docker-compose logs -f telemetry-simulator-backend
```

---

## System Architecture

### Microservices Overview

```
┌─────────────┐      UDP:20777      ┌──────────────┐
│             │ ───────────────────> │              │
│  F1 Game /  │                      │  Telemetry   │
│  Simulator  │                      │   Ingest     │
│             │                      │   (C++)      │
└─────────────┘                      └──────┬───────┘
                                            │ ZMQ TCP:5555
                                            v
                                     ┌──────────────┐
                                     │  Telemetry   │
                                     │  Processor   │
                                     │   (Python)   │
                                     └──────┬───────┘
                                            │ WebSocket:8765
                                            v
                                     ┌──────────────┐
                                     │  Telemetry   │
                                     │  Frontend    │
                                     │  (React)     │
                                     └──────────────┘
```

### Service Details

#### 1. Telemetry Ingest Service (C++)
- **Purpose**: High-performance UDP packet receiver and parser
- **Tech Stack**: C++17, ZeroMQ, CMake
- **Port**: UDP 20777
- **Output**: ZMQ TCP 5555

#### 2. Telemetry Processor Service (Python)
- **Purpose**: Data filtering, transformation, and WebSocket relay
- **Tech Stack**: Python 3.11, ZeroMQ, WebSockets
- **Input**: ZMQ TCP 5555
- **Output**: WebSocket 8765

#### 3. Telemetry Frontend Service (React)
- **Purpose**: Real-time telemetry visualization dashboard
- **Tech Stack**: React 19, TypeScript, Redux, Vite
- **Port**: HTTP 3000
- **WebSocket**: 8765

#### 4. Telemetry Simulator Service (Python)
- **Purpose**: Generate test telemetry without F1 game
- **Tech Stack**: Python 3.11, Standard Library
- **Output**: UDP 20777

---

## Development Environment Setup

### Option 1: Dev Containers (Recommended)

Each service has a standalone `.devcontainer` configuration for independent development.

**Multi-Service Workflow:**
```bash
# Open multiple services simultaneously in separate VS Code windows
code services/telemetry-simulator-backend     # Window 1: Simulator Backend
code services/telemetry-simulator-frontend    # Window 2: Simulator Frontend
code services/telemetry-ingest                # Window 3: Ingest
code services/telemetry-processor             # Window 4: Processor
code services/telemetry-frontend              # Window 5: Frontend

# Each window will prompt: "Reopen in Container"
# Or use Command Palette: "Dev Containers: Reopen in Container"
```

**Single Service Development:**
```bash
# Work on just one service
code services/telemetry-processor
# Reopen in container when prompted
```

**Benefits:**
- ✅ Each service runs in its own isolated container
- ✅ Work on multiple services simultaneously (e.g., simulator + ingest)
- ✅ All dependencies pre-installed per service
- ✅ Services communicate via `--network=host` 
- ✅ No context switching between extensions
- ✅ Consistent environment across team members

### Option 2: Devpod (Remote Development)

[DevPod](https://devpod.sh/) enables remote development with containers.

```bash
# Install devpod
brew install devpod

# Create workspace from repository
devpod up https://github.com/BosWojciech/F1-Telemetry

# Select service to develop
devpod ssh F1-Telemetry
cd services/telemetry-processor
```

### Option 3: Local Development

#### C++ Service (Ingest)

```bash
cd services/telemetry-ingest

# Install dependencies (Ubuntu/Debian)
sudo apt-get install -y build-essential cmake libzmq3-dev libgtest-dev

# Build
cmake --preset=default
cmake --build build

# Run tests
cd build && ctest --verbose

# Run service
./build/telemetry-ingest
```

#### Python Services (Processor & Simulator)

**Using Poetry (Recommended):**

```bash
cd services/telemetry-processor

# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run tests with coverage
poetry run pytest

# Run service
poetry run python main.py --mode passthrough
```

**Using pip (Legacy):**

```bash
cd services/telemetry-processor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=.

# Run service
python main.py --mode passthrough
```

#### Frontend Service

```bash
cd services/telemetry-frontend

# Install dependencies
npm install

# Run tests
npm run test

# Run development server
npm run dev

# Build for production
npm run build
```

---

## Service Development

### Telemetry Ingest (C++)

#### Building

```bash
cd services/telemetry-ingest

# Configure with tests
cmake --preset=default -DBUILD_TESTS=ON

# Build
cmake --build build -j$(nproc)

# Run tests
cd build
ctest --output-on-failure
```

#### Adding Packet Types

1. Add packet definition to `include/core/DataTypes.h`
2. Implement parser in `src/core/PacketHandlers.cpp`
3. Add JSON serialization in `src/core/TelemetryProcessor.cpp`
4. Write tests in `tests/test_packet_handlers.cpp`

#### Memory Management

```bash
# Run with Valgrind
valgrind --leak-check=full --show-leak-kinds=all ./build/telemetry-ingest

# Address Sanitizer
cmake --preset=default -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-fsanitize=address"
```

### Telemetry Processor (Python)

#### Development Workflow

```bash
cd services/telemetry-processor

# Install dev dependencies
pip install pytest pytest-cov black flake8 mypy

# Format code
black .

# Lint
flake8 .

# Type check
mypy . --ignore-missing-imports

# Run tests
pytest tests/ -v
```

#### Adding Features

1. Implement in respective module (`zmq_client/`, `websocket_server/`)
2. Add tests in `tests/`
3. Update `main.py` if needed
4. Run tests: `pytest tests/ --cov=.`

### Telemetry Frontend (React)

#### Development Workflow

```bash
cd services/telemetry-frontend

# Install dependencies
npm install

# Run dev server (with hot reload)
npm run dev

# Run tests (watch mode)
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Lint
npm run lint

# Type check
npx tsc --noEmit
```

#### Adding Components

1. Create component in `src/components/`
2. Add tests: `src/components/MyComponent.test.tsx`
3. Import and use in `App.tsx`
4. Update Redux store if needed (`src/redux/`)

---

## Testing

### Unit Tests

Each service has its own test suite with **50% minimum coverage**.

#### C++ Tests (Google Test)

```bash
cd services/telemetry-ingest/build
ctest --verbose

# Run specific test
./tests/f1-telemetry-ingest_tests --gtest_filter=*MotionData*
```

#### Python Tests (pytest)

```bash
# Processor
cd services/telemetry-processor
pytest tests/ -v --cov=. --cov-report=html

# Simulator Backend
cd services/telemetry-simulator-backend
pytest tests/ -v --cov=. --cov-report=html

# View coverage
open htmlcov/index.html
```

#### TypeScript Tests (Vitest)

```bash
cd services/telemetry-frontend
npm run test:coverage
open coverage/index.html
```

### End-to-End Tests

E2E tests validate the complete pipeline.

```bash
# Start all services
docker-compose up -d

# Wait for services to be healthy
sleep 10

# Run E2E tests
cd tests/e2e
pip install -r requirements.txt
pytest test_pipeline.py -v

# Stop services
docker-compose down
```

### CI/CD Testing

GitHub Actions automatically run tests on push/PR:

- **cpp-ci.yml**: C++ tests with multiple build types
- **python-ci.yml**: Python processor tests (3.10, 3.11, 3.12)
- **simulator-ci.yml**: Simulator tests
- **frontend-ci.yml**: Frontend tests (Node 18, 20)
- **e2e-tests.yml**: Full pipeline integration tests

**Coverage Requirements:**
- Minimum 50% line coverage enforced
- CI fails if coverage drops below threshold
- Coverage reports uploaded to Codecov

---

## Deployment

### Docker Compose (Development)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild service
docker-compose up -d --build telemetry-processor
```

### Docker Compose (Production)

```bash
# Use production compose file
docker-compose -f docker-compose.yml up -d

# Enable monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access Grafana: http://localhost:3001
# Access Prometheus: http://localhost:9090
```

### Kubernetes (Minikube)

#### Setup Minikube

```bash
# Install minikube
brew install minikube

# Start minikube
minikube start --cpus=4 --memory=8192

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
```

#### Deploy Services

```bash
cd deployment/kubernetes

# Create namespace
kubectl create namespace f1-telemetry

# Deploy services
kubectl apply -f telemetry-ingest/
kubectl apply -f telemetry-processor/
kubectl apply -f telemetry-frontend/

# Check status
kubectl get pods -n f1-telemetry

# View logs
kubectl logs -f -n f1-telemetry deployment/telemetry-ingest

# Access frontend
minikube service telemetry-frontend -n f1-telemetry
```

#### Port Forwarding for Development

```bash
# Forward WebSocket port
kubectl port-forward -n f1-telemetry svc/telemetry-processor 8765:8765

# Forward frontend
kubectl port-forward -n f1-telemetry svc/telemetry-frontend 3000:80

# Forward ZMQ (for debugging)
kubectl port-forward -n f1-telemetry svc/telemetry-ingest 5555:5555
```

### Kubernetes (Production Cluster)

```bash
# Deploy to production cluster
kubectl config use-context production-cluster
kubectl apply -k deployment/kubernetes/overlays/production/

# Monitor deployment
kubectl rollout status deployment/telemetry-processor -n f1-telemetry

# Scale services
kubectl scale deployment/telemetry-processor --replicas=3 -n f1-telemetry
```

---

## Troubleshooting

### Common Issues

#### 1. UDP Packets Not Received

**Symptoms:** Ingest service starts but no telemetry data

**Solutions:**
```bash
# Check if port 20777 is available
netstat -an | grep 20777

# Test with simulator
docker-compose -f docker-compose.simulator.yml up telemetry-simulator

# Check firewall
sudo ufw allow 20777/udp

# Verify F1 game settings
# Telemetry: UDP, Port: 20777, IP: 127.0.0.1 or Docker host IP
```

#### 2. ZMQ Connection Failed

**Symptoms:** Processor can't connect to ingest service

**Solutions:**
```bash
# Check ZMQ port
docker-compose exec telemetry-ingest netstat -an | grep 5555

# Check container networking
docker-compose exec telemetry-processor ping telemetry-ingest

# View ingest logs
docker-compose logs telemetry-ingest

# Restart services in order
docker-compose restart telemetry-ingest
docker-compose restart telemetry-processor
```

#### 3. WebSocket Connection Failed

**Symptoms:** Frontend shows "Disconnected"

**Solutions:**
```bash
# Check processor WebSocket server
docker-compose logs telemetry-processor | grep "WebSocket"

# Test WebSocket connectivity
wscat -c ws://localhost:8765

# Check browser console for errors
# Verify WEBSOCKET_URL environment variable
docker-compose exec telemetry-frontend env | grep VITE_WEBSOCKET_URL

# Update docker-compose.yml if needed:
# environment:
#   - VITE_WEBSOCKET_URL=ws://telemetry-processor:8765
```

#### 4. Build Failures

**C++ Build Issues:**
```bash
# Clean build directory
cd services/telemetry-ingest
rm -rf build
cmake --preset=default
cmake --build build

# Install missing dependencies
sudo apt-get install libzmq3-dev libgtest-dev
```

**Python Dependency Issues:**
```bash
# Recreate virtual environment
cd services/telemetry-processor
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Frontend Build Issues:**
```bash
# Clear cache and reinstall
cd services/telemetry-frontend
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite
npm run build
```

#### 5. Test Failures

```bash
# Run tests with verbose output
pytest tests/ -vv --tb=long

# Run specific test
pytest tests/test_zmq_client.py::TestZmqClient::test_connect_success -vv

# Debug test with pdb
pytest tests/ -vv --pdb

# Check test coverage
pytest tests/ --cov=. --cov-report=html
```

### Performance Optimization

#### High CPU Usage

```bash
# Check container resources
docker stats

# Limit CPU usage in docker-compose.yml
services:
  telemetry-processor:
    cpus: '0.5'
    mem_limit: 512M
```

#### Packet Loss

```bash
# Increase UDP buffer size (Linux)
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400

# Add to /etc/sysctl.conf for persistence
```

#### WebSocket Latency

```bash
# Enable WebSocket compression in processor
# Update websocket_server.py to use compression

# Reduce packet processing overhead
# Adjust frequency in simulator config.yaml
```

### Logging and Monitoring

```bash
# View all service logs
docker-compose logs -f

# View specific service
docker-compose logs -f telemetry-processor

# Export logs
docker-compose logs > logs/all-services.log

# Enable debug logging
# Update docker-compose.yml:
# environment:
#   - LOG_LEVEL=DEBUG
```

---

## Development Best Practices

### Code Style

- **C++**: Follow Google C++ Style Guide, use `clang-format`
- **Python**: Follow PEP 8, use `black` formatter
- **TypeScript**: Follow Airbnb style, use ESLint + Prettier

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-telemetry-packet

# Make changes and commit
git add .
git commit -m "feat: Add lap data packet parsing"

# Push and create PR
git push origin feature/new-telemetry-packet
```

### Commit Messages

Follow Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Maintenance

### Testing Requirements

- All new features must have tests
- Maintain >= 50% code coverage
- E2E tests for major features
- Update tests before merging

---

## Resources

### Documentation

- [F1 Telemetry UDP Specification](docs/telemetry-fields.md)
- [ZeroMQ Guide](https://zguide.zeromq.org/)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [React Documentation](https://react.dev/)

### Tools

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [DevPod](https://devpod.sh/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

### Community

- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas
- Pull Requests: Contribute code improvements

---

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

## Support

For questions or issues:

1. Check this development guide
2. Search existing GitHub issues
3. Create a new issue with detailed information
4. Join discussions for general questions

Happy coding! 🏎️💨
