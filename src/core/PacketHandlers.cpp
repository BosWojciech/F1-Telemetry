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

std::optional<PacketMotionData> PacketHandlers::handlePacketMotionData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_MOTION_DATA_SIZE, "PacketMotionData"))
        return std::nullopt;

    PacketMotionData motionData;
    std::memcpy(&motionData, buffer, sizeof(PacketMotionData));

    return motionData;
}

std::optional<PacketSessionData> PacketHandlers::handlePacketSessionData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_SESSION_DATA_SIZE, "PacketSessionData"))
        return std::nullopt;

    PacketSessionData sessionData;
    std::memcpy(&sessionData, buffer, sizeof(PacketSessionData));

    return sessionData;
}

std::optional<PacketLapData> PacketHandlers::handlePacketLapData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_LAP_DATA_SIZE, "PacketLapData"))
        return std::nullopt;

    PacketLapData lapData;
    std::memcpy(&lapData, buffer, sizeof(PacketLapData));

    return lapData;
}

std::optional<PacketEventData> PacketHandlers::handlePacketEventData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_EVENT_DATA_SIZE, "PacketEventData"))
        return std::nullopt;

    PacketEventData eventData;
    std::memcpy(&eventData, buffer, sizeof(PacketEventData));

    return eventData;
}

std::optional<PacketParticipantsData> PacketHandlers::handlePacketParticipantsData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_PARTICIPANTS_DATA_SIZE, "PacketParticipantsData"))
        return std::nullopt;

    PacketParticipantsData participantsData;
    std::memcpy(&participantsData, buffer, sizeof(PacketParticipantsData));

    return participantsData;
}

std::optional<PacketCarTelemetryData> PacketHandlers::handlePacketCarTelemetryData(ssize_t bytesReceived, char *buffer)
{
    if (!validatePacket(bytesReceived, PACKET_CAR_TELEMETRY_DATA_SIZE, "PacketCarTelemetryData"))
        return std::nullopt;

    PacketCarTelemetryData telemetryData;
    std::memcpy(&telemetryData, buffer, sizeof(PacketCarTelemetryData));

    return telemetryData;
}

std::optional<PacketCarStatusData> PacketHandlers::handlePacketCarStatusData(ssize_t bytesReceived, char *buffer){
    if(!validatePacket(bytesReceived, PACKET_CAR_STATUS_DATA_SIZE, "PacketCarStatusData"))
        return std::nullopt;

    PacketCarStatusData statusData;
    std::memcpy(&statusData, buffer, sizeof(PacketCarStatusData));
    return statusData;
}

std::optional<PacketCarDamageData> PacketHandlers::handlePacketCarDamageData(ssize_t bytesReceived, char *buffer){
    if(!validatePacket(bytesReceived, PACKET_CAR_DAMAGE_DATA_SIZE, "PacketCarDamageData"))
        return std::nullopt;

    PacketCarDamageData damageData;
    std::memcpy(&damageData, buffer, sizeof(PacketCarDamageData));
    return damageData;
}

std::optional<PacketSessionHistoryData> PacketHandlers::handlePacketSessionHistoryData(ssize_t bytesReceived, char *buffer){
    if(!validatePacket(bytesReceived, PACKET_SESSION_HISTORY_DATA_SIZE, "PacketSessionHistoryData"))
        return std::nullopt;

    PacketSessionHistoryData historyData;
    std::memcpy(&historyData, buffer, sizeof(PacketSessionHistoryData));
    return historyData;
}

std::optional<PacketTyreSetsData> PacketHandlers::handlePacketTyreSetsData(ssize_t bytesReceived, char *buffer){
    if(!validatePacket(bytesReceived, PACKET_TYRE_SETS_DATA_SIZE, "PacketTyreSetsData"))
        return std::nullopt;

    PacketTyreSetsData tyreSetsData;
    std::memcpy(&tyreSetsData, buffer, sizeof(PacketTyreSetsData));
    return tyreSetsData;
}