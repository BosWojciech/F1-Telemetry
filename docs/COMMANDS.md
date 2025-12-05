# Command Reference

Quick reference for all available commands in the F1 Telemetry System.

## Make Commands

### Basic Operations

```bash
make help              # Show all available commands
make init              # Initialize project (.env from template)
make build             # Build all services
make up                # Start all services (production)
make down              # Stop all services
make restart           # Restart all services
make ps                # List running services
make health            # Check health status of all services
```

### Development

```bash
make dev-build         # Build development images
make dev-up            # Start services in development mode
make dev-down          # Stop development services
make dev-logs          # View development logs
make dev-quickstart    # Initialize + build + start (dev mode)
```

### Logs

```bash
make logs              # View logs from all services
make logs-ingest       # View telemetry-ingest logs
make logs-processor    # View telemetry-processor logs
make logs-frontend     # View telemetry-frontend logs
```

### Service Management

```bash
make restart-ingest    # Restart telemetry-ingest service
make restart-processor # Restart telemetry-processor service
make restart-frontend  # Restart telemetry-frontend service
```

### Shell Access

```bash
make shell-ingest      # Open shell in telemetry-ingest container
make shell-processor   # Open shell in telemetry-processor container
make shell-frontend    # Open shell in telemetry-frontend container
```

### Cleanup

```bash
make clean             # Remove containers, volumes, and images
make clean-volumes     # Remove all volumes (WARNING: deletes data)
make prune             # Remove all unused Docker resources
```

### Testing

```bash
make test              # Run tests for all services
```

### Quick Start

```bash
make quickstart        # Initialize + build + start (production)
```

## Docker Compose Commands

### Production

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f telemetry-processor

# Restart service
docker-compose restart telemetry-processor

# Scale service
docker-compose up -d --scale telemetry-processor=3

# Rebuild and restart
docker-compose up -d --build

# Remove everything including volumes
docker-compose down -v
```

### Development

```bash
# Start in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Stop development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# View development logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f
```

### Monitoring

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Stop monitoring stack
docker-compose -f docker-compose.monitoring.yml down

# Combined: services + monitoring
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

## Docker Commands

### Image Management

```bash
# List images
docker images

# Build specific service
docker build -t f1-telemetry-ingest services/telemetry-ingest

# Remove image
docker rmi f1-telemetry-ingest

# Pull images
docker-compose pull
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop f1-telemetry-ingest

# Remove container
docker rm f1-telemetry-ingest

# View container logs
docker logs f1-telemetry-processor

# Execute command in container
docker exec -it f1-telemetry-processor /bin/bash

# View container stats
docker stats
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect f1-telemetry-network

# Create network
docker network create f1-telemetry-network
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect f1-telemetry-data

# Remove volume
docker volume rm f1-telemetry-data

# Remove all unused volumes
docker volume prune
```

## Service-Specific Commands

### Telemetry Ingest (C++)

```bash
# Local build
cd services/telemetry-ingest
./build_and_run.sh

# CMake build
cmake --preset=default
cmake --build build --config Release
./build/telemetry-ingest

# Debug build
cmake --preset=debug
cmake --build build --config Debug
gdb ./build/telemetry-ingest
```

### Telemetry Processor (Python)

```bash
# Local setup
cd services/telemetry-processor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run service
python main.py --mode passthrough
python main.py --mode datacollection

# Run with debug logging
python main.py --mode passthrough --log-level DEBUG

# Run tests
pytest
pytest --cov=.

# Format code
black .

# Lint
flake8 .

# Type check
mypy .
```

### Telemetry Frontend (React)

```bash
# Local setup
cd services/telemetry-frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint

# Type check
npx tsc --noEmit
```

## Git Commands

```bash
# Clone repository
git clone https://github.com/BosWojciech/F1-Telemetry.git

# Create feature branch
git checkout -b feature/your-feature

# Stage changes
git add .

# Commit changes
git commit -m "feat: add new feature"

# Push changes
git push origin feature/your-feature

# Pull latest changes
git pull origin main
```

## Monitoring URLs

```bash
# Open in browser
open http://localhost:3000      # Frontend (Production)
open http://localhost:5173      # Frontend (Development)
open http://localhost:3001      # Grafana
open http://localhost:9090      # Prometheus
open http://localhost:8080      # cAdvisor
```

## Debugging

### Python (telemetry-processor)

```bash
# With debugpy
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py

# In VS Code, attach to port 5678
```

### C++ (telemetry-ingest)

```bash
# With GDB
gdb ./build/telemetry-ingest
(gdb) run
(gdb) backtrace

# With Valgrind
valgrind --leak-check=full ./build/telemetry-ingest
```

## Utility Commands

```bash
# Check if ports are in use
lsof -i :20777  # F1 UDP
lsof -i :5555   # ZeroMQ
lsof -i :8765   # WebSocket
lsof -i :3000   # Frontend

# Monitor UDP packets
nc -ul 20777

# Test WebSocket connection
wscat -c ws://localhost:8765

# Check Docker disk usage
docker system df

# View Docker events
docker events

# Export Docker images
docker save f1-telemetry-ingest -o ingest.tar
docker load -i ingest.tar
```

## Environment Variables

```bash
# View current environment
docker-compose config

# Override environment variable
UDP_LISTEN_PORT=20777 docker-compose up -d

# Use different .env file
docker-compose --env-file .env.production up -d
```

## Shortcuts

```bash
# Quick restart everything
make down && make up

# Rebuild and restart specific service
docker-compose up -d --build telemetry-processor

# View logs from last 100 lines
docker-compose logs --tail=100 -f

# Remove everything and start fresh
make clean && make quickstart

# Development with monitoring
make dev-up && docker-compose -f docker-compose.monitoring.yml up -d
```

## Pro Tips

```bash
# Alias for quick access (add to ~/.zshrc or ~/.bashrc)
alias f1-start="cd ~/path/to/F1-Telemetry && make up"
alias f1-stop="cd ~/path/to/F1-Telemetry && make down"
alias f1-logs="cd ~/path/to/F1-Telemetry && make logs"
alias f1-health="cd ~/path/to/F1-Telemetry && make health"

# Watch mode for logs
watch -n 1 'docker-compose ps'

# Follow multiple service logs
docker-compose logs -f telemetry-ingest telemetry-processor

# Format JSON logs
docker-compose logs telemetry-processor | jq .

# Export logs to file
docker-compose logs > logs-$(date +%Y%m%d).txt
```

---

For more information, see:
- [Quick Start Guide](./QUICKSTART.md)
- [Architecture Documentation](./ARCHITECTURE.md)
- [Deployment Guide](./DEPLOYMENT.md)
