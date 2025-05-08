#ifndef F1TELEMETRY_TELEMETRYPROCESSOR_H
#define F1TELEMETRY_TELEMETRYPROCESSOR_H

#include "nlohmann/json.hpp"
#include "DataTypes.h"

namespace TelemetryProcessor {

nlohmann::json processPacketMotionData(const PacketMotionData& data);
nlohmann::json processPacketCarTelemetryData(const PacketCarTelemetryData& data);

}
#endif // F1TELEMETRY_TELEMETRYPROCESSOR_H