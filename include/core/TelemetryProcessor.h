#ifndef F1TELEMETRY_TELEMETRYPROCESSOR_H
#define F1TELEMETRY_TELEMETRYPROCESSOR_H

#include <iostream>
#include <unordered_map>
#include "nlohmann/json.hpp"
#include "DataTypes.h"

namespace TelemetryProcessor
{

    template <typename K, typename V>
    std::string mapLookup(const std::unordered_map<K, V> &map, K key, const std::string &defaultValue = "unknown")
    {
        auto it = map.find(key);
        return it != map.end() ? it->second : defaultValue;
    }

    nlohmann::json eventPacketParser(const std::string &code, const EventDataDetails &data);
    nlohmann::json processPacketHeader(const PacketHeader &header);
    nlohmann::json processPacketMotionData(const PacketMotionData &data);
    nlohmann::json processPacketSessionData(const PacketSessionData &data);
    nlohmann::json processPacketLapData(const PacketLapData &data);
    nlohmann::json processPacketEventData(const PacketEventData &data);
    nlohmann::json processPacketParticipantsData(const PacketParticipantsData &data);

}
#endif // F1TELEMETRY_TELEMETRYPROCESSOR_H