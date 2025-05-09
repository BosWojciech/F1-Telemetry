#ifndef F1TELEMETRY_PACKET_HANDLERS_H
#define F1TELEMETRY_PACKET_HANDLERS_H

#include "DataTypes.h"

namespace PacketHandlers
{

    // validation method
    bool validatePacket(ssize_t bytesReceived, size_t correctSize, std::string name);

    // packet handlers
    PacketMotionData handlePacketMotionData(ssize_t bytesReceived, char *buffer);
    PacketCarTelemetryData handlePacketCarTelemetryData(ssize_t bytesReceived, char *buffer);

}
#endif // F1TELEMETRY_PACKET_HANDLERS_H