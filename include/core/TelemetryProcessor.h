#ifndef F1TELEMETRY_TELEMETRYPROCESSOR_H
#define F1TELEMETRY_TELEMETRYPROCESSOR_H

#include <iostream>
#include <unordered_map>
#include "nlohmann/json.hpp"
#include "DataTypes.h"

namespace TelemetryProcessor
{

    static const std::unordered_map<int, std::string> weatherMap;
    static const std::unordered_map<int, std::string> sessionTypeMap;
    static const std::unordered_map<int, std::string> trackIdMap;
    static const std::unordered_map<int, std::string> safetyCarStatusMap;

    template <typename K, typename V>
    std::string mapLookup(const std::unordered_map<K, V>& map, K key, const std::string& defaultValue = "unknown") {
        auto it = map.find(key);
        return it != map.end() ? it->second : defaultValue;
    }

    nlohmann::json processPacketHeader(const PacketHeader &header);
    nlohmann::json processPacketMotionData(const PacketMotionData &data);
    nlohmann::json processPacketSessionData(const PacketSessionData &data);

}
#endif // F1TELEMETRY_TELEMETRYPROCESSOR_H