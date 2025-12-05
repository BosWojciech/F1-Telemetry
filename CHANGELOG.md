# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete microservices architecture restructure
- Docker containerization for all services
- Dev container configurations for each service
- CI/CD pipelines with GitHub Actions
- Monitoring stack (Prometheus, Grafana, Loki)
- Comprehensive documentation
- Security scanning with Trivy
- Multi-stage Docker builds
- Development and production Docker Compose configurations
- Makefile for convenient operations

### Changed
- Restructured repository into `services/` directory
- Renamed Layer1 to `telemetry-ingest`
- Renamed Layer2 to `telemetry-processor`
- Renamed Layer3 to `telemetry-frontend`
- Updated all build configurations
- Improved logging with structured logs
- Enhanced error handling

### Planned
- Migration from ZeroMQ to Kafka
- Prometheus metrics exporters
- InfluxDB integration
- Unit and integration tests
- Kubernetes deployment manifests

## [1.0.0] - 2025-12-04

### Added
- Initial release with three-layer architecture
- C++ UDP telemetry ingest
- Python middleware processor
- React frontend dashboard
- ZeroMQ communication layer
- Basic WebSocket streaming
- F1 23 telemetry support

---

[Unreleased]: https://github.com/BosWojciech/F1-Telemetry/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/BosWojciech/F1-Telemetry/releases/tag/v1.0.0
