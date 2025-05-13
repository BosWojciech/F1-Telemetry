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
    std::memcpy(&motionData, buffer, sizeof(PacketMotionData));

    return motionData;
    
}

std::optional<PacketSessionData> PacketHandlers::handlePacketSessionData(ssize_t bytesReceived, char* buffer){
    if(!validatePacket(bytesReceived, PACKET_SESSION_DATA_SIZE, "PacketSessionData"))
        return std::nullopt;
    
    PacketSessionData sessionData;
    std::memcpy(&sessionData, buffer, sizeof(PacketSessionData));

    return sessionData;
}

std::optional<PacketLapData> PacketHandlers::handlePacketLapData(ssize_t bytesReceived, char* buffer){
    if(!validatePacket(bytesReceived, PACKET_LAP_DATA_SIZE, "PacketLapData"))
        return std::nullopt;

    PacketLapData lapData;
    std::memcpy(&lapData, buffer, sizeof(PacketLapData));

    return lapData;
}

std::optional<PacketEventData> PacketHandlers::handlePacketEventData(ssize_t bytesReceived, char* buffer){
    if(!validatePacket(bytesReceived, PACKET_EVENT_DATA_SIZE, "PacketEventData"))
        return std::nullopt;
    
    PacketEventData eventData;
    std::memcpy(&eventData, buffer, sizeof(PacketEventData));

    return eventData;
}