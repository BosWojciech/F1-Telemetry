# Deployment Guide

## Prerequisites

- Docker Engine 24.0+
- Docker Compose 2.20+
- 2GB RAM minimum
- 5GB disk space
- Network access for F1 game UDP packets

## Quick Deployment

### 1. Clone Repository

```bash
git clone https://github.com/BosWojciech/F1-Telemetry.git
cd F1-Telemetry
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Deploy Services

```bash
# Production mode
make quickstart

# Development mode
make dev-quickstart
```

### 4. Verify Deployment

```bash
# Check service status
make health

# View logs
make logs
```

### 5. Access Services

- **Frontend**: http://localhost:3000
- **WebSocket**: ws://localhost:8765
- **Grafana**: http://localhost:3001 (optional monitoring)

## Production Deployment

### Docker Compose

#### Single Host Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Scale processor if needed
docker-compose up -d --scale telemetry-processor=3
```

#### Multi-Host Deployment (Docker Swarm)

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml f1-telemetry

# Check services
docker stack services f1-telemetry
```

### Kubernetes (Future)

Coming soon: Helm charts and Kubernetes manifests

## Configuration

### Environment Variables

Create `.env` file from template:

```bash
# Telemetry Ingest
UDP_LISTEN_PORT=20777
ZMQ_PUBLISHER_ENDPOINT=tcp://*:5555

# Telemetry Processor
ZMQ_SUBSCRIBER_ENDPOINT=tcp://telemetry-ingest:5555
WEBSOCKET_HOST=0.0.0.0
WEBSOCKET_PORT=8765
MODE=passthrough

# Frontend
VITE_WEBSOCKET_URL=ws://localhost:8765

# Logging
LOG_LEVEL=info
```

### Network Configuration

#### Port Mapping

| Service | Internal Port | External Port | Protocol |
|---------|---------------|---------------|----------|
| telemetry-ingest | 20777 | 20777 | UDP |
| telemetry-ingest | 5555 | - | TCP (internal) |
| telemetry-processor | 8765 | 8765 | TCP |
| telemetry-frontend | 80 | 3000 | TCP |

#### Firewall Rules

```bash
# Allow F1 game UDP
sudo ufw allow 20777/udp

# Allow WebSocket
sudo ufw allow 8765/tcp

# Allow Frontend
sudo ufw allow 3000/tcp
```

### F1 Game Configuration

1. **Launch F1 Game**
2. **Go to Settings → Telemetry**
3. **Set UDP Telemetry**: ON
4. **UDP Port**: 20777
5. **UDP Format**: 2023 or 2024
6. **UDP Send Rate**: Maximum
7. **IP Address**: 127.0.0.1 (if running locally)

## Monitoring Setup

### Deploy Monitoring Stack

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

### Access Monitoring

- **Grafana**: http://localhost:3001
  - Username: `admin`
  - Password: `admin`
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8080

## Troubleshooting

### Services Not Starting

```bash
# Check service logs
make logs

# Check service-specific logs
make logs-ingest
make logs-processor
make logs-frontend

# Check Docker
docker-compose ps
docker-compose logs
```

### No Telemetry Data

1. **Check F1 game settings** (UDP enabled, correct port)
2. **Check network connectivity**
   ```bash
   # Listen for UDP packets
   nc -ul 20777
   ```
3. **Check ingest service logs**
   ```bash
   make logs-ingest
   ```

### WebSocket Connection Failed

1. **Check processor service status**
   ```bash
   docker-compose ps telemetry-processor
   ```
2. **Verify WebSocket port** (8765)
   ```bash
   netstat -an | grep 8765
   ```
3. **Check frontend configuration** (VITE_WEBSOCKET_URL)

### High CPU/Memory Usage

```bash
# Check resource usage
docker stats

# Limit resources in docker-compose.yml
services:
  telemetry-processor:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Backup & Recovery

### Backup Data

```bash
# Backup volumes
docker run --rm \
  -v f1-telemetry-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz /data

# Backup configuration
cp .env .env.backup
```

### Restore Data

```bash
# Restore volumes
docker run --rm \
  -v f1-telemetry-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /
```

## Updates & Maintenance

### Update Services

```bash
# Pull latest images
docker-compose pull

# Recreate containers
docker-compose up -d

# Remove old images
docker image prune -a
```

### Health Checks

```bash
# Manual health check
make health

# Automated monitoring
# Configure alerts in Grafana
```

## Security Best Practices

1. **Change default passwords** (Grafana, etc.)
2. **Use reverse proxy** (Nginx, Traefik) with SSL
3. **Restrict network access** (firewall rules)
4. **Regular updates** (Docker, services, dependencies)
5. **Monitor logs** for suspicious activity
6. **Use secrets management** (not .env in production)

## Performance Tuning

### Optimize Docker

```bash
# Increase Docker resources
# Edit Docker Desktop → Resources

# Prune unused resources
docker system prune -a --volumes
```

### Optimize Services

- **Ingest**: Single-threaded, CPU-bound
- **Processor**: Multi-worker if needed
- **Frontend**: Use CDN for static assets

## Scaling

### Horizontal Scaling

```bash
# Scale processor service
docker-compose up -d --scale telemetry-processor=3

# Load balancing (future)
# Configure Nginx upstream
```

### Vertical Scaling

Update resource limits in `docker-compose.yml`

## Support

- **Documentation**: `/docs`
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
