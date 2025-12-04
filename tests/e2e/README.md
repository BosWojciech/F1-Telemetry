# E2E Integration Tests

End-to-end tests for the complete F1 telemetry pipeline.

## Test Coverage

### Data Flow Tests
- `test_simulator_to_ingest_udp`: UDP packet transmission
- `test_ingest_to_processor_zmq`: ZMQ publish/subscribe
- `test_processor_to_frontend_websocket`: WebSocket delivery
- `test_complete_pipeline_e2e`: Full pipeline validation

### Performance Tests
- `test_high_frequency_data_flow`: 20Hz telemetry handling
- `test_packet_data_integrity`: Data structure validation

## Running Tests

### Prerequisites
All services must be running:
```bash
docker-compose up -d
```

### Run Tests
```bash
cd tests/e2e
pip install -r requirements.txt
pytest test_pipeline.py -v
```

### Run with Coverage
```bash
pytest test_pipeline.py -v --cov=. --cov-report=html
```

## Test Requirements

- All services healthy and accessible
- Ports available: 20777 (UDP), 5555 (ZMQ), 8765 (WebSocket)
- Network connectivity between containers

## Skipped Tests

Tests will skip gracefully if services are not running, with clear messages indicating which service is unavailable.
