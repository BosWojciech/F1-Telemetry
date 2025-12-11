# Complete Migration TODO: ZeroMQ/JSON → Kafka/Protobuf

> **Status**: Ready for Implementation  
> **Estimated Effort**: 30-40 hours  
> **Priority Order**: Phase 1 → Phase 2 → Phase 3 → Phase 4

---

## Table of Contents
1. [Current State Analysis](#current-state-analysis)
2. [Phase 1: Infrastructure & Protobuf Setup](#phase-1-infrastructure--protobuf-setup)
3. [Phase 2: C++ Telemetry Ingest Service](#phase-2-c-telemetry-ingest-service)
4. [Phase 3: Python Telemetry Processor Service](#phase-3-python-telemetry-processor-service)
5. [Phase 4: Frontend & Testing](#phase-4-frontend--testing)
6. [Phase 5: Cleanup & Optimization](#phase-5-cleanup--optimization)

---

## Current State Analysis

### 🔍 What Each Service Currently Does

#### **telemetry-ingest** (C++ Service)
**Current Flow:**
```
UDP:20777 (F1 Game) 
  → Parse binary packets (14 types)
  → Convert to JSON using TelemetryProcessor
  → Publish via ZeroMQ (tcp://*:5555)
```

**Key Files:**
- `src/main.cpp` - Main loop with packet type switch (14 cases)
- `src/core/TelemetryProcessor.cpp` - Converts binary structs → JSON (575 lines)
- `src/network/zmqPublisher.cpp` - ZMQ publisher implementation
- `include/core/DataTypes.h` - All F1 23 packet structs (593 lines)
- `include/core/DataMaps.h` - All enums/mappings (massive file)
- `CMakeLists.txt` - Links against libzmq

**Current Behavior:**
1. Receives UDP packets from F1 game
2. Validates packet size
3. Copies binary data to structs (`std::memcpy`)
4. Calls `TelemetryProcessor::process*` for each packet type
5. Uses `DataMaps.h` to convert enums to strings
6. Publishes JSON to ZMQ with topic = packet type name

#### **telemetry-processor** (Python Service)
**Current Flow:**
```
ZMQ Subscriber (tcp://telemetry-ingest:5555)
  → Receive JSON messages
  → Mode: passthrough or datacollection
  → Forward to WebSocket clients
```

**Key Files:**
- `main.py` - Main orchestrator (143 lines)
- `zmq_client/zmq_client.py` - ZMQ subscriber
- `websocket_server/websocket_server.py` - WebSocket broadcaster
- `requirements.txt` - Depends on pyzmq, websockets

**Current Behavior:**
1. Connects to ZMQ publisher from ingest service
2. Subscribes to all topics ('')
3. Receives `(topic, payload)` tuples
4. In passthrough mode: forwards directly to WebSocket
5. In datacollection mode: stores to data structure (future: DB)
6. WebSocket server runs in separate thread
7. Broadcasts to all connected WebSocket clients

#### **websocket-gateway** (NEW - NEEDS TO BE CREATED)
**Purpose:** Bridge Kafka → WebSocket (replacement for processor's WebSocket forwarding)
**Status:** ⚠️ Does not exist yet - must be created in Phase 3

#### **telemetry-frontend** (React/TypeScript)
**Current Flow:**
```
WebSocket (ws://localhost:8765)
  → Receive JSON telemetry
  → Parse and dispatch to Redux store
  → Render real-time dashboard
```

**Key Files:**
- `src/socket/socketService.ts` - WebSocket client (104 lines)
- Connects directly to processor's WebSocket server
- Parses JSON messages
- No changes needed (connects to gateway instead)

---

## Phase 1: Infrastructure & Protobuf Setup

**Goal:** Prepare build environment and compile protobuf schemas  
**Effort:** 2-3 hours  
**Dependencies:** None

### 1.1 Install System Dependencies

#### macOS
```bash
# Protocol Buffers compiler
brew install protobuf

# Kafka C++ client (librdkafka)
brew install librdkafka

# Verify installations
protoc --version  # Should be 3.20+
brew list librdkafka
```

#### Ubuntu/Debian
```bash
# Protocol Buffers
sudo apt-get update
sudo apt-get install -y protobuf-compiler libprotobuf-dev

# librdkafka
sudo apt-get install -y librdkafka-dev

# Verify
protoc --version
```

### 1.2 Compile Protocol Buffer Schemas

```bash
cd /path/to/F1-Telemetry

# Compile all protobuf schemas
./scripts/compile-protos.sh

# Verify generated files exist
ls services/telemetry-ingest/generated/
ls services/telemetry-processor/generated/
ls services/websocket-gateway/generated/
ls services/telemetry-frontend/src/generated/
```

**Expected Output:**
```
services/telemetry-ingest/generated/
  common/enums.pb.h, enums.pb.cc
  f1_23/telemetry.pb.h, telemetry.pb.cc
  kafka/messages.pb.h, messages.pb.cc

services/telemetry-processor/generated/
  common/enums_pb2.py, enums_pb2.pyi
  f1_23/telemetry_pb2.py, telemetry_pb2.pyi
  kafka/messages_pb2.py, messages_pb2.pyi
```

### 1.3 Start Kafka Infrastructure

```bash
# Start Kafka + Zookeeper + Kafka UI
docker-compose up -d zookeeper kafka kafka-ui

# Wait for startup (30 seconds)
sleep 30

# Verify Kafka is healthy
docker ps | grep kafka
docker logs f1-kafka --tail 50

# Access Kafka UI
open http://localhost:8080
```

**Verification Steps:**
- [ ] Kafka UI accessible at http://localhost:8080
- [ ] Topics can be created manually (test)
- [ ] No error logs in `docker logs f1-kafka`

### 1.4 Create Generated Code Directories

```bash
# Create .gitignore for generated code
cat > services/telemetry-ingest/generated/.gitignore << EOF
*
!.gitignore
EOF

cat > services/telemetry-processor/generated/.gitignore << EOF
*
!.gitignore
EOF

# Commit .gitignore files
git add services/**/generated/.gitignore
git commit -m "Add .gitignore for generated protobuf code"
```

---

## Phase 2: C++ Telemetry Ingest Service

**Goal:** Replace ZeroMQ → Kafka, JSON → Protobuf  
**Effort:** 12-16 hours  
**Priority:** HIGH

### 2.1 Update CMakeLists.txt Dependencies

**File:** `services/telemetry-ingest/CMakeLists.txt`

**Changes:**
1. Remove ZeroMQ dependency
2. Add librdkafka dependency
3. Add protobuf dependency
4. Include generated protobuf files in build

```cmake
# BEFORE (lines 26-31):
find_path(ZMQ_INCLUDE_DIR zmq.h)
find_library(ZMQ_LIBRARY NAMES zmq)
if(NOT ZMQ_INCLUDE_DIR OR NOT ZMQ_LIBRARY)
    message(FATAL_ERROR "ZeroMQ not found. Please install libzmq3-dev")
endif()

# AFTER:
# Protobuf
find_package(Protobuf REQUIRED)
if(NOT Protobuf_FOUND)
    message(FATAL_ERROR "Protobuf not found. Install: brew install protobuf")
endif()

# librdkafka
find_library(RDKAFKA_LIBRARY NAMES rdkafka++ rdkafkacpp)
find_path(RDKAFKA_INCLUDE_DIR librdkafka/rdkafkacpp.h)
if(NOT RDKAFKA_LIBRARY OR NOT RDKAFKA_INCLUDE_DIR)
    message(FATAL_ERROR "librdkafka not found. Install: brew install librdkafka")
endif()
```

```cmake
# Include directories - ADD:
include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/generated  # <-- ADD THIS
    ${Protobuf_INCLUDE_DIRS}         # <-- ADD THIS
    ${RDKAFKA_INCLUDE_DIR}           # <-- ADD THIS
)
```

```cmake
# Source files - UPDATE:
file(GLOB_RECURSE SOURCES
    ${PROJECT_SOURCE_DIR}/src/*.cpp
    ${PROJECT_SOURCE_DIR}/generated/**/*.cc  # <-- ADD THIS (protobuf generated)
)
```

```cmake
# Link libraries - UPDATE:
target_link_libraries(${PROJECT_NAME}
    PRIVATE
    Threads::Threads
    ${Protobuf_LIBRARIES}   # <-- ADD THIS
    ${RDKAFKA_LIBRARY}      # <-- ADD THIS
    # REMOVE: ${ZMQ_LIBRARY}
)
```

**Testing:**
```bash
cd services/telemetry-ingest
mkdir build && cd build
cmake ..
# Should configure without errors
```

### 2.2 Create KafkaProducer Class

**New File:** `services/telemetry-ingest/include/kafka/KafkaProducer.h`

```cpp
#ifndef KAFKA_PRODUCER_H
#define KAFKA_PRODUCER_H

#include <string>
#include <memory>
#include <librdkafka/rdkafkacpp.h>

namespace KafkaProducer {
    
    /**
     * @brief Initialize Kafka producer
     * @param brokers Comma-separated list of Kafka brokers (e.g., "kafka:29092")
     * @param clientId Unique client identifier
     */
    void initialize(const std::string& brokers, const std::string& clientId = "telemetry-ingest");
    
    /**
     * @brief Publish protobuf message to Kafka topic
     * @param topic Kafka topic name
     * @param key Message key (optional, use session UID or frame ID)
     * @param payload Serialized protobuf bytes
     * @param payloadSize Size of payload in bytes
     * @return true if published successfully
     */
    bool publish(
        const std::string& topic,
        const std::string& key,
        const char* payload,
        size_t payloadSize
    );
    
    /**
     * @brief Flush pending messages and cleanup
     */
    void shutdown();
    
    /**
     * @brief Get producer statistics
     */
    void printStats();

    // Delivery report callback
    class DeliveryReportCb : public RdKafka::DeliveryReportCb {
    public:
        void dr_cb(RdKafka::Message& message) override;
    };

    extern std::unique_ptr<RdKafka::Producer> producer;
    extern std::unique_ptr<DeliveryReportCb> deliveryCallback;
}

#endif // KAFKA_PRODUCER_H
```

**New File:** `services/telemetry-ingest/src/kafka/KafkaProducer.cpp`

```cpp
#include "kafka/KafkaProducer.h"
#include <iostream>
#include <chrono>
#include <thread>

namespace KafkaProducer {
    
    std::unique_ptr<RdKafka::Producer> producer = nullptr;
    std::unique_ptr<DeliveryReportCb> deliveryCallback = nullptr;
    
    void DeliveryReportCb::dr_cb(RdKafka::Message& message) {
        if (message.err() != RdKafka::ERR_NO_ERROR) {
            std::cerr << "[KAFKA] Delivery failed: " << message.errstr() << std::endl;
        } else {
            // Successful delivery (optional: log only errors in production)
            // std::cout << "[KAFKA] Message delivered to topic " << message.topic_name() << std::endl;
        }
    }
    
    void initialize(const std::string& brokers, const std::string& clientId) {
        std::cout << "[KAFKA] Initializing producer..." << std::endl;
        std::cout << "[KAFKA] Brokers: " << brokers << std::endl;
        
        std::string errstr;
        
        // Create configuration
        RdKafka::Conf* conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);
        
        // Set broker list
        if (conf->set("bootstrap.servers", brokers, errstr) != RdKafka::Conf::CONF_OK) {
            std::cerr << "[KAFKA] Failed to set bootstrap.servers: " << errstr << std::endl;
            exit(1);
        }
        
        // Set client ID
        if (conf->set("client.id", clientId, errstr) != RdKafka::Conf::CONF_OK) {
            std::cerr << "[KAFKA] Failed to set client.id: " << errstr << std::endl;
        }
        
        // Performance tuning
        conf->set("compression.codec", "snappy", errstr);  // Enable compression
        conf->set("batch.size", "16384", errstr);          // 16KB batches
        conf->set("linger.ms", "10", errstr);              // 10ms batching window
        conf->set("acks", "1", errstr);                    // Leader acknowledgment
        
        // Set delivery report callback
        deliveryCallback = std::make_unique<DeliveryReportCb>();
        if (conf->set("dr_cb", deliveryCallback.get(), errstr) != RdKafka::Conf::CONF_OK) {
            std::cerr << "[KAFKA] Failed to set delivery callback: " << errstr << std::endl;
        }
        
        // Create producer
        producer.reset(RdKafka::Producer::create(conf, errstr));
        if (!producer) {
            std::cerr << "[KAFKA] Failed to create producer: " << errstr << std::endl;
            exit(1);
        }
        
        delete conf;
        std::cout << "[KAFKA] Producer initialized successfully" << std::endl;
    }
    
    bool publish(
        const std::string& topic,
        const std::string& key,
        const char* payload,
        size_t payloadSize
    ) {
        if (!producer) {
            std::cerr << "[KAFKA] Producer not initialized!" << std::endl;
            return false;
        }
        
        RdKafka::ErrorCode err = producer->produce(
            topic,                              // Topic
            RdKafka::Topic::PARTITION_UA,      // Unassigned partition (let Kafka decide)
            RdKafka::Producer::RK_MSG_COPY,    // Copy payload
            const_cast<char*>(payload),        // Payload
            payloadSize,                       // Payload size
            key.empty() ? nullptr : &key,      // Message key
            key.empty() ? 0 : key.size(),      // Key size
            0,                                 // Timestamp (0 = now)
            nullptr                            // Message opaque
        );
        
        if (err != RdKafka::ERR_NO_ERROR) {
            std::cerr << "[KAFKA] Produce failed: " << RdKafka::err2str(err) << std::endl;
            return false;
        }
        
        // Poll to handle delivery reports (non-blocking)
        producer->poll(0);
        
        return true;
    }
    
    void shutdown() {
        if (producer) {
            std::cout << "[KAFKA] Flushing pending messages..." << std::endl;
            producer->flush(10000);  // Wait up to 10 seconds
            std::cout << "[KAFKA] Producer shutdown complete" << std::endl;
        }
    }
    
    void printStats() {
        if (producer) {
            std::cout << "[KAFKA] Outqueue size: " << producer->outq_len() << std::endl;
        }
    }
}
```

**Testing:**
```bash
# Compile
cd services/telemetry-ingest/build
make

# Should compile without errors
```

### 2.3 Create ProtobufSerializer Class

**New File:** `services/telemetry-ingest/include/core/ProtobufSerializer.h`

```cpp
#ifndef PROTOBUF_SERIALIZER_H
#define PROTOBUF_SERIALIZER_H

#include <string>
#include <optional>
#include "core/DataTypes.h"
#include "generated/f1_23/telemetry.pb.h"
#include "generated/kafka/messages.pb.h"

namespace ProtobufSerializer {
    
    /**
     * @brief Detect F1 game version from packet header
     * @param header Packet header
     * @return Game year (23, 24, etc.)
     */
    uint8_t detectGameVersion(const PacketHeader& header);
    
    /**
     * @brief Create Kafka message envelope
     * @param header Packet header
     * @param packetTypeName Human-readable packet type name
     * @return TelemetryMessage wrapper
     */
    kafka::TelemetryMessage createEnvelope(
        const PacketHeader& header,
        const std::string& packetTypeName
    );
    
    /**
     * @brief Serialize PacketMotionData to protobuf
     * @param data Binary packet data
     * @return Serialized TelemetryMessage (with envelope)
     */
    std::optional<std::string> serializeMotionData(const PacketMotionData& data);
    
    /**
     * @brief Serialize PacketSessionData to protobuf
     */
    std::optional<std::string> serializeSessionData(const PacketSessionData& data);
    
    /**
     * @brief Serialize PacketLapData to protobuf
     */
    std::optional<std::string> serializeLapData(const PacketLapData& data);
    
    /**
     * @brief Serialize PacketEventData to protobuf
     */
    std::optional<std::string> serializeEventData(const PacketEventData& data);
    
    /**
     * @brief Serialize PacketParticipantsData to protobuf
     */
    std::optional<std::string> serializeParticipantsData(const PacketParticipantsData& data);
    
    /**
     * @brief Serialize PacketCarSetupData to protobuf
     */
    std::optional<std::string> serializeCarSetupData(const PacketCarSetupData& data);
    
    /**
     * @brief Serialize PacketCarTelemetryData to protobuf
     */
    std::optional<std::string> serializeCarTelemetryData(const PacketCarTelemetryData& data);
    
    /**
     * @brief Serialize PacketCarStatusData to protobuf
     */
    std::optional<std::string> serializeCarStatusData(const PacketCarStatusData& data);
    
    /**
     * @brief Serialize PacketFinalClassificationData to protobuf
     */
    std::optional<std::string> serializeFinalClassificationData(const PacketFinalClassificationData& data);
    
    /**
     * @brief Serialize PacketLobbyInfoData to protobuf
     */
    std::optional<std::string> serializeLobbyInfoData(const PacketLobbyInfoData& data);
    
    /**
     * @brief Serialize PacketCarDamageData to protobuf
     */
    std::optional<std::string> serializeCarDamageData(const PacketCarDamageData& data);
    
    /**
     * @brief Serialize PacketSessionHistoryData to protobuf
     */
    std::optional<std::string> serializeSessionHistoryData(const PacketSessionHistoryData& data);
    
    /**
     * @brief Serialize PacketTyreSetsData to protobuf
     */
    std::optional<std::string> serializeTyreSetsData(const PacketTyreSetsData& data);
    
    /**
     * @brief Serialize PacketMotionExData to protobuf
     */
    std::optional<std::string> serializeMotionExData(const PacketMotionExData& data);
}

#endif // PROTOBUF_SERIALIZER_H
```

**Implementation File:** `services/telemetry-ingest/src/core/ProtobufSerializer.cpp`

*This is a large file - I'll show the structure and one complete example:*

```cpp
#include "core/ProtobufSerializer.h"
#include "core/DataMaps.h"
#include <google/protobuf/util/time_util.h>
#include <google/protobuf/any.pb.h>
#include <uuid/uuid.h>  // Or use boost::uuid
#include <iostream>

namespace ProtobufSerializer {
    
    uint8_t detectGameVersion(const PacketHeader& header) {
        return header.gameYear;
    }
    
    kafka::TelemetryMessage createEnvelope(
        const PacketHeader& header,
        const std::string& packetTypeName
    ) {
        kafka::TelemetryMessage message;
        
        // Generate UUID for message ID (simplified - use proper UUID library)
        message.set_message_id("msg-" + std::to_string(header.frameIdentifier));
        
        // Set timestamp
        auto* timestamp = new google::protobuf::Timestamp();
        timestamp->set_seconds(std::time(nullptr));
        timestamp->set_nanos(0);
        message.set_allocated_timestamp(timestamp);
        
        // Set metadata
        message.set_game_year(header.gameYear);
        message.set_packet_type(header.packetId);
        message.set_packet_type_name(packetTypeName);
        message.set_session_uid(header.sessionUID);
        message.set_session_time(header.sessionTime);
        message.set_frame_identifier(header.frameIdentifier);
        
        return message;
    }
    
    // EXAMPLE IMPLEMENTATION: Motion Data
    std::optional<std::string> serializeMotionData(const PacketMotionData& data) {
        try {
            // Create protobuf message
            f1_23::PacketMotionData protoPacket;
            
            // Serialize header
            auto* header = protoPacket.mutable_header();
            header->set_packet_format(data.header.packetFormat);
            header->set_game_year(data.header.gameYear);
            header->set_game_major_version(data.header.gameMajorVersion);
            header->set_game_minor_version(data.header.gameMinorVersion);
            header->set_packet_version(data.header.packetVersion);
            header->set_packet_id(data.header.packetId);
            header->set_session_uid(data.header.sessionUID);
            header->set_session_time(data.header.sessionTime);
            header->set_frame_identifier(data.header.frameIdentifier);
            header->set_overall_frame_identifier(data.header.overallFrameIdentifier);
            header->set_player_car_index(data.header.playerCarIndex);
            header->set_secondary_player_car_index(data.header.secondaryPlayerCarIndex);
            
            // Serialize car motion data (22 cars)
            for (int i = 0; i < 22; i++) {
                const auto& carData = data.carMotionData[i];
                auto* protoCar = protoPacket.add_car_motion_data();
                
                protoCar->set_world_position_x(carData.worldPositionX);
                protoCar->set_world_position_y(carData.worldPositionY);
                protoCar->set_world_position_z(carData.worldPositionZ);
                protoCar->set_world_velocity_x(carData.worldVelocityX);
                protoCar->set_world_velocity_y(carData.worldVelocityY);
                protoCar->set_world_velocity_z(carData.worldVelocityZ);
                protoCar->set_world_forward_dir_x(carData.worldForwardDirX);
                protoCar->set_world_forward_dir_y(carData.worldForwardDirY);
                protoCar->set_world_forward_dir_z(carData.worldForwardDirZ);
                protoCar->set_world_right_dir_x(carData.worldRightDirX);
                protoCar->set_world_right_dir_y(carData.worldRightDirY);
                protoCar->set_world_right_dir_z(carData.worldRightDirZ);
                protoCar->set_g_force_lateral(carData.gForceLateral);
                protoCar->set_g_force_longitudinal(carData.gForceLongitudinal);
                protoCar->set_g_force_vertical(carData.gForceVertical);
                protoCar->set_yaw(carData.yaw);
                protoCar->set_pitch(carData.pitch);
                protoCar->set_roll(carData.roll);
            }
            
            // Create Kafka envelope
            kafka::TelemetryMessage envelope = createEnvelope(data.header, "PacketMotionData");
            
            // Pack payload into Any
            envelope.mutable_payload()->PackFrom(protoPacket);
            
            // Serialize to string
            std::string serialized;
            if (!envelope.SerializeToString(&serialized)) {
                std::cerr << "[PROTOBUF] Failed to serialize MotionData" << std::endl;
                return std::nullopt;
            }
            
            return serialized;
            
        } catch (const std::exception& e) {
            std::cerr << "[PROTOBUF] Exception serializing MotionData: " << e.what() << std::endl;
            return std::nullopt;
        }
    }
    
    // REPEAT PATTERN FOR OTHER 13 PACKET TYPES...
    // (CarTelemetry, Session, Lap, Event, Participants, etc.)
    
    std::optional<std::string> serializeCarTelemetryData(const PacketCarTelemetryData& data) {
        // TODO: Implement following same pattern as MotionData
        // See proto/f1_23/telemetry.proto for field mappings
        return std::nullopt;  // Placeholder
    }
    
    // ... Implement remaining 12 packet types ...
}
```

**Action Items:**
- [ ] Implement all 14 packet serialization functions
- [ ] Map binary struct fields → protobuf fields (use DataMaps.h for enums)
- [ ] Handle repeated fields (arrays)
- [ ] Handle enum conversions (use proto enums instead of DataMaps)
- [ ] Add error handling for each function

### 2.4 Update main.cpp

**File:** `services/telemetry-ingest/src/main.cpp`

**Replace ZeroMQ with Kafka:**

```cpp
// OLD includes:
#include "network/zmqPublisher.h"

// NEW includes:
#include "kafka/KafkaProducer.h"
#include "core/ProtobufSerializer.h"

// OLD initialization (line 16):
ZmqPublisher::initialize("tcp://*:5555");

// NEW initialization:
std::string kafkaBrokers = std::getenv("KAFKA_BOOTSTRAP_SERVERS") 
    ? std::getenv("KAFKA_BOOTSTRAP_SERVERS") 
    : "kafka:29092";
std::string kafkaTopic = std::getenv("KAFKA_TOPIC_RAW")
    ? std::getenv("KAFKA_TOPIC_RAW")
    : "f1-telemetry-raw";

std::cout << "Connecting to Kafka: " << kafkaBrokers << std::endl;
KafkaProducer::initialize(kafkaBrokers);
```

**Replace each packet handler:**

```cpp
// OLD (case 0 - Motion Data):
case 0: {
    auto maybeData = PacketHandlers::handlePacketMotionData(bytesReceived, buffer);
    if (!maybeData.has_value()) break;
    PacketMotionData data = maybeData.value();
    
    nlohmann::json processedData = TelemetryProcessor::processPacketMotionData(data);
    ZmqPublisher::send("PacketMotionData", processedData);
    break;
}

// NEW:
case 0: {
    auto maybeData = PacketHandlers::handlePacketMotionData(bytesReceived, buffer);
    if (!maybeData.has_value()) break;
    PacketMotionData data = maybeData.value();
    
    // Serialize to protobuf
    auto serialized = ProtobufSerializer::serializeMotionData(data);
    if (!serialized.has_value()) {
        std::cerr << "Failed to serialize MotionData" << std::endl;
        break;
    }
    
    // Publish to Kafka
    std::string key = std::to_string(data.header.sessionUID);
    bool success = KafkaProducer::publish(
        kafkaTopic,
        key,
        serialized.value().data(),
        serialized.value().size()
    );
    
    if (!success) {
        std::cerr << "Failed to publish MotionData to Kafka" << std::endl;
    }
    break;
}
```

**Repeat for all 14 packet types (cases 0-13).**

**Add cleanup:**
```cpp
// At end of main(), before return:
std::cout << "Shutting down..." << std::endl;
KafkaProducer::shutdown();
```

### 2.5 Update Dockerfile

**File:** `services/telemetry-ingest/Dockerfile`

**Add librdkafka and protobuf:**

```dockerfile
# Build stage
FROM ubuntu:22.04 as build

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    librdkafka-dev \      # <-- ADD THIS
    libprotobuf-dev \     # <-- ADD THIS
    protobuf-compiler \   # <-- ADD THIS
    && rm -rf /var/lib/apt/lists/*

# Copy generated protobuf files
COPY generated/ /app/generated/   # <-- ADD THIS

# ... rest of Dockerfile
```

### 2.6 Remove ZeroMQ Code

**Files to delete:**
- [ ] `include/network/zmqPublisher.h`
- [ ] `src/network/zmqPublisher.cpp`

**Files to update:**
- [ ] Remove all `#include "network/zmqPublisher.h"` references
- [ ] Remove all `ZmqPublisher::` calls

### 2.7 Testing Checklist

- [ ] Code compiles without errors
- [ ] Kafka producer connects successfully
- [ ] Protobuf serialization works for packet type 0 (Motion)
- [ ] Messages appear in Kafka topic (check Kafka UI)
- [ ] Implement remaining 13 packet types
- [ ] Test with F1 game UDP stream
- [ ] Monitor Kafka producer stats
- [ ] Check memory leaks (valgrind)

---

## Phase 3: Python Telemetry Processor & WebSocket Gateway

**Goal:** Replace ZeroMQ → Kafka, create WebSocket Gateway service  
**Effort:** 8-12 hours  
**Priority:** HIGH

### 3.1 Update requirements.txt

**File:** `services/telemetry-processor/requirements.txt`

```diff
-# Production dependencies
-pyzmq>=25.1.0
+# Kafka client
+confluent-kafka>=2.3.0

+# Protobuf
+protobuf>=4.25.1

-websockets>=12.0
-asyncio>=3.4.3

# ... keep rest of dependencies ...
```

**Install:**
```bash
cd services/telemetry-processor
pip install -r requirements.txt
```

### 3.2 Create Kafka Consumer Module

**New File:** `services/telemetry-processor/kafka_consumer.py`

```python
"""
Kafka Consumer for F1 Telemetry Data
Consumes protobuf messages from f1-telemetry-raw topic
"""
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError
from typing import Optional, Tuple
from generated.kafka import messages_pb2
from generated.f1_23 import telemetry_pb2

logger = logging.getLogger(__name__)


class TelemetryKafkaConsumer:
    """Kafka consumer for telemetry data"""
    
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        auto_offset_reset: str = 'latest'
    ):
        """
        Initialize Kafka consumer
        
        Args:
            bootstrap_servers: Comma-separated Kafka broker list
            topic: Topic to consume from
            group_id: Consumer group ID
            auto_offset_reset: 'earliest' or 'latest'
        """
        self.topic = topic
        self.consumer_config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': auto_offset_reset,
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 5000,
        }
        
        logger.info(f"Initializing Kafka consumer: {bootstrap_servers}")
        logger.info(f"Topic: {topic}, Group: {group_id}")
        
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([self.topic])
        self.running = False
        
        logger.info("Kafka consumer initialized successfully")
    
    def consume_message(self, timeout: float = 1.0) -> Optional[messages_pb2.TelemetryMessage]:
        """
        Consume one message from Kafka
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            TelemetryMessage or None
        """
        try:
            msg = self.consumer.poll(timeout=timeout)
            
            if msg is None:
                return None
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition - not an error
                    return None
                else:
                    raise KafkaException(msg.error())
            
            # Deserialize protobuf message
            telemetry_msg = messages_pb2.TelemetryMessage()
            telemetry_msg.ParseFromString(msg.value())
            
            return telemetry_msg
            
        except Exception as e:
            logger.error(f"Error consuming message: {e}")
            return None
    
    def close(self):
        """Close consumer and commit offsets"""
        logger.info("Closing Kafka consumer...")
        if self.consumer:
            self.consumer.close()
        logger.info("Kafka consumer closed")
```

### 3.3 Create Kafka Producer Module

**New File:** `services/telemetry-processor/kafka_producer.py`

```python
"""
Kafka Producer for Processed Telemetry Data
Produces to f1-telemetry-processed topic
"""
import logging
from confluent_kafka import Producer, KafkaException
from generated.kafka import messages_pb2

logger = logging.getLogger(__name__)


class TelemetryKafkaProducer:
    """Kafka producer for processed telemetry"""
    
    def __init__(self, bootstrap_servers: str):
        """
        Initialize Kafka producer
        
        Args:
            bootstrap_servers: Comma-separated Kafka broker list
        """
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers,
            'compression.type': 'snappy',
            'linger.ms': 10,
            'batch.size': 16384,
        }
        
        logger.info(f"Initializing Kafka producer: {bootstrap_servers}")
        self.producer = Producer(self.producer_config)
        logger.info("Kafka producer initialized successfully")
    
    def produce_message(
        self,
        topic: str,
        message: messages_pb2.TelemetryMessage,
        key: str = None
    ) -> bool:
        """
        Produce message to Kafka topic
        
        Args:
            topic: Kafka topic
            message: TelemetryMessage protobuf
            key: Message key (optional)
            
        Returns:
            True if successful
        """
        try:
            # Serialize protobuf
            serialized = message.SerializeToString()
            
            # Produce to Kafka
            self.producer.produce(
                topic=topic,
                value=serialized,
                key=key.encode('utf-8') if key else None,
                callback=self._delivery_callback
            )
            
            # Poll to handle delivery reports
            self.producer.poll(0)
            
            return True
            
        except Exception as e:
            logger.error(f"Error producing message: {e}")
            return False
    
    def _delivery_callback(self, err, msg):
        """Delivery report callback"""
        if err:
            logger.error(f"Message delivery failed: {err}")
        # Optionally log successful deliveries (verbose)
        # else:
        #     logger.debug(f"Message delivered to {msg.topic()}")
    
    def flush(self, timeout: float = 10.0):
        """Flush pending messages"""
        logger.info("Flushing pending messages...")
        self.producer.flush(timeout=timeout)
    
    def close(self):
        """Close producer"""
        self.flush()
        logger.info("Kafka producer closed")
```

### 3.4 Update main.py

**File:** `services/telemetry-processor/main.py`

**Complete rewrite:**

```python
"""
F1 Telemetry Processor Service (Kafka Version)

Middleware service that:
1. Consumes telemetry data from Kafka (f1-telemetry-raw)
2. Processes and filters data based on operational mode
3. Produces processed data to Kafka (f1-telemetry-processed)
4. WebSocket forwarding handled by websocket-gateway service
"""

import argparse
import signal
import sys
import os
import logging
from kafka_consumer import TelemetryKafkaConsumer
from kafka_producer import TelemetryKafkaProducer
from generated.kafka import messages_pb2
from generated.f1_23 import telemetry_pb2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelemetryProcessor:
    """Main service orchestrator for telemetry processing"""
    
    def __init__(self, mode: str):
        self.mode = mode
        self.consumer = None
        self.producer = None
        self.running = False
        
        # Configuration from environment
        self.kafka_brokers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
        self.topic_raw = os.getenv('KAFKA_TOPIC_RAW', 'f1-telemetry-raw')
        self.topic_processed = os.getenv('KAFKA_TOPIC_PROCESSED', 'f1-telemetry-processed')
        self.consumer_group = os.getenv('KAFKA_CONSUMER_GROUP', 'telemetry-processor')
        
        logger.info(f"Telemetry Processor initialized in {mode} mode")
        logger.info(f"Kafka brokers: {self.kafka_brokers}")
    
    def start(self):
        """Start the telemetry processor service"""
        self.running = True
        
        try:
            # Initialize Kafka consumer
            logger.info("Initializing Kafka consumer...")
            self.consumer = TelemetryKafkaConsumer(
                bootstrap_servers=self.kafka_brokers,
                topic=self.topic_raw,
                group_id=self.consumer_group
            )
            
            # Initialize Kafka producer
            logger.info("Initializing Kafka producer...")
            self.producer = TelemetryKafkaProducer(
                bootstrap_servers=self.kafka_brokers
            )
            
            logger.info("Telemetry Processor started successfully!")
            logger.info(f"Consuming from: {self.topic_raw}")
            logger.info(f"Producing to: {self.topic_processed}")
            logger.info("Waiting for messages...")
            
            # Main loop
            message_count = 0
            while self.running:
                telemetry_msg = self.consumer.consume_message(timeout=1.0)
                
                if telemetry_msg:
                    message_count += 1
                    self._process_telemetry_message(telemetry_msg)
                    
                    if message_count % 100 == 0:
                        logger.info(f"Processed {message_count} messages")
            
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            self.stop()
        except Exception as e:
            logger.error(f"Telemetry processor error: {e}", exc_info=True)
            self.stop()
            raise
    
    def _process_telemetry_message(self, telemetry_msg: messages_pb2.TelemetryMessage):
        """
        Process incoming telemetry message
        
        Args:
            telemetry_msg: TelemetryMessage from Kafka
        """
        try:
            if self.mode == "passthrough":
                # Passthrough mode - forward directly to processed topic
                key = str(telemetry_msg.session_uid)
                self.producer.produce_message(
                    topic=self.topic_processed,
                    message=telemetry_msg,
                    key=key
                )
                
            elif self.mode == "datacollection":
                # Data collection mode - process and store
                self._store_telemetry_data(telemetry_msg)
                
                # Still forward to processed topic
                key = str(telemetry_msg.session_uid)
                self.producer.produce_message(
                    topic=self.topic_processed,
                    message=telemetry_msg,
                    key=key
                )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def _store_telemetry_data(self, telemetry_msg: messages_pb2.TelemetryMessage):
        """
        Store telemetry data (datacollection mode)
        Future: Write to InfluxDB, PostgreSQL, etc.
        
        Args:
            telemetry_msg: TelemetryMessage to store
        """
        # TODO: Implement data storage
        # For now, just log
        logger.debug(f"Storing {telemetry_msg.packet_type_name} data")
    
    def stop(self):
        """Stop the service gracefully"""
        logger.info("Stopping Telemetry Processor...")
        self.running = False
        
        if self.producer:
            self.producer.close()
        
        if self.consumer:
            self.consumer.close()
        
        logger.info("Telemetry Processor stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='F1 Telemetry Processor Service')
    parser.add_argument(
        '--mode',
        type=str,
        choices=['passthrough', 'datacollection'],
        default='passthrough',
        help='Operation mode'
    )
    args = parser.parse_args()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start processor
    processor = TelemetryProcessor(mode=args.mode)
    processor.start()


if __name__ == "__main__":
    main()
```

### 3.5 Remove Old Code

**Directories/Files to delete:**
- [ ] `zmq_client/` directory (entire folder)
- [ ] `websocket_server/` directory (entire folder)

**Note:** WebSocket functionality is now handled by the `websocket-gateway` service (already created).

### 3.6 Update Dockerfile

**File:** `services/telemetry-processor/Dockerfile`

```dockerfile
# BEFORE:
COPY zmq_client/ ./zmq_client/
COPY websocket_server/ ./websocket_server/

# AFTER:
COPY kafka_consumer.py ./
COPY kafka_producer.py ./
COPY generated/ ./generated/
```

### 3.7 Testing Checklist (Processor)

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify generated protobuf files exist
- [ ] Test Kafka consumer connection
- [ ] Test message deserialization
- [ ] Test Kafka producer
- [ ] Verify messages flow: raw → processed topics
- [ ] Check Kafka UI for consumer lag
- [ ] Test datacollection mode
- [ ] Performance testing (throughput)

### 3.8 Create WebSocket Gateway Service

**Goal:** New service to bridge Kafka → WebSocket for frontend

**New Directory Structure:**
```
services/websocket-gateway/
├── main.py
├── kafka_consumer.py
├── websocket_server.py
├── requirements.txt
├── Dockerfile
├── README.md
└── generated/  (symlink or copy from root)
```

#### 3.8.1 Create Directory and Files

```bash
mkdir -p services/websocket-gateway
cd services/websocket-gateway
```

#### 3.8.2 Create requirements.txt

**New File:** `services/websocket-gateway/requirements.txt`

```txt
# Kafka client
confluent-kafka>=2.3.0

# Protobuf
protobuf>=4.25.1

# WebSocket server
websockets>=12.0

# Async support
asyncio>=3.4.3

# Development dependencies
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

#### 3.8.3 Create kafka_consumer.py

**New File:** `services/websocket-gateway/kafka_consumer.py`

```python
"""
Kafka Consumer for WebSocket Gateway
Consumes from f1-telemetry-processed topic
"""
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError
from typing import Optional
from generated.kafka import messages_pb2

logger = logging.getLogger(__name__)


class GatewayKafkaConsumer:
    """Kafka consumer for gateway service"""
    
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str = 'websocket-gateway'
    ):
        self.topic = topic
        self.consumer_config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
        }
        
        logger.info(f"Initializing Kafka consumer: {bootstrap_servers}")
        self.consumer = Consumer(self.consumer_config)
        self.consumer.subscribe([self.topic])
    
    def consume_message(self, timeout: float = 1.0) -> Optional[messages_pb2.TelemetryMessage]:
        """Consume one message from Kafka"""
        try:
            msg = self.consumer.poll(timeout=timeout)
            
            if msg is None or msg.error():
                return None
            
            telemetry_msg = messages_pb2.TelemetryMessage()
            telemetry_msg.ParseFromString(msg.value())
            return telemetry_msg
            
        except Exception as e:
            logger.error(f"Error consuming: {e}")
            return None
    
    def close(self):
        """Close consumer"""
        if self.consumer:
            self.consumer.close()
```

#### 3.8.4 Create websocket_server.py

**New File:** `services/websocket-gateway/websocket_server.py`

```python
"""
WebSocket Server for Frontend
Broadcasts telemetry data to connected clients
"""
import asyncio
import websockets
import json
import logging
from typing import Set
from google.protobuf.json_format import MessageToDict
from generated.kafka import messages_pb2

logger = logging.getLogger(__name__)


class WebSocketBroadcaster:
    """WebSocket server that broadcasts telemetry to clients"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
    
    async def register_client(self, websocket: websockets.WebSocketServerProtocol):
        """Register new WebSocket client"""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
    
    async def unregister_client(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister WebSocket client"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle WebSocket client connection"""
        await self.register_client(websocket)
        try:
            # Keep connection alive
            async for message in websocket:
                # Echo or handle client messages if needed
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def broadcast_message(self, telemetry_msg: messages_pb2.TelemetryMessage):
        """
        Broadcast protobuf message to all connected clients
        Converts protobuf to JSON before sending
        """
        if not self.clients:
            return
        
        try:
            # Convert protobuf to JSON
            json_data = MessageToDict(
                telemetry_msg,
                preserving_proto_field_name=True,
                including_default_value_fields=False
            )
            
            # Serialize to JSON string
            message = json.dumps(json_data)
            
            # Broadcast to all clients
            disconnected_clients = set()
            for client in self.clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.add(client)
            
            # Clean up disconnected clients
            for client in disconnected_clients:
                await self.unregister_client(client)
                
        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
    
    async def start(self):
        """Start WebSocket server"""
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        logger.info("WebSocket server started")
    
    async def stop(self):
        """Stop WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        logger.info("WebSocket server stopped")
```

#### 3.8.5 Create main.py

**New File:** `services/websocket-gateway/main.py`

```python
"""
WebSocket Gateway Service
Bridges Kafka (f1-telemetry-processed) to WebSocket clients
"""
import asyncio
import logging
import signal
import sys
import os
from kafka_consumer import GatewayKafkaConsumer
from websocket_server import WebSocketBroadcaster

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebSocketGateway:
    """Main gateway service orchestrator"""
    
    def __init__(self):
        self.kafka_brokers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
        self.kafka_topic = os.getenv('KAFKA_TOPIC_PROCESSED', 'f1-telemetry-processed')
        self.ws_host = os.getenv('WEBSOCKET_HOST', '0.0.0.0')
        self.ws_port = int(os.getenv('WEBSOCKET_PORT', '8765'))
        
        self.consumer = None
        self.broadcaster = None
        self.running = False
        
        logger.info("WebSocket Gateway initialized")
        logger.info(f"Kafka: {self.kafka_brokers} -> {self.kafka_topic}")
        logger.info(f"WebSocket: {self.ws_host}:{self.ws_port}")
    
    async def start(self):
        """Start the gateway service"""
        self.running = True
        
        try:
            # Initialize Kafka consumer
            self.consumer = GatewayKafkaConsumer(
                bootstrap_servers=self.kafka_brokers,
                topic=self.kafka_topic
            )
            
            # Initialize WebSocket broadcaster
            self.broadcaster = WebSocketBroadcaster(
                host=self.ws_host,
                port=self.ws_port
            )
            
            # Start WebSocket server
            await self.broadcaster.start()
            
            logger.info("Gateway started - consuming and broadcasting...")
            
            # Main loop - consume from Kafka and broadcast
            message_count = 0
            while self.running:
                # Consume from Kafka (non-blocking)
                telemetry_msg = await asyncio.to_thread(
                    self.consumer.consume_message,
                    timeout=0.1
                )
                
                if telemetry_msg:
                    message_count += 1
                    await self.broadcaster.broadcast_message(telemetry_msg)
                    
                    if message_count % 100 == 0:
                        logger.info(f"Broadcasted {message_count} messages")
                
                # Small sleep to prevent CPU spinning
                await asyncio.sleep(0.001)
                
        except Exception as e:
            logger.error(f"Gateway error: {e}", exc_info=True)
            raise
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the gateway service"""
        logger.info("Stopping WebSocket Gateway...")
        self.running = False
        
        if self.broadcaster:
            await self.broadcaster.stop()
        
        if self.consumer:
            self.consumer.close()
        
        logger.info("Gateway stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)


async def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    gateway = WebSocketGateway()
    await gateway.start()


if __name__ == "__main__":
    asyncio.run(main())
```

#### 3.8.6 Create Dockerfile

**New File:** `services/websocket-gateway/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY kafka_consumer.py .
COPY websocket_server.py .

# Copy generated protobuf files
COPY generated/ ./generated/

# Expose WebSocket port
EXPOSE 8765

CMD ["python", "main.py"]
```

#### 3.8.7 Create README.md

**New File:** `services/websocket-gateway/README.md`

```markdown
# WebSocket Gateway Service

Bridges Kafka telemetry stream to WebSocket clients (frontend).

## Purpose
- Consumes from `f1-telemetry-processed` Kafka topic
- Deserializes protobuf messages
- Converts to JSON
- Broadcasts to WebSocket clients

## Environment Variables
- `KAFKA_BOOTSTRAP_SERVERS` - Kafka brokers (default: kafka:29092)
- `KAFKA_TOPIC_PROCESSED` - Kafka topic (default: f1-telemetry-processed)
- `WEBSOCKET_HOST` - WebSocket bind address (default: 0.0.0.0)
- `WEBSOCKET_PORT` - WebSocket port (default: 8765)

## Running Locally
```bash
pip install -r requirements.txt
python main.py
```

## Docker
```bash
docker build -t websocket-gateway .
docker run -p 8765:8765 websocket-gateway
```
```

#### 3.8.8 Update docker-compose.yml

**Add to:** `docker-compose.yml`

```yaml
  websocket-gateway:
    container_name: f1-websocket-gateway
    build:
      context: .
      dockerfile: services/websocket-gateway/Dockerfile
    ports:
      - "8765:8765"
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:29092
      - KAFKA_TOPIC_PROCESSED=f1-telemetry-processed
      - WEBSOCKET_HOST=0.0.0.0
      - WEBSOCKET_PORT=8765
    depends_on:
      - kafka
      - telemetry-processor
    networks:
      - telemetry-network
    restart: unless-stopped
```

#### 3.8.9 Copy Generated Protobuf Files

```bash
# Create symlink or copy generated files
cd services/websocket-gateway
ln -s ../../proto/generated ./generated

# Or copy if symlinks don't work in Docker
cp -r ../../proto/generated ./generated
```

### 3.9 Testing Checklist (WebSocket Gateway)

- [ ] Install dependencies
- [ ] Verify protobuf files accessible
- [ ] Test Kafka consumer connection
- [ ] Test WebSocket server starts
- [ ] Test client connection to WebSocket
- [ ] Test message broadcasting
- [ ] Test multiple clients
- [ ] Test reconnection handling
- [ ] Performance testing

---

## Phase 4: Frontend & Testing

**Goal:** Ensure frontend connects to WebSocket Gateway  
**Effort:** 2-3 hours  
**Priority:** MEDIUM

### 4.1 Verify Frontend Configuration

**File:** `services/telemetry-frontend/src/socket/socketService.ts`

**No changes needed** - frontend still connects via WebSocket.

**Verify environment variable:**
```bash
# In .env or docker-compose.yml
VITE_WEBSOCKET_URL=ws://localhost:8765
```

Frontend connects to `websocket-gateway` service (already created), which:
- Consumes from `f1-telemetry-processed` Kafka topic
- Deserializes protobuf messages
- Converts to JSON
- Broadcasts via WebSocket

### 4.2 Test WebSocket Gateway

**Start services:**
```bash
docker-compose up -d websocket-gateway
docker logs -f f1-websocket-gateway
```

**Verify:**
- [ ] Gateway connects to Kafka
- [ ] Gateway subscribes to `f1-telemetry-processed` topic
- [ ] WebSocket server starts on port 8765
- [ ] Frontend can connect
- [ ] Messages are forwarded

### 4.3 End-to-End Integration Testing

**Full pipeline test:**

```bash
# 1. Start all infrastructure
docker-compose up -d zookeeper kafka kafka-ui

# 2. Start services
docker-compose up -d telemetry-ingest telemetry-processor websocket-gateway

# 3. Start frontend
docker-compose up -d telemetry-frontend

# 4. Monitor logs
docker logs -f f1-telemetry-ingest
docker logs -f f1-telemetry-processor
docker logs -f f1-websocket-gateway

# 5. Check Kafka UI
open http://localhost:8080

# 6. Check frontend
open http://localhost:3000
```

**Test with F1 Game:**
1. Start F1 2023 game
2. Enable UDP telemetry (Settings → Telemetry → UDP: ON, Port: 20777)
3. Start a session
4. Verify data flow:
   - Ingest receives UDP packets ✓
   - Kafka shows messages in `f1-telemetry-raw` ✓
   - Processor consumes and produces to `f1-telemetry-processed` ✓
   - Gateway forwards to WebSocket ✓
   - Frontend displays data ✓

### 4.4 Test with Simulator

**If no F1 game available:**

```bash
# Start simulator
docker-compose up -d telemetry-simulator

# Simulator sends UDP packets to ingest service
# Monitor logs to verify data flow
```

---

## Phase 5: Cleanup & Optimization

**Goal:** Remove old code, optimize performance  
**Effort:** 4-6 hours  
**Priority:** MEDIUM

### 5.1 Code Cleanup

#### Ingest Service (C++)
- [ ] Delete `TelemetryProcessor.cpp` (575 lines - no longer needed)
- [ ] Delete `TelemetryProcessor.h`
- [ ] Remove all JSON includes (`nlohmann/json.hpp`)
- [ ] Remove DataMaps.h usage (enums now in protobuf)
- [ ] Update README.md
- [ ] Remove old comments referencing ZeroMQ/JSON

#### Processor Service (Python)
- [ ] Remove `zmq_client/` tests
- [ ] Remove `websocket_server/` tests
- [ ] Update README.md
- [ ] Remove old imports
- [ ] Update docstrings

#### Documentation
- [ ] Update DEVELOPMENT.md with new build instructions
- [ ] Update DEPLOYMENT.md
- [ ] Update service READMEs
- [ ] Add Kafka troubleshooting guide

### 5.2 Performance Optimization

#### Kafka Configuration
```bash
# Tune producer (ingest)
compression.codec=snappy
batch.size=32768        # Increase if high throughput
linger.ms=10           # Batch window

# Tune consumer (processor)
fetch.min.bytes=1
fetch.max.wait.ms=500
max.poll.records=500
```

#### Protobuf Optimization
- Use protobuf arena allocation for large messages
- Enable message caching for repeated fields
- Profile serialization performance

### 5.3 Monitoring & Metrics

**Add Prometheus metrics:**

```cpp
// C++ - Kafka producer metrics
- kafka_messages_produced_total
- kafka_bytes_sent_total
- kafka_errors_total
- kafka_serialization_time_seconds
```

```python
# Python - Kafka consumer metrics
- kafka_messages_consumed_total
- kafka_lag_messages
- kafka_processing_time_seconds
```

### 5.4 Testing Comprehensive

#### Unit Tests
- [ ] C++ - KafkaProducer unit tests
- [ ] C++ - ProtobufSerializer tests (all 14 types)
- [ ] Python - Kafka consumer tests
- [ ] Python - Kafka producer tests

#### Integration Tests
- [ ] Ingest → Kafka flow
- [ ] Kafka → Processor flow
- [ ] Processor → Kafka flow
- [ ] Kafka → Gateway → WebSocket flow
- [ ] Full end-to-end pipeline

#### Performance Tests
- [ ] Throughput testing (packets/sec)
- [ ] Latency testing (p50, p95, p99)
- [ ] Memory usage profiling
- [ ] CPU usage monitoring
- [ ] Network bandwidth measurement

### 5.5 Documentation Updates

**Update all documentation:**
- [ ] README.md - Architecture diagram
- [ ] DEVELOPMENT.md - Build instructions
- [ ] DEPLOYMENT.md - Deployment guide
- [ ] Service READMEs
- [ ] API documentation
- [ ] Troubleshooting guide

---

## Implementation Checklist

### ✅ Phase 1: Infrastructure (2-3 hours)
- [ ] Install protoc and librdkafka
- [ ] Compile protobuf schemas
- [ ] Start Kafka infrastructure
- [ ] Verify Kafka UI access

### 🚧 Phase 2: C++ Ingest (12-16 hours)
- [ ] Update CMakeLists.txt
- [ ] Create KafkaProducer class
- [ ] Create ProtobufSerializer class
- [ ] Implement 14 packet serializers
- [ ] Update main.cpp
- [ ] Update Dockerfile
- [ ] Remove ZeroMQ code
- [ ] Test and debug

### 🚧 Phase 3: Python Processor & WebSocket Gateway (8-12 hours)
- [ ] **Processor:** Update requirements.txt
- [ ] **Processor:** Create Kafka consumer module
- [ ] **Processor:** Create Kafka producer module
- [ ] **Processor:** Rewrite main.py
- [ ] **Processor:** Remove ZMQ/WebSocket code
- [ ] **Processor:** Update Dockerfile
- [ ] **Gateway:** Create new websocket-gateway service
- [ ] **Gateway:** Implement Kafka consumer
- [ ] **Gateway:** Implement WebSocket server
- [ ] **Gateway:** Add Dockerfile
- [ ] Test and debug both services

### 🚧 Phase 4: Integration (2-3 hours)
- [ ] Verify frontend configuration
- [ ] Test WebSocket Gateway
- [ ] End-to-end integration test
- [ ] Test with F1 game/simulator

### 🚧 Phase 5: Cleanup (4-6 hours)
- [ ] Remove old code
- [ ] Optimize performance
- [ ] Add monitoring
- [ ] Comprehensive testing
- [ ] Update documentation

---

## Success Criteria

**The migration is complete when:**
- ✅ All services compile without errors
- ✅ No ZeroMQ code remains
- ✅ No JSON serialization in ingest service
- ✅ All 14 packet types work with protobuf
- ✅ Messages flow through Kafka (3 topics)
- ✅ Frontend displays real-time data
- ✅ Kafka UI shows healthy topics
- ✅ No data loss under normal operation
- ✅ Performance meets targets (50k msg/s, <10ms latency)
- ✅ Tests pass (unit + integration)
- ✅ Documentation updated

---

## Rollback Plan

If critical issues occur:

```bash
# 1. Stop new services
docker-compose down

# 2. Checkout previous commit
git checkout <previous-commit>

# 3. Rebuild with old code
make build
make up

# 4. Verify old architecture works
```

---

## Getting Help

**Resources:**
- Protobuf Guide: `docs/PROTOBUF.md`
- Migration Guide: `docs/MIGRATION_KAFKA_PROTOBUF.md`
- Quick Reference: `docs/QUICK_REFERENCE.md`
- Kafka UI: http://localhost:8080

**Debugging:**
```bash
# Check Kafka topics
docker exec -it f1-kafka kafka-topics --list --bootstrap-server localhost:9092

# Consume messages
docker exec -it f1-kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic f1-telemetry-raw \
  --from-beginning

# Check consumer groups
docker exec -it f1-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe --group telemetry-processor
```

---

**Last Updated:** 2024-12-05  
**Status:** Ready for implementation  
**Estimated Total Time:** 30-40 hours  
**Next Step:** Start with Phase 1 (Infrastructure)
