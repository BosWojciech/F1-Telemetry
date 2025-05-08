#include "core/TelemetryProcessor.h"
#include "core/DataTypes.h"
#include "nlohmann/json.hpp"

namespace TelemetryProcessor {

nlohmann::json processPacketMotionData(const PacketMotionData& data) {
    nlohmann::json jsonMotionData;
    nlohmann::json carsArray = nlohmann::json::array();

    for (const CarMotionData& carMotion : data.m_carMotionData) {
        nlohmann::json carJson;
        carJson["m_worldPositionX"] = carMotion.m_worldPositionX;
        carJson["m_worldPositionY"] = carMotion.m_worldPositionY;
        carJson["m_worldPositionZ"] = carMotion.m_worldPositionZ;

        carsArray.push_back(carJson);
    }

    jsonMotionData["cars"] = carsArray;
    return jsonMotionData;
}

nlohmann::json processPacketCarTelemetryData(const PacketCarTelemetryData& data) {
    nlohmann::json jsonTelemetryData;
    nlohmann::json carsArray = nlohmann::json::array();

    for (const CarTelemetryData& carTelemetry : data.m_carTelemetryData) {
        nlohmann::json carJson;
        carJson["throttle"] = carTelemetry.m_throttle;
        carJson["brake"] = carTelemetry.m_brake;

        carsArray.push_back(carJson);
    }

    jsonTelemetryData["cars"] = carsArray;
    return jsonTelemetryData;
}


} // namespace TelemetryProcessor