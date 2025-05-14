#ifndef F1TELEMETRY_TELEMETRYPROCESSOR_H
#define F1TELEMETRY_TELEMETRYPROCESSOR_H

#include <iostream>
#include <unordered_map>
#include "nlohmann/json.hpp"
#include "DataTypes.h"

namespace TelemetryProcessor
{

    enum class EventType
    {
        SessionStarted,
        SessionEnded,
        FastestLap,
        Retirement,
        DRSEnabled,
        DRSDisabled,
        TeamMateInPits,
        ChequeredFlag,
        RaceWinner,
        PenaltyIssued,
        SpeedTrapTriggered,
        StartLight,
        LightsOut,
        DriveThroughServed,
        StopGoServed,
        Flashback,
        ButtonStatus,
        RedFlag,
        Overtake,
        Unknown
    };

    template <typename K, typename V>
    std::string mapLookup(const std::unordered_map<K, V> &map, K key, const std::string &defaultValue = "unknown")
    {
        auto it = map.find(key);
        return it != map.end() ? it->second : defaultValue;
    }

    EventType eventTypeFromCode(const std::string &code)
    {
        const std::unordered_map<std::string, EventType> eventMap = {
            {"SSTA", EventType::SessionStarted},
            {"SEND", EventType::SessionEnded},
            {"FTLP", EventType::FastestLap},
            {"RTMT", EventType::Retirement},
            {"DRSE", EventType::DRSEnabled},
            {"DRSD", EventType::DRSDisabled},
            {"TMPT", EventType::TeamMateInPits},
            {"CHQF", EventType::ChequeredFlag},
            {"RCWN", EventType::RaceWinner},
            {"PENA", EventType::PenaltyIssued},
            {"SPTP", EventType::SpeedTrapTriggered},
            {"STLG", EventType::StartLight},
            {"LGOT", EventType::LightsOut},
            {"DTSV", EventType::DriveThroughServed},
            {"SGSV", EventType::StopGoServed},
            {"FLBK", EventType::Flashback},
            {"BUTN", EventType::ButtonStatus},
            {"RDFL", EventType::RedFlag},
            {"OVTK", EventType::Overtake}};

        auto it = eventMap.find(code);
        return it != eventMap.end() ? it->second : EventType::Unknown;
    }

    static const std::unordered_map<int, std::string> weatherMap;
    static const std::unordered_map<int, std::string> sessionTypeMap;
    static const std::unordered_map<int, std::string> trackIdMap;
    static const std::unordered_map<int, std::string> safetyCarStatusMap;
    static const std::unordered_map<int, std::string> temperatureChangeMap;
    static const std::unordered_map<int, std::string> pitStatusMap;
    static const std::unordered_map<int, std::string> sectorMap;
    static const std::unordered_map<int, std::string> lapInvalidMap;
    static const std::unordered_map<int, std::string> resultStatusMap;
    static const std::unordered_map<int, std::string> pitShouldServePenMap;
    static const std::unordered_map<std::string, std::string> eventTypeMap;
    static const std::unordered_map<int, std::string> penaltyTypeMap;
    static const std::unordered_map<int, std::string> infringementTypes;
    static const std::unordered_map<uint32_t, std::string> buttonFlagsMap;
    static const std::unordered_map<int, std::string> driverIdsMap;
    static const std::unordered_map<int, std::string> teamIdMap;
    static const std::unordered_map<int, std::string> TelemetryProcessor::nationalityIdMap;

    nlohmann::json eventPacketParser(const std::string &code, const EventDataDetails &data);
    nlohmann::json processPacketHeader(const PacketHeader &header);
    nlohmann::json processPacketMotionData(const PacketMotionData &data);
    nlohmann::json processPacketSessionData(const PacketSessionData &data);
    nlohmann::json processPacketLapData(const PacketLapData &data);
    nlohmann::json processPacketEventData(const PacketEventData &data);
    nlohmann::json processPacketParticipantsData(const PacketParticipantsData &data);
    
}
#endif // F1TELEMETRY_TELEMETRYPROCESSOR_H