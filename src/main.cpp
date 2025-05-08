#include <iostream>
#include <cstdint>
#include <cstring>
#include "network/udpClient.h"
#include "core/DataTypes.h"
#include "nlohmann/json.hpp"

// Define the expected size of PacketCarTelemetryData based on documentation


int main() {
    std::cout << "Running F1 UDP Client" << std::endl;

    // Check structure size at runtime
    if (sizeof(PacketCarTelemetryData) != PACKET_CAR_TELEMETRY_DATA_SIZE) {
        std::cerr << "ERROR: PacketCarTelemetryData size mismatch!" << std::endl;
        std::cerr << "  Struct size: " << sizeof(PacketCarTelemetryData)
                  << ", Expected: " << PACKET_CAR_TELEMETRY_DATA_SIZE << std::endl;
        return 1;
    }

    UdpClient client(20777);
    if (!client.initialize()) {
        return 1;
    }

    char buffer[2048];

    while (true) {

        std::cout << "\033[2J\033[H";

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
        //std::cout << "Received packet with header: " << static_cast<int>(header.packetId) << ", Size: " << bytesReceived << " bytes" << std::endl;

        switch (header.packetId) {
            case 6: { // PacketCarTelemetryData
                if (bytesReceived < PACKET_CAR_TELEMETRY_DATA_SIZE) {
                    //std::cerr << "Received PacketCarTelemetryData too small! Expected " << PACKET_CAR_TELEMETRY_DATA_SIZE << ", got " << bytesReceived << " bytes." << std::endl;
                    continue;
                }

                PacketCarTelemetryData telemetryPacket;
                std::memcpy(&telemetryPacket, buffer, sizeof(PacketCarTelemetryData));

                uint8_t playerIndex = telemetryPacket.header.playerCarIndex;
                if (playerIndex >= 22) {
                    //std::cerr << "Invalid playerCarIndex: " << static_cast<int>(playerIndex) << std::endl;
                    continue;
                }

                const CarTelemetryData& playerCar = telemetryPacket.carTelemetryData[playerIndex];
                std::cout << "Player Car Telemetry:" << std::endl;
                std::cout << "  Steer: " << playerCar.steer << std::endl;
                std::cout << "  Throttle: " << playerCar.throttle << std::endl;
                std::cout << "  Brake: " << playerCar.brake << std::endl;
                std::cout << "  RPM: " << playerCar.engineRPM << std::endl;
                std::cout << "  Gear: " << static_cast<int>(playerCar.gear) << std::endl;
                std::cout << "  Speed: " << playerCar.speed << "km/h" <<std::endl;
                std::cout << "  DRS: " << static_cast<int>(playerCar.drs) << std::endl;
                break;
            }

            default:
                break;
        }
    }

    return 0;
}
