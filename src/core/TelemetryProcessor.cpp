#include "core/TelemetryProcessor.h"
#include "core/DataTypes.h"
#include "nlohmann/json.hpp"
#include <unordered_map>

namespace TelemetryProcessor
{

    // unordered maps for replacing numerical to string data
    static const std::unordered_map<int, std::string> weatherMap = {
        {0, "clear"},
        {1, "light cloud"},
        {2, "overcast"},
        {3, "light rain"},
        {4, "heavy rain"},
        {5, "storm"}};

    static const std::unordered_map<int, std::string> sessionTypeMap = {
        {0, "unknown"},
        {1, "P1"},
        {2, "P2"},
        {3, "P3"},
        {4, "Short P"},
        {5, "Q1"},
        {6, "Q2"},
        {7, "Q3"},
        {8, "Short Q"},
        {9, "OSQ"},
        {10, "R"},
        {11, "R2"},
        {12, "R3"},
        {13, "Time Trial"}};

    static const std::unordered_map<int, std::string> trackIdMap = {
        {0, "Melbourne"},
        {1, "Paul Ricard"},
        {2, "Shanghai"},
        {3, "Sakhir (Bahrain)"},
        {4, "Catalunya"},
        {5, "Monaco"},
        {6, "Montreal"},
        {7, "Silverstone"},
        {8, "Hockenheim"},
        {9, "Hungaroring"},
        {10, "Spa"},
        {11, "Monza"},
        {12, "Singapore"},
        {13, "Suzuka"},
        {14, "Abu Dhabi"},
        {15, "Texas"},
        {16, "Brazil"},
        {17, "Austria"},
        {18, "Sochi"},
        {19, "Mexico"},
        {20, "Baku (Azerbaijan)"},
        {21, "Sakhir Short"},
        {22, "Silverstone Short"},
        {23, "Texas Short"},
        {24, "Suzuka Short"},
        {25, "Hanoi"},
        {26, "Zandvoort"},
        {27, "Imola"},
        {28, "Portimão"},
        {29, "Jeddah"},
        {30, "Miami"},
        {31, "Las Vegas"},
        {32, "Losail"}};

    static const std::unordered_map<int, std::string> safetyCarStatusMap = {
        {0, "no safety car"},
        {1, "full safety car"},
        {2, "virtual safety car"},
        {3, "formation lap"}};

    nlohmann::json processPacketHeader(const PacketHeader &header)
    {
        nlohmann::json jsonHeader;
        jsonHeader["gameYear"] = header.gameYear;
        jsonHeader["packetId"] = header.packetId;
        jsonHeader["sessionUID"] = header.sessionUID;
        jsonHeader["sessionTime"] = header.sessionTime;
        jsonHeader["playerCarIndex"] = header.playerCarIndex;

        return jsonHeader;
    }

    nlohmann::json processPacketMotionData(const PacketMotionData &data)
    {
        nlohmann::json jsonMotionData;
        jsonMotionData["header"] = processPacketHeader(data.header);

        nlohmann::json carsArray = nlohmann::json::array();

        for (const CarMotionData &carMotion : data.carMotionData)
        {
            nlohmann::json carJson;
            carJson["worldPositionX"] = carMotion.worldPositionX;
            carJson["worldPositionY"] = carMotion.worldPositionY;
            carJson["worldPositionZ"] = carMotion.worldPositionZ;

            carsArray.push_back(carJson);
        }

        jsonMotionData["cars"] = carsArray;
        return jsonMotionData;
    }

    nlohmann::json processPacketSessionData(const PacketSessionData &data)
    {
        nlohmann::json jsonSessionData;
        jsonSessionData["header"] = processPacketHeader(data.header);
        jsonSessionData["weather"] = mapLookup(weatherMap, static_cast<int>(data.weather));
        jsonSessionData["trackTemperature"] = data.trackTemperature;
        jsonSessionData["airTemperature"] = data.airTemperature;
        jsonSessionData["totalLaps"] = data.totalLaps;
        jsonSessionData["sessionType"] = mapLookup(sessionTypeMap, static_cast<int>(data.sessionType));
        jsonSessionData["trackId"] = mapLookup(trackIdMap, static_cast<int>(data.trackId));
        jsonSessionData["sessionTimeLeft"] = data.sessionTimeLeft;
        jsonSessionData["sessionDuration"] = data.sessionDuration;
        jsonSessionData["safetyCarStatus"] = mapLookup(safetyCarStatusMap, static_cast<int>(data.safetyCarStatus));
        jsonSessionData["numWeatherForecastSamples"] = data.numWeatherForecastSamples;
        // TODO weather forecast

        jsonSessionData["pitStopWindowIdealLap"] = data.pitStopWindowIdealLap;
        jsonSessionData["pitStopRejoinPosition"] = data.pitStopRejoinPosition;

        return jsonSessionData;
    }

} // namespace TelemetryProcessor