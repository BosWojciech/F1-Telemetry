# F1 Telemetry Simulator

Python-based UDP packet simulator for testing the F1 Telemetry System without the actual F1 game.

## Overview

This service simulates realistic F1 game telemetry packets, allowing you to test and develop the telemetry pipeline without needing the F1 game running. Perfect for:

- **Development**: Test your changes without launching the game
- **CI/CD**: Automated testing in pipelines
- **Demonstrations**: Show the system working without game dependency
- **Load Testing**: Generate high-frequency packet streams

## Features

- ✅ **Configurable packet generation** via JSON
- ✅ **Multiple packet types** (Session, Lap, Telemetry, Status, etc.)
- ✅ **Adjustable frequency** per packet type
- ✅ **Realistic data ranges** matching F1 game format
- ✅ **UDP transmission** to telemetry-ingest service
- ✅ **Easy configuration** for different scenarios

## Quick Start

### Using Docker Compose

```bash
# Start simulator with other services
docker-compose up telemetry-simulator

# Or in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up telemetry-simulator
```

### Local Development

```bash
# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run simulator
python simulator.py --config config/race_simulation.json

# Or with quick test config
python simulator.py --config config/test_simulation.json
```

## Configuration

### Configuration Files

Located in `config/` directory:

- `race_simulation.json` - Full race simulation (realistic frequencies)
- `test_simulation.json` - Quick testing (higher frequencies)

### Configuration Format

```json
{
    "description": "Simulation description",
    "mode": "race",
    "target_host": "telemetry-ingest",
    "target_port": 20777,
    "packet_format": 2023,
    
    "packet_types": {
        "SessionData": {
            "enabled": true,
            "frequency_hz": 2,
            "weather": 0,
            "track_temperature": 32,
            "air_temperature": 24
        },
        "LapData": {
            "enabled": true,
            "frequency_hz": 10
        },
        "CarTelemetry": {
            "enabled": true,
            "frequency_hz": 20
        }
    }
}
```

### Packet Types

| Packet Type | Description | Typical Frequency |
|-------------|-------------|-------------------|
| Motion | Car position, velocity, acceleration | 60 Hz |
| SessionData | Weather, track status, session info | 2 Hz |
| LapData | Lap times, sectors, positions | 10 Hz |
| CarTelemetry | Speed, throttle, brake, RPM | 20 Hz |
| CarStatus | Fuel, tyres, DRS, ERS | 5 Hz |
| Participants | Driver names and IDs | 1 Hz |

## Usage

### Command Line Options

```bash
python simulator.py --help

Options:
  --config PATH        Configuration file path (default: config/race_simulation.json)
  --target-host HOST   Override target host
  --target-port PORT   Override target port
```

### Examples

```bash
# Use race simulation
python simulator.py --config config/race_simulation.json

# Use test configuration with custom target
python simulator.py --config config/test_simulation.json --target-host localhost

# Quick test on custom port
python simulator.py --target-port 20778
```

## Development

### Dev Container

Open this directory in VS Code with the Dev Containers extension for a fully configured development environment.

### Testing Locally

```bash
# Terminal 1: Start telemetry-ingest service
cd ../../
docker-compose up telemetry-ingest

# Terminal 2: Run simulator
cd services/telemetry-simulator
python simulator.py --target-host localhost
```

### Creating Custom Scenarios

Create new JSON config files in the `config/` directory:

```json
{
    "description": "Qualifying simulation",
    "mode": "qualifying",
    "packet_types": {
        "LapData": {
            "enabled": true,
            "frequency_hz": 20
        }
    }
}
```

## Architecture

```
Simulator → UDP Packets → Telemetry Ingest → ZeroMQ → Processor → WebSocket → Frontend
```

The simulator replaces the F1 game in the data flow:

```
┌─────────────────────┐
│  Telemetry          │
│  Simulator          │
│  (This Service)     │
└──────────┬──────────┘
           │ UDP:20777
           ▼
┌─────────────────────┐
│  Telemetry Ingest   │
│  (C++ Service)      │
└──────────┬──────────┘
           │ ZeroMQ
           ▼
    (Rest of pipeline)
```

## Packet Format

Follows F1 2023/2024 UDP telemetry specification:

- **Header**: Common to all packets (packet type, session info, timing)
- **Data**: Packet-specific payload
- **Format**: Binary (struct-packed)

## Performance

- **Packet Rate**: Up to 60 Hz per type
- **Total Rate**: 100+ packets/second
- **Network**: UDP (no overhead)
- **CPU**: < 5% utilization

## Troubleshooting

### Simulator starts but no data in dashboard

1. Check telemetry-ingest is running:
   ```bash
   docker-compose ps telemetry-ingest
   ```

2. Verify network connectivity:
   ```bash
   docker-compose exec telemetry-simulator ping telemetry-ingest
   ```

3. Check logs:
   ```bash
   docker-compose logs telemetry-simulator
   docker-compose logs telemetry-ingest
   ```

### Wrong target host/port

Override in command:
```bash
python simulator.py --target-host localhost --target-port 20777
```

Or update config file.

## Future Enhancements

- [ ] Replay mode from recorded telemetry files
- [ ] Interactive mode with keyboard controls
- [ ] Race event simulation (crashes, safety car, etc.)
- [ ] Multi-lap progression
- [ ] Tire degradation simulation
- [ ] Fuel consumption modeling

## Contributing

To add new packet types:

1. Add packet type to configuration
2. Implement `_generate_<type>_packet()` in `packet_generator.py`
3. Follow F1 UDP specification format
4. Test with telemetry-ingest service

## License

MIT License - see root LICENSE file
