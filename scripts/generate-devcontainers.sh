#!/bin/bash

# Script to auto-generate .devcontainer/devcontainer.json for each service
# based on detected programming language

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICES_DIR="$PROJECT_ROOT/services"

echo "=== F1 Telemetry Dev Container Generator ==="
echo "Project root: $PROJECT_ROOT"
echo "Services directory: $SERVICES_DIR"
echo

# Function to detect language and return image + extension
detect_language() {
    local service_dir="$1"
    
    if [ -f "$service_dir/go.mod" ]; then
        echo "go|mcr.microsoft.com/devcontainers/go:latest|golang.go"
    elif [ -f "$service_dir/package.json" ]; then
        echo "node|mcr.microsoft.com/devcontainers/javascript-node:latest|dbaeumer.vscode-eslint"
    elif [ -f "$service_dir/CMakeLists.txt" ] || [ -f "$service_dir/*.cpp" ]; then
        echo "cpp|mcr.microsoft.com/devcontainers/cpp:latest|ms-vscode.cpptools"
    elif [ -f "$service_dir/requirements.txt" ] || [ -f "$service_dir/pyproject.toml" ]; then
        echo "python|mcr.microsoft.com/devcontainers/python:latest|ms-python.python"
    else
        echo "unknown|mcr.microsoft.com/devcontainers/base:ubuntu|ms-azuretools.vscode-docker"
    fi
}

# Create root devcontainer if it doesn't exist
create_root_devcontainer() {
    local root_devcontainer="$PROJECT_ROOT/.devcontainer"
    local root_config="$root_devcontainer/devcontainer.json"
    
    if [ ! -d "$root_devcontainer" ]; then
        mkdir -p "$root_devcontainer"
        echo "Created root .devcontainer directory"
    fi
    
    cat > "$root_config" << 'EOF'
{
  "name": "F1 Telemetry: Monorepo",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {}
  },
  "workspaceFolder": "/workspaces/f1-telemetry",
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/f1-telemetry,type=bind",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools"
      ]
    }
  },
  "remoteUser": "vscode"
}
EOF
    echo "✓ Root devcontainer created: $root_config"
}

# Create service devcontainers
create_service_devcontainer() {
    local service_name="$1"
    local service_dir="$SERVICES_DIR/$service_name"
    local devcontainer_dir="$service_dir/.devcontainer"
    local devcontainer_config="$devcontainer_dir/devcontainer.json"
    
    if [ ! -d "$service_dir" ]; then
        echo "⚠ Service directory not found: $service_dir"
        return
    fi
    
    # Detect language
    local detection=$(detect_language "$service_dir")
    local language=$(echo "$detection" | cut -d'|' -f1)
    local image=$(echo "$detection" | cut -d'|' -f2)
    local extension=$(echo "$detection" | cut -d'|' -f3)
    
    echo "  Language detected: $language"
    echo "  Base image: $image"
    echo "  Extension: $extension"
    
    # Create .devcontainer directory
    if [ ! -d "$devcontainer_dir" ]; then
        mkdir -p "$devcontainer_dir"
    fi
    
    # Create the devcontainer.json
    cat > "$devcontainer_config" << EOF
{
  "name": "F1 Telemetry: $service_name",
  "image": "$image",
  "workspaceFolder": "/workspaces/f1-telemetry/services/$service_name",
  "workspaceMount": "source=\${localWorkspaceFolder}/../../,target=/workspaces/f1-telemetry,type=bind",
  "customizations": {
    "vscode": {
      "extensions": [
        "$extension",
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools"
      ]
    }
  },
  "remoteUser": "vscode"
}
EOF
    echo "✓ Service devcontainer created: $devcontainer_config"
}

# Main execution
echo "Creating root devcontainer..."
create_root_devcontainer
echo

echo "Scanning services and creating devcontainers..."
if [ ! -d "$SERVICES_DIR" ]; then
    echo "Error: Services directory not found at $SERVICES_DIR"
    exit 1
fi

for service_dir in "$SERVICES_DIR"/*; do
    if [ -d "$service_dir" ]; then
        service_name=$(basename "$service_dir")
        echo "Processing: $service_name"
        create_service_devcontainer "$service_name"
        echo
    fi
done

echo "=== Generation Complete ==="
echo "Next steps:"
echo "  1. Review generated .devcontainer/devcontainer.json files"
echo "  2. Run 'make dev-<service>' to open a service in its devcontainer"
echo "  3. Commit changes to version control"
