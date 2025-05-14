#include "core/TelemetryProcessor.h"
#include "core/DataTypes.h"
#include "core/DataMaps.h"
#include "nlohmann/json.hpp"
#include <unordered_map>

#pragma region processPacketHeader

/**
 * @brief Converts the packet header to a JSON object.
 *
 * @param header The packet header received from the telemetry stream.
 * @return A JSON object containing the basic metadata of the packet.
 */
nlohmann::json TelemetryProcessor::processPacketHeader(const PacketHeader &header)
{
    nlohmann::json jsonHeader;
    jsonHeader["gameYear"] = header.gameYear;
    jsonHeader["packetId"] = header.packetId;
    jsonHeader["sessionUID"] = header.sessionUID;
    jsonHeader["sessionTime"] = header.sessionTime;
    jsonHeader["playerCarIndex"] = header.playerCarIndex;

    return jsonHeader;
}

#pragma endregion

#pragma region processPacketMotionData
/**
 * @brief Converts the vehicle motion data to a JSON object.
 *
 * @param data The PacketMotionData struct containing all necessary data
 * @return A JSON object containing only selected pieces of data.
 */
nlohmann::json TelemetryProcessor::processPacketMotionData(const PacketMotionData &data)
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

#pragma endregion

#pragma region processPacketSessionData
/**
 * @brief Converts the game session data to a JSON object.
 *
 * @param data The PacketSessionData struct containing all necessary data
 * @return A JSON object containing only selected pieces of data.
 */
nlohmann::json TelemetryProcessor::processPacketSessionData(const PacketSessionData &data)
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

    nlohmann::json weatherArray = nlohmann::json::array();
    for (const WeatherForecastSample &weatherData : data.weatherForecastSamples)
    {
        nlohmann::json weatherForecastSample;
        weatherForecastSample["sessionType"] = mapLookup(sessionTypeMap, static_cast<int>(weatherData.sessionType));
        weatherForecastSample["timeOffset"] = weatherData.timeOffset;
        weatherForecastSample["weather"] = mapLookup(weatherMap, static_cast<int>(weatherData.weather));
        weatherForecastSample["trackTemperature"] = weatherData.trackTemperature;
        weatherForecastSample["trackTemperatureChange"] = mapLookup(temperatureChangeMap, static_cast<int>(weatherData.trackTemperatureChange));
        weatherForecastSample["airTemperature"] = weatherData.airTemperature;
        weatherForecastSample["airTemperatureChange"] = mapLookup(temperatureChangeMap, static_cast<int>(weatherData.airTemperatureChange));
        weatherForecastSample["rainPercentage"] = weatherData.rainPercentage;

        weatherArray.push_back(weatherForecastSample);
    }

    jsonSessionData["pitStopWindowIdealLap"] = data.pitStopWindowIdealLap;
    jsonSessionData["pitStopRejoinPosition"] = data.pitStopRejoinPosition;

    return jsonSessionData;
}

#pragma endregion

#pragma region processPacketLapData

/**
 * @brief Converts the lap data to a JSON object.
 *
 * @param data The PacketLapData struct containing all necessary data
 * @return A JSON object containing only selected pieces of data.
 */
nlohmann::json TelemetryProcessor::processPacketLapData(const PacketLapData &data)
{
    nlohmann::json jsonLapData;
    jsonLapData["header"] = processPacketHeader(data.header);

    nlohmann::json carsData = nlohmann::json::array();

    for (const LapData &lapData : data.lapData)
    {
        nlohmann::json specificLapData;
        specificLapData["lastLapTimeInMS"] = lapData.lastLapTimeInMS;
        specificLapData["currentLapTimeInMS"] = lapData.currentLapTimeInMS;
        specificLapData["sector1TimeInMS"] = lapData.sector1TimeInMS;
        specificLapData["sector2TimeInMS"] = lapData.sector2TimeInMS;
        specificLapData["deltaToCarInFrontInMS"] = lapData.deltaToCarInFrontInMS;
        specificLapData["deltaToRaceLeaderInMS"] = lapData.deltaToRaceLeaderInMS;
        specificLapData["safetCarDelta"] = lapData.safetyCarDelta;
        specificLapData["carPosition"] = lapData.carPosition;
        specificLapData["currentLapNum"] = lapData.currentLapNum;
        specificLapData["pitStatus"] = mapLookup(pitStatusMap, static_cast<int>(lapData.pitStatus));
        specificLapData["numPitStops"] = lapData.numPitStops;
        specificLapData["sector"] = mapLookup(sectorMap, static_cast<int>(lapData.sector));
        specificLapData["currentLapInvalid"] = mapLookup(lapInvalidMap, static_cast<int>(lapData.currentLapInvalid));
        specificLapData["penalties"] = lapData.penalties;
        specificLapData["totalWarnings"] = lapData.totalWarnings;
        specificLapData["cornerCuttingWarnings"] = lapData.cornerCuttingWarnings;
        specificLapData["numUnservedDriveThroughPens"] = lapData.numUnservedDriveThroughPens;
        specificLapData["numUnservedStopGoPens"] = lapData.numUnservedStopGoPens;
        specificLapData["gridPosition"] = lapData.gridPosition;
        specificLapData["resultStatus"] = mapLookup(resultStatusMap, static_cast<int>(lapData.resultStatus));
        specificLapData["pitLaneTimeInLaneInMS"] = lapData.pitLaneTimeInLaneInMS;
        specificLapData["pitStopTimerInMS"] = lapData.pitStopTimerInMS;
        specificLapData["pitStopShouldServePen"] = mapLookup(pitShouldServePenMap, static_cast<int>(lapData.pitStopShouldServePen));

        carsData.push_back(specificLapData);
    }

    jsonLapData["cars"] = carsData;
    jsonLapData["timeTrialPBCarIdx"] = data.timeTrialPBCarIdx;

    return jsonLapData;
}

#pragma endregion

#pragma region processPacketEventData

/**
 * @brief Converts the event code to json containing data about event
 *
 * @param code 4 character code of event
 * @param data EventDataDetails struct containing event's data
 * @return A JSON object containing only selected pieces of event's data.
 */
nlohmann::json TelemetryProcessor::eventPacketParser(const std::string &code, const EventDataDetails &data)
{
    EventType event = eventTypeFromCode(code);
    nlohmann::json payload;

    switch (event)
    {
    case EventType::SessionStarted:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::SessionEnded:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::FastestLap:
    {
        payload["vehicleIdx"] = data.FastestLap.vehicleIdx;
        payload["lapTime"] = data.FastestLap.lapTime;
        return payload;
    }
    case EventType::Retirement:
    {
        payload["vehicleIdx"] = data.Retirement.vehicleIdx;
        return payload;
    }
    case EventType::DRSEnabled:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::DRSDisabled:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::TeamMateInPits:
    {
        payload["vehicleIdx"] = data.TeamMateInPits.vehicleIdx;
        return payload;
    }
    case EventType::ChequeredFlag:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::RaceWinner:
    {
        payload["vehicleIdx"] = data.RaceWinner.vehicleIdx;
        return payload;
    }
    case EventType::PenaltyIssued:
    {
        payload["penaltyType"] = mapLookup(penaltyTypeMap, static_cast<int>(data.Penalty.penaltyType));
        payload["infringementType"] = mapLookup(infringementTypes, static_cast<int>(data.Penalty.infringementType));
        payload["vehicleIdx"] = data.Penalty.vehicleIdx;
        payload["otherVehicleIdx"] = data.Penalty.otherVehicleIdx;
        payload["timeGained"] = data.Penalty.time;
        payload["lapNum"] = data.Penalty.lapNum;
        payload["placesGained"] = data.Penalty.placesGained;
        return payload;
    }
    case EventType::SpeedTrapTriggered:
    {
        payload["vehicleIdx"] = data.SpeedTrap.vehicleIdx;
        payload["speed"] = data.SpeedTrap.speed;
        payload["isOverallFastestInSession"] = data.SpeedTrap.isOverallFastestInSession;
        payload["isDriverFastestInSession"] = data.SpeedTrap.isDriverFastestInSession;
        payload["fastestVehicleIdxInSession"] = data.SpeedTrap.fastestVehicleIdxInSession;
        payload["fastestSpeedInSession"] = data.SpeedTrap.fastestSpeedInSession;
        return payload;
    }
    case EventType::StartLight:
    {
        payload["numLights"] = data.StartLights.numLights;
        return payload;
    }
    case EventType::LightsOut:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::DriveThroughServed:
    {
        payload["vehicleIdx"] = data.DriveThroughPenaltyServed.vehicleIdx;
        return payload;
    }
    case EventType::StopGoServed:
    {
        payload["vehicleIdx"] = data.StopGoPenaltyServed.vehicleIdx;
        return payload;
    }
    case EventType::Flashback:
    {
        payload["flashbackFrameIdentifier"] = data.Flashback.flashbackFrameIdentifier;
        payload["flashbackSessionTime"] = data.Flashback.flashbackSessionTime;
        return payload;
    }
    case EventType::ButtonStatus:
    {
        payload["button"] = mapLookup(buttonFlagsMap, data.Buttons.buttonStatus);
        return payload;
    }
    case EventType::RedFlag:
    {
        payload["data"] = true;
        return payload;
    }
    case EventType::Overtake:
    {
        payload["overtakingVehicleIdx"] = data.Overtake.overtakingVehicleIdx;
        payload["beingOvertakenVehicleIdx"] = data.Overtake.beingOvertakenVehicleIdx;
        return payload;
    }
    default:
    {
        payload["Unknown"] = "Unknown";
        return payload;
    }
    }
}

/**
 * @brief Converts the event data to a JSON object.
 *
 * @param data The PacketEventData struct containing all necessary data
 * @return A JSON object containing only selected pieces of data.
 */
nlohmann::json TelemetryProcessor::processPacketEventData(const PacketEventData &data)
{
    nlohmann::json jsonEventData;
    jsonEventData["header"] = processPacketHeader(data.header);

    std::string eventCode = std::string(reinterpret_cast<const char *>(data.eventStringCode), 4);
    jsonEventData["type"] = mapLookup(eventTypeMap, eventCode);

    jsonEventData["payload"] = eventPacketParser(eventCode, data.eventDetails);
    return jsonEventData;
}

#pragma endregion

#pragma region processPacketParticipantsData

/**
 * @brief Converts the game participants data to a JSON object.
 *
 * @param data The PacketParticipantsData struct containing all necessary data
 * @return A JSON object containing only selected pieces of data.
 */
nlohmann::json TelemetryProcessor::processPacketParticipantsData(const PacketParticipantsData &data)
{
    nlohmann::json jsonParticipantsData;
    jsonParticipantsData["header"] = processPacketHeader(data.header);
    jsonParticipantsData["numActiveCars"] = data.numActiveCars;

    nlohmann::json participants = nlohmann::json::array();

    for (const ParticipantData &participantData : data.participants)
    {
        nlohmann::json participant;

        if (participantData.driverId == 255)
        {
            participant["driverName"] = mapLookup(driverIdsMap, static_cast<int>(participantData.driverId));
            participant["teamId"] = mapLookup(teamIdMap, static_cast<int>(participantData.teamId));
            participant["carRaceNumber"] = participantData.raceNumber;
            participant["nationality"] = mapLookup(nationalityIdMap, static_cast<int>(participantData.nationality));
        }
        else
        {
            participant["driverName"] = participantData.name;
            participant["networkId"] = participantData.networkId;
            participant["teamId"] = mapLookup(teamIdMap, static_cast<int>(participantData.teamId));
            participant["carRaceNumber"] = participantData.raceNumber;
            participant["nationality"] = mapLookup(nationalityIdMap, static_cast<int>(participantData.nationality));
        }

        participants.push_back(participant);
    }

    jsonParticipantsData["participants"] = participants;
    return jsonParticipantsData;
}

#pragma endregion