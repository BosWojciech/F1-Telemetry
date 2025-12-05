# Quick Start Guide

Get the F1 Telemetry System up and running in minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Docker Desktop installed (24.0+)
- ✅ At least 2GB free RAM
- ✅ 5GB free disk space
- ✅ F1 game installed (F1 23 or F1 24)

## Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/BosWojciech/F1-Telemetry.git
cd F1-Telemetry

# Run migration script (if coming from old structure)
./scripts/migrate.sh

# Initialize environment
cp .env.example .env
```

## Step 2: Start Services

### Option A: Quick Start (Production Mode)

```bash
make quickstart
```

This will:
- Build all Docker images
- Start all services
- Configure networking

### Option B: Development Mode

```bash
make dev-quickstart
```

This will:
- Build development images
- Enable hot-reloading
- Start debuggers
- Mount source code volumes

## Step 3: Configure F1 Game

1. **Launch your F1 game**
2. **Navigate to**: Settings → Telemetry Settings
3. **Configure**:
   - UDP Telemetry: **ON**
   - UDP Port: **20777**
   - UDP Format: **2023** or **2024**
   - UDP Send Rate: **Maximum**
   - IP Address: **127.0.0.1** (if running locally)

## Step 4: Access Dashboard

Open your browser and navigate to:

**Production Mode**: http://localhost:3000  
**Development Mode**: http://localhost:5173

You should see the F1 telemetry dashboard!

## Step 5: Verify Everything Works

```bash
# Check service health
make health

# View logs
make logs

# Expected output:
# ✓ telemetry-ingest    healthy
# ✓ telemetry-processor healthy
# ✓ telemetry-frontend  healthy
```

## Troubleshooting

### No Data Showing?

1. **Check F1 game UDP settings** - ensure UDP is enabled on port 20777
2. **Check ingest service logs**:
   ```bash
   make logs-ingest
   ```
3. **Verify network**:
   ```bash
   # On Mac/Linux, check UDP packets are being received
   nc -ul 20777
   ```

### Services Not Starting?

```bash
# View specific service logs
make logs-ingest
make logs-processor
make logs-frontend

# Restart services
make restart
```

### WebSocket Connection Failed?

1. Check processor service is running:
   ```bash
   docker-compose ps telemetry-processor
   ```
2. Verify WebSocket URL in browser console
3. Check firewall isn't blocking port 8765

## Next Steps

### Explore Features

- **Real-time telemetry**: Watch data stream as you drive
- **Session info**: Track lap times, weather, tire wear
- **Race events**: See overtakes, penalties, DRS status
- **MFD Display**: F1-style multi-function display

### Enable Monitoring

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
open http://localhost:3001
# Login: admin / admin
```

### Development

Want to modify or extend the system?

1. **Open a service in VS Code**:
   ```bash
   code services/telemetry-processor
   ```

2. **Reopen in Dev Container** (F1 → "Dev Containers: Reopen in Container")

3. **Start coding!** All dependencies are pre-installed

### Join the Community

- ⭐ Star the repository
- 📖 Read the [full documentation](./docs)
- 🐛 Report bugs via [Issues](https://github.com/BosWojciech/F1-Telemetry/issues)
- 💡 Suggest features via [Discussions](https://github.com/BosWojciech/F1-Telemetry/discussions)

## Common Commands

```bash
make help              # Show all commands
make up                # Start services
make down              # Stop services
make restart           # Restart services
make logs              # View logs
make health            # Check health
make clean             # Clean up everything
```

## Getting Help

- 📚 [Full Documentation](./docs)
- 🏗️ [Architecture Guide](./docs/ARCHITECTURE.md)
- 🚀 [Deployment Guide](./docs/DEPLOYMENT.md)
- 🤝 [Contributing Guide](./CONTRIBUTING.md)

## What's Next?

Now that you're up and running, check out:

1. **[Architecture Documentation](./docs/ARCHITECTURE.md)** - Understand how it all works
2. **[Deployment Guide](./docs/DEPLOYMENT.md)** - Production deployment tips
3. **[Contributing Guide](./CONTRIBUTING.md)** - Help improve the project

Happy racing! 🏎️💨
