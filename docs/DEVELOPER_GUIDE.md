# Developer Guide - Dev Containers & Kubernetes Integration

## Quick Start (TL;DR)

```bash
# 1. Set your environment variables (one time)
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"

# 2. Start a dev container
make dev-telemetry-frontend

# 3. VS Code opens with the dev container

# 4. View in k9s
k9s -n f1-telemetry-${USER}
```

---

## Overview

The F1 Telemetry project uses VS Code dev containers for local development, with integration into Kubernetes for pod and namespace organization. Each developer can:

1. **Pull the repo directly** to their laptop
2. **Define their Kubernetes namespace and pod** via environment variables
3. **Run specific dev containers** using Make commands
4. **See containers in k9s** identified by service name

No DevPod needed - just pure dev containers running in your K8s cluster.

---

## Setup

### Prerequisites

- **VS Code** with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Docker** running locally
- **kubectl** configured with your Kubernetes context
- **k9s** (optional, but recommended): `brew install derailed/k9s/k9s`

### Environment Configuration

Define where your containers will run by setting two environment variables:

```bash
# Option 1: Per-Developer Isolation (Recommended)
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"

# Option 2: Per-Branch Isolation
BRANCH=$(git rev-parse --abbrev-ref HEAD | tr '/' '-')
export K8S_NAMESPACE="f1-telemetry-${BRANCH}"
export K8S_POD_NAME="f1-telemetry-dev-${BRANCH}"

# Option 3: Shared Development
export K8S_NAMESPACE="f1-telemetry-dev"
export K8S_POD_NAME="f1-telemetry-dev"
```

**Persist your choice** by adding to `~/.bashrc` or `~/.zshrc`:

```bash
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"
```

Or create `.env.local` in the repo root (it's in `.gitignore`):

```bash
# .env.local
K8S_NAMESPACE="f1-telemetry-alice"
K8S_POD_NAME="f1-telemetry-dev-alice"
```

Then source it:
```bash
source .env.local
```

---

## Starting Dev Containers

Each service has its own dev container configuration in `.devcontainer/devcontainer.json`:

```bash
# Frontend (React + Node.js)
make dev-telemetry-frontend

# Ingest Service (C++)
make dev-telemetry-ingest

# Processor Service (Python)
make dev-telemetry-processor

# Simulator Service (Python)
make dev-telemetry-simulator
```

Each command:
1. Opens VS Code
2. Launches the service's dev container
3. Mounts the entire repo as `/workspaces/f1-telemetry`
4. Pre-installs all language-specific tools

---

## Container Architecture

### Pod Structure

When you run `make dev-*` commands, containers run in your Kubernetes pod:

```
Kubernetes Namespace: f1-telemetry-alice (your K8S_NAMESPACE)
│
└── Pod: f1-telemetry-dev-alice (your K8S_POD_NAME)
    ├── Container: telemetry-frontend     ← Named after service
    ├── Container: telemetry-ingest       ← Named after service
    ├── Container: telemetry-processor    ← Named after service
    └── Container: telemetry-simulator    ← Named after service
```

### Container Names

Containers are automatically named after their services for easy identification in k9s:

| Service | Container Name | Dev Command |
|---------|---|---|
| Frontend | `telemetry-frontend` | `make dev-telemetry-frontend` |
| Ingest | `telemetry-ingest` | `make dev-telemetry-ingest` |
| Processor | `telemetry-processor` | `make dev-telemetry-processor` |
| Simulator | `telemetry-simulator` | `make dev-telemetry-simulator` |

### Network Isolation

All containers in the same pod share:
- **Network namespace**: Can communicate via `localhost:<port>`
- **Volumes**: Access the same mounted repo
- **ConfigMaps**: Share environment variables (if configured)

**Example communication:**
```
Frontend → Processor: ws://localhost:8765
Ingest → Processor: tcp://localhost:5555 (ZMQ)
Simulator → Ingest: UDP localhost:20777
```

No Kubernetes service discovery needed - everything talks via localhost!

---

## Viewing in k9s

After starting dev containers, view them in k9s:

```bash
k9s -n f1-telemetry-${USER}
```

You'll see your pod with all containers:

```
NAMESPACE              NAME                              READY   STATUS
f1-telemetry-alice     f1-telemetry-dev-alice            4/4     Running
```

Select the pod to see all 4 named containers. Each is identifiable by service name.

---

## Customization Examples

### Example 1: Per-Developer Isolation

Each developer gets their own namespace and pod:

```bash
# In ~/.zshrc
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"
```

**Result:**
```
alice gets: f1-telemetry-alice
bob gets:   f1-telemetry-bob
eve gets:   f1-telemetry-eve

Each person's containers run independently!
```

### Example 2: Per-Feature-Branch Isolation

Each feature branch gets isolated environment:

```bash
# In a shell function or script
BRANCH=$(git rev-parse --abbrev-ref HEAD | tr '/' '-')
export K8S_NAMESPACE="f1-telemetry-${BRANCH}"
export K8S_POD_NAME="f1-telemetry-dev-${BRANCH}"
```

**Result:**
```
main                → f1-telemetry-main
feature/websocket   → f1-telemetry-feature-websocket
bugfix/zmq-crash    → f1-telemetry-bugfix-zmq-crash

Each branch has isolated containers!
```

### Example 3: Shared Development Environment

All developers work in the same namespace:

```bash
export K8S_NAMESPACE="f1-telemetry-dev"
export K8S_POD_NAME="f1-telemetry-dev"
```

**Result:**
```
Everyone shares: f1-telemetry-dev namespace
Useful for team debugging or collaborative development
```

---

## Dev Container Configuration

Each service has a `.devcontainer/devcontainer.json` file:

```
services/
├── telemetry-frontend/.devcontainer/devcontainer.json
├── telemetry-ingest/.devcontainer/devcontainer.json
├── telemetry-processor/.devcontainer/devcontainer.json
└── telemetry-simulator/.devcontainer/devcontainer.json
```

### Configuration Details

Each file specifies:
- **Base image**: Language-specific Docker image (Node.js, C++, Python, etc.)
- **Extensions**: VS Code extensions for that language
- **Tools**: Pre-installed development tools
- **Workspace**: Mounted path inside container
- **Environment**: Language-specific variables

Example:
```json
{
  "name": "telemetry-processor",
  "image": "mcr.microsoft.com/devcontainers/python:latest",
  "extensions": [
    "ms-python.python",
    "ms-python.debugpy"
  ],
  "workspaceFolder": "/workspaces/f1-telemetry/services/telemetry-processor"
}
```

---

## Workflow Examples

### Scenario 1: Single Service Development

```bash
# Start processor service
make dev-telemetry-processor

# VS Code opens with Python dev container
# Install dependencies: pip install -r requirements.txt
# Run: python main.py
# Debug: Set breakpoints in VS Code
```

### Scenario 2: Multi-Service Development

```bash
# Terminal 1: Start frontend
make dev-telemetry-frontend

# Terminal 2: Start processor
make dev-telemetry-processor

# Terminal 3: Monitor in k9s
k9s -n f1-telemetry-${USER}

# Both containers running in same pod
# Frontend connects to processor via localhost:8765
```

### Scenario 3: Integration Testing

```bash
# Start all services
make dev-telemetry-frontend &
make dev-telemetry-ingest &
make dev-telemetry-processor &
make dev-telemetry-simulator &

# All containers in same pod → can communicate
# Run integration tests
cd tests/e2e && pytest test_pipeline.py
```

---

## Troubleshooting

### Issue: Can't find containers in k9s

**Check:**
```bash
# Verify environment variables are set
echo $K8S_NAMESPACE
echo $K8S_POD_NAME

# Check if namespace exists
kubectl get namespace | grep f1-telemetry

# Check if pod is running
kubectl get pods -n f1-telemetry-${USER}
```

**Solution:**
```bash
# Ensure variables are exported before running make commands
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"

# Then start the container
make dev-telemetry-frontend
```

### Issue: Dev container won't start

**Check:**
```bash
# Verify Docker is running
docker ps

# Verify VS Code has Dev Containers extension
code --version

# Check container logs
docker logs <container-id>
```

**Solution:**
```bash
# Restart Docker
# Reinstall Dev Containers extension
# Check .devcontainer/devcontainer.json syntax
```

### Issue: Can't connect between containers

**Check:**
```bash
# Verify both containers are in same pod
kubectl describe pod f1-telemetry-dev-${USER} -n f1-telemetry-${USER}

# Test localhost connection from one container
kubectl exec -it f1-telemetry-dev-${USER} -c telemetry-frontend -- \
  curl http://localhost:8765
```

**Solution:**
```bash
# Both containers must be in same pod (same K8S_POD_NAME)
# Use localhost:<port> for communication
# Check service is actually listening on that port
```

### Issue: Namespace doesn't exist

**Check:**
```bash
kubectl get namespace | grep f1-telemetry
```

**Solution:**
```bash
# Create it manually
kubectl create namespace f1-telemetry-${USER}

# Or Kubernetes will create it when pod starts
kubectl create namespace f1-telemetry-${USER} --dry-run=client -o yaml | kubectl apply -f -
```

### Issue: Wrong namespace being used

**Check:**
```bash
# Verify which variables are set
printenv | grep K8S_

# Check Makefile (should not hardcode namespace)
grep -i namespace Makefile
```

**Solution:**
```bash
# Unset wrong variables
unset K8S_NAMESPACE K8S_POD_NAME

# Set correct ones
export K8S_NAMESPACE="f1-telemetry-${USER}"
export K8S_POD_NAME="f1-telemetry-dev-${USER}"

# Verify
echo $K8S_NAMESPACE
```

---

## Advanced Configuration

### Connecting to Remote Kubernetes Cluster

```bash
# Switch Kubernetes context
kubectl config use-context my-remote-cluster

# Set your environment for that cluster
export K8S_NAMESPACE="f1-telemetry-alice"
export K8S_POD_NAME="f1-telemetry-dev-alice"

# Start dev container (now runs on remote cluster)
make dev-telemetry-frontend
```

### Adding Custom Environment Variables

Create `.env.local`:
```bash
K8S_NAMESPACE="f1-telemetry-alice"
K8S_POD_NAME="f1-telemetry-dev-alice"
DEBUG="true"
LOG_LEVEL="debug"
```

Source it:
```bash
source .env.local
```

### Using Different Docker Registry

```bash
export DOCKER_REGISTRY="my-registry.com"
export DEVCONTAINER_IMAGE="${DOCKER_REGISTRY}/f1-telemetry-frontend"

# Dev container will use your custom image
make dev-telemetry-frontend
```

---

## Common Commands

### Starting Services
```bash
make dev-telemetry-frontend      # Start frontend
make dev-telemetry-ingest        # Start ingest
make dev-telemetry-processor     # Start processor
make dev-telemetry-simulator     # Start simulator
```

### Viewing
```bash
k9s -n f1-telemetry-${USER}                      # Browse pods/containers
kubectl get pods -n f1-telemetry-${USER}         # List pods
kubectl get namespace | grep f1-telemetry        # List namespaces
```

### Debugging
```bash
# Describe pod
kubectl describe pod f1-telemetry-dev-${USER} -n f1-telemetry-${USER}

# View logs
kubectl logs f1-telemetry-dev-${USER} -c telemetry-frontend -n f1-telemetry-${USER}

# Execute command in container
kubectl exec -it f1-telemetry-dev-${USER} -c telemetry-processor -n f1-telemetry-${USER} -- bash
```

### Cleanup
```bash
# Delete namespace (removes all pods)
kubectl delete namespace f1-telemetry-${USER}

# Delete specific pod
kubectl delete pod f1-telemetry-dev-${USER} -n f1-telemetry-${USER}
```

---

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [COMMANDS.md](COMMANDS.md) - All available commands
- [../DEVELOPMENT.md](../DEVELOPMENT.md) - Full development guide
- [../DEVCONTAINER_SETUP.md](../DEVCONTAINER_SETUP.md) - Dev container details

---

## Configuration Summary

| Aspect | Details |
|--------|---------|
| **Namespace Definition** | `K8S_NAMESPACE` environment variable |
| **Pod Name Definition** | `K8S_POD_NAME` environment variable |
| **Container Names** | Automatic: `telemetry-<service>` |
| **K8s Integration** | Full - containers run in your cluster |
| **Communication** | Via `localhost:<port>` (same pod) |
| **Customization** | Per-developer, per-branch, or shared |
| **Tools** | VS Code Dev Containers + kubectl + k9s |
| **Setup Time** | ~5 minutes (one-time environment setup) |

---

## Key Takeaways

✅ **Simple**: Just set 2 environment variables and run `make dev-*`  
✅ **K8s Native**: Containers run in your Kubernetes cluster  
✅ **Service Names**: Containers identified by service name in k9s  
✅ **Flexible**: Per-developer, per-branch, or shared options  
✅ **No DevPod**: Pure dev containers - simpler, lighter  
✅ **Isolated**: Each developer can have their own namespace  

---

**Ready to start?** Set your environment variables and run `make dev-telemetry-frontend`!
