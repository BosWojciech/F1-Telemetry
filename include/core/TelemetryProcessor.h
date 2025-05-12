#ifndef F1TELEMETRY_TELEMETRYPROCESSOR_H
#define F1TELEMETRY_TELEMETRYPROCESSOR_H

#include "nlohmann/json.hpp"
#include "DataTypes.h"

namespace TelemetryProcessor {

    nlohmann::json processPacketHeader(const PacketHeader& header);
    nlohmann::json processPacketMotionData(const PacketMotionData& data);

}
#endif // F1TELEMETRY_TELEMETRYPROCESSOR_H