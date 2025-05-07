cmake_minimum_required(VERSION 3.10.0)
project(f1telemetry VERSION 0.1.0 LANGUAGES C CXX)

add_executable(f1telemetry src/main.cpp)

target_sources(f1telemetry PRIVATE src/udpClient.cpp)