#ifndef F1TELEMETRY_PACKET_HANDLERS_H
#define F1TELEMETRY_PACKET_HANDLERS_H

#include "DataTypes.h"
#include <optional>

namespace PacketHandlers
{

    // validation method
    bool validatePacket(ssize_t bytesReceived, size_t correctSize, std::string name);

    // packet handlers
    std::optional<PacketMotionData> handlePacketMotionData(ssize_t bytesReceived, char *buffer);
    std::optional<PacketCarTelemetryData> handlePacketCarTelemetryData(ssize_t bytesReceived, char *buffer);

}
#endif // F1TELEMETRY_PACKET_HANDLERS_H