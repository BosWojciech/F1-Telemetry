#include <iostream>
#include <cstring>
#include <optional>

#include "core/PacketHandlers.h"
#include "core/DataTypes.h"

bool PacketHandlers::validatePacket(ssize_t bytesReceived, size_t correctSize, std::string name)
{
    if (static_cast<size_t>(bytesReceived) < correctSize)
    {
        std::cerr << "Received " << name << " too small! Expected " << correctSize << ", got " << bytesReceived << " bytes." << std::endl;
        return false;
    }
    return true;
}

std::optional<PacketMotionData> PacketHandlers::handlePacketMotionData(ssize_t bytesReceived, char* buffer){
    if(!validatePacket(bytesReceived, PACKET_MOTION_DATA_SIZE, "PacketMotionData"))
        return std::nullopt;

    PacketMotionData motionData;
    std::memcpy(&motionData, buffer, sizeof(PACKET_MOTION_DATA_SIZE));

    return motionData;
    
}

// PacketCarTelemetryData PacketHandlers::handlePacketCarTelemetryData(ssize_t bytesReceived, char* buffer) {
//     if (!validatePacket(bytesReceived, PACKET_CAR_TELEMETRY_DATA_SIZE, "PacketCarTelemetryData"))
//         return;

//     PacketCarTelemetryData telemetryPacket;
//     std::memcpy(&telemetryPacket, buffer, sizeof(PacketCarTelemetryData));

//     uint8_t playerIndex = telemetryPacket.header.playerCarIndex;
//     if (playerIndex >= 22)
//         return;
    

//     const CarTelemetryData &playerCar = telemetryPacket.carTelemetryData[playerIndex];
//     std::cout << "Player Car Telemetry:" << std::endl;
//     std::cout << "  Steer: " << playerCar.steer << std::endl;
//     std::cout << "  Throttle: " << playerCar.throttle << std::endl;
//     std::cout << "  Brake: " << playerCar.brake << std::endl;
//     std::cout << "  RPM: " << playerCar.engineRPM << std::endl;
//     std::cout << "  Gear: " << static_cast<int>(playerCar.gear) << std::endl;
//     std::cout << "  Speed: " << playerCar.speed << "km/h" << std::endl;
//     std::cout << "  DRS: " << static_cast<int>(playerCar.drs) << std::endl;
// }