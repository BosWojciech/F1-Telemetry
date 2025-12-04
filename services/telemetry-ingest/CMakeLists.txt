cmake_minimum_required(VERSION 3.20)

project(f1-telemetry-ingest
    VERSION 1.0.0
    DESCRIPTION "F1 Telemetry UDP Ingest Service"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -pedantic")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Find required packages
find_package(Threads REQUIRED)

# ZeroMQ
find_path(ZMQ_INCLUDE_DIR zmq.h)
find_library(ZMQ_LIBRARY NAMES zmq)

if(NOT ZMQ_INCLUDE_DIR OR NOT ZMQ_LIBRARY)
    message(FATAL_ERROR "ZeroMQ not found. Please install libzmq3-dev")
endif()

# Include directories
include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${ZMQ_INCLUDE_DIR}
)

# Source files
file(GLOB_RECURSE SOURCES
    ${PROJECT_SOURCE_DIR}/src/*.cpp
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Link libraries
target_link_libraries(${PROJECT_NAME}
    PRIVATE
    Threads::Threads
    ${ZMQ_LIBRARY}
)

# Set output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
    OUTPUT_NAME telemetry-ingest
)

# Installation
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

# Print configuration
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "ZeroMQ include: ${ZMQ_INCLUDE_DIR}")
message(STATUS "ZeroMQ library: ${ZMQ_LIBRARY}")

# ============================================
# Testing Configuration
# ============================================
option(BUILD_TESTS "Build unit tests" ON)

if(BUILD_TESTS)
    enable_testing()
    
    # Find Google Test
    find_package(GTest REQUIRED)
    include(GoogleTest)
    
    # Source files for library (exclude main.cpp)
    file(GLOB_RECURSE LIB_SOURCES
        ${PROJECT_SOURCE_DIR}/src/core/*.cpp
        ${PROJECT_SOURCE_DIR}/src/network/*.cpp
    )
    
    # Create library from source files (needed for testing)
    add_library(${PROJECT_NAME}_lib STATIC ${LIB_SOURCES})
    target_link_libraries(${PROJECT_NAME}_lib
        PUBLIC
        Threads::Threads
        ${ZMQ_LIBRARY}
    )
    target_include_directories(${PROJECT_NAME}_lib
        PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${ZMQ_INCLUDE_DIR}
    )
    
    # Test files
    file(GLOB TEST_SOURCES ${PROJECT_SOURCE_DIR}/tests/*.cpp)
    
    # Create test executable
    add_executable(${PROJECT_NAME}_tests ${TEST_SOURCES})
    target_link_libraries(${PROJECT_NAME}_tests
        PRIVATE
        ${PROJECT_NAME}_lib
        GTest::gtest
        GTest::gtest_main
    )
    
    # Discover and register tests
    gtest_discover_tests(${PROJECT_NAME}_tests)
    
    # Set output directory for tests
    set_target_properties(${PROJECT_NAME}_tests PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests
    )
    
    message(STATUS "Testing enabled - Google Test found")
endif()
