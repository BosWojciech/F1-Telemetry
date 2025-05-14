# F1-Telemetry

## Overview
A modular, multi-layer telemetry pipeline built to ingest, process, and visualize real-time F1 game data.
Originally designed for F1 23, the system will be version-aware. It is built with extensibility in mind — capable of supporting future editions.

## Project Architecture
The system is composed of three distinct layers, each handling a critical role in the data lifecycle: from raw binary packets to a rich web-based telemetry dashboard.

### Layer1 - C++ Data Ingestion & Processing

Directory: /Layer1

- Listens to the F1 game’s UDP telemetry stream.
- Parses and validates raw packets into strongly typed C++ structs (DataTypes.h).
- Extracts relevant data and converts it to structured JSON using nlohmann::json.
- Translates numeric values into human-readable form using F1-specific lookup tables (DataMaps.h).
- Forwards cleaned data to the Python layer over ZeroMQ.



## Layer2 - Python Middleware (Router & Collector)

Directory: /Layer2 (coming soon)

- Subscribes to telemetry data via ZeroMQ.
- Runs in two operational modes:
    - Pass-through Mode: Forwards data to frontend via WebSocket in real-time.
    - Data Collection Mode: Deduplicates and stores meaningful state changes for ML and analysis.
- Manages time-series logging (InfluxDB) and structured logs (Graylog).
- Version-aware and schema-flexible.
- Checks for data difference, and forwards only new data
- Sends JSON through WebSockets to last layer

## Layer3 - Web Frontend (React + Redux + Typescript)

Directory: /Layer3 (coming soon)

- Built with React, TypeScript, and Redux.
- Receives data via WebSocket and renders it in real-time.
- Dashboards simulate an F1-style driver MFD and session overview.
- Supports various telemetry components such as:
    - Lap timings
    - Sector data
    - Weather and track conditions
    - Driver positioning and events
    - more coming soon


## Contributors

Wojciech Bos [Github](https://github.com/BosWojciech) [LinkedIn](https://www.linkedin.com/in/wbos/):
- Data Pipeline Design/Architecture
- Layer 1 development
