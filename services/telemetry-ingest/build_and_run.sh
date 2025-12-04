#!/bin/bash
set -e

echo "Building F1 Telemetry Ingest Service..."

# Create build directory
mkdir -p build
cd build

# Configure with CMake
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(nproc)

echo "Build complete! Binary: ./build/telemetry-ingest"
echo ""
echo "To run the service:"
echo "  ./build/telemetry-ingest"
