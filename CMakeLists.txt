cmake_minimum_required(VERSION 3.10.0)
project(f1telemetry VERSION 0.1.0 LANGUAGES C CXX)

# Add executable
add_executable(f1telemetry
    src/main.cpp
    src/core/TelemetryProcessor.cpp
    src/network/udpClient.cpp
)

# Include directories for header files
target_include_directories(f1telemetry PRIVATE include)
