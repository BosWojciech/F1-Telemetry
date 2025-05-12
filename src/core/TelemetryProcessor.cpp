#include "core/TelemetryProcessor.h"
#include "core/DataTypes.h"
#include "nlohmann/json.hpp"

namespace TelemetryProcessor {

    nlohmann::json processPacketHeader(const PacketHeader& header){
        nlohmann::json jsonHeader;
        jsonHeader["gameYear"] = header.gameYear;
        jsonHeader["packetId"] = header.packetId;
        jsonHeader["sessionUID"] = header.sessionUID;
        jsonHeader["sessionTime"] = header.sessionTime;
        jsonHeader["playerCarIndex"] = header.playerCarIndex;

        return jsonHeader;
    }

    nlohmann::json processPacketMotionData(const PacketMotionData& data) {
        nlohmann::json jsonMotionData;
        jsonMotionData["header"] = processPacketHeader(data.header);

        nlohmann::json carsArray = nlohmann::json::array();

        for (const CarMotionData& carMotion : data.carMotionData) {
            nlohmann::json carJson;
            carJson["worldPositionX"] = carMotion.worldPositionX;
            carJson["worldPositionY"] = carMotion.worldPositionY;
            carJson["worldPositionZ"] = carMotion.worldPositionZ;

            carsArray.push_back(carJson);
        }

        jsonMotionData["cars"] = carsArray;
        return jsonMotionData;
    }




} // namespace TelemetryProcessor