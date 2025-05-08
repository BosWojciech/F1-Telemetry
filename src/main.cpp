#include <iostream>
#include <cstdint>
#include <cstring>
#include "network/udpClient.h"
#include "nlohmann/json.hpp"
#include "core/TelemetryProcessor.h"


// Define the expected size of PacketCarTelemetryData based on documentation
const size_t PACKET_CAR_TELEMETRY_DATA_SIZE = 1352;

int main() {
    std::cout << "Running F1 UDP Client" << std::endl;

    UdpClient client(20777);
    if (!client.initialize()) {
        return 1;
    }

    char buffer[2048];

    while (true) {
        ssize_t bytesReceived = client.receiveData(buffer, sizeof(buffer));
        if (bytesReceived == -1) {
            std::cerr << "Error receiving data." << std::endl;
            break;
        }

        if (bytesReceived < sizeof(PacketHeader)) {
            std::cerr << "Received packet too small for header!" << std::endl;
            continue;
        }

        PacketHeader header;
        std::memcpy(&header, buffer, sizeof(PacketHeader));
        std::cout << "Received packet with header: " << header.packetId << ", Size: " << bytesReceived << " bytes" << std::endl;

        switch (header.packetId) {
            case 6: {
                if (bytesReceived < PACKET_CAR_TELEMETRY_DATA_SIZE) {
                    std::cerr << "Received PacketCarTelemetryData too small! Expected "
                              << PACKET_CAR_TELEMETRY_DATA_SIZE << ", got " << bytesReceived << " bytes."
                              << std::endl;
                    continue;
                }
                PacketCarTelemetryData packetCarTelemetryData;
                std::memcpy(&packetCarTelemetryData, buffer, sizeof(PacketCarTelemetryData));

                nlohmann::json telemetryJson = TelemetryProcessor::processPacketCarTelemetryData(packetCarTelemetryData);

                if (telemetryJson.contains("cars") && telemetryJson["cars"].is_array()) {
                    std::cout << "Car Telemetry Data:" << std::endl;
                    for (const auto& car : telemetryJson["cars"]) {
                        if (car.contains("throttle") && car.contains("brake")) {
                            std::cout << "  Throttle: " << car["throttle"]
                                      << ", Brake: " << car["brake"] << std::endl;
                        }
                    }
                }
                break;
            }

            default:
                std::cout << "Unknown packet ID: " << header.packetId << std::endl;
                break;
        }
    }

    return 0;
}