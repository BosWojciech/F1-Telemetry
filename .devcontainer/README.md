Per-service Dev Containers

This repository exposes per-service dev container configurations under services/*/.devcontainer.

How to use

- Open the service folder you want to work on in VS Code (for example: services/telemetry-processor).
- When prompted, choose "Reopen in Container". Each service's devcontainer is configured to build from that service's Dockerfile and attach the workspace.
- To run multiple services together for integrated development, use Docker Compose from the repository root:

  docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

Notes

- Dev containers are configured to join the f1-telemetry-network (docker-compose.yml) instead of using host networking, which works better in DevPod / Kubernetes environments.
- If your environment requires host networking (some UDP workflows), consult the README or adjust the service devcontainer runArgs accordingly.
