#!/bin/bash

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build directory
BUILD_DIR="build"

# Function to display messages
print_message() {
    echo -e "${BLUE}[F1-Telemetry]${NC} $1"
}

# Function to display errors
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display success messages
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if build directory exists, create if not
if [ ! -d "$BUILD_DIR" ]; then
    print_message "Creating build directory..."
    mkdir -p "$BUILD_DIR"
    if [ $? -ne 0 ]; then
        print_error "Failed to create build directory."
        exit 1
    fi
fi

# Navigate to build directory
cd "$BUILD_DIR"

# Configure with CMake
print_message "Configuring project with CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Debug
if [ $? -ne 0 ]; then
    print_error "CMake configuration failed."
    exit 1
fi

# Build the project
print_message "Building project..."
cmake --build . -- -j$(nproc)
if [ $? -ne 0 ]; then
    print_error "Build failed."
    exit 1
fi

print_success "Build completed successfully!"

# Check if executable exists
if [ ! -f "bin/f1telemetry" ]; then
    print_error "Executable not found."
    exit 1
fi

# Run the application
print_message "Running F1 Telemetry application..."
echo -e "${YELLOW}---------- APPLICATION OUTPUT ----------${NC}"
./bin/f1telemetry
EXIT_CODE=$?
echo -e "${YELLOW}---------- END OF OUTPUT ----------${NC}"

if [ $EXIT_CODE -eq 0 ]; then
    print_success "Application executed successfully (exit code: 0)"
else
    print_error "Application exited with code: $EXIT_CODE"
fi

exit $EXIT_CODE