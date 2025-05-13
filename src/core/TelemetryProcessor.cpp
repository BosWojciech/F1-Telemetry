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
    
    static const std::unordered_map<int, std::string> temperatureChangeMap = {
        {0, "up"},
        {1, "down"},
        {2, "no change"}
    };

    static const std::unordered_map<int, std::string> safetyCarStatusMap = {
        {0, "no safety car"},
        {1, "full safety car"},
        {2, "virtual safety car"},
        {3, "formation lap"}};

    static const std::unordered_map<int, std::string> TelemetryProcessor::pitStatusMap = {
        {0, "none"},
        {1, "pitting"},
        {2, "in pit area"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::sectorMap = {
        {0, "sector1"},
        {1, "sector2"},
        {2, "sector3"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::lapInvalidMap = {
        {0, "valid"},
        {1, "invalid"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::resultStatusMap = {
        {0, "invalid"},
        {1, "inactive"},
        {2, "active"},
        {3, "finished"},
        {4, "DNF"},
        {5, "DSQ"},
        {6, "Not Classified"},
        {7, "Retired"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::pitShouldServePenMap = {
        {0, "no"},
        {1, "yes"}
    };

    static const std::unordered_map<std::string, std::string> TelemetryProcessor::eventTypeMap = {
        {"SSTA", "SessionStarted"},
        {"SEND", "SessionEnded"},
        {"FTLP", "FastestLap"},
        {"RTMT", "Retirement"},
        {"DRSE", "DRSEnabled"},
        {"DRSD", "DRSDisabled"},
        {"TMPT", "TeamMateInPits"},
        {"CHQF", "ChequeredFlag"},
        {"RCWN", "RaceWinner"},
        {"PENA", "PenaltyIssued"},
        {"SPTP", "SpeedTrapTriggered"},
        {"STLG", "StartLight"},
        {"LGOT", "LightsOut"},
        {"DTSV", "DriveThroughServed"},
        {"SGSV", "StopGoServed"},
        {"FLBK", "Flashback"},
        {"BUTN", "ButtonStatus"},
        {"RDFL", "RedFlag"},
        {"OVTK", "Overtake"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::penaltyTypeMap = {
        {0, "Drive Through"},
        {1, "Stop Go"},
        {2, "Grid Penalty"},
        {3, "Penalty Reminder"},
        {4, "Time Penalty"},
        {5, "Warning"},
        {6, "Disqualified"},
        {7, "Removed From Formation Lap"},
        {8, "Parked Too Long Timer"},
        {9, "Tyre Regulations"},
        {10, "This Lap Invalidated"},
        {11, "This And Next Lap Invalidated"},
        {12, "This Lap Invalidated Without Reason"},
        {13, "This And Next Lap Invalidated Without Reason"},
        {14, "This And Previous Lap Invalidated"},
        {15, "This And Previous Lap Invalidated Without Reason"},
        {16, "Retired"},
        {17, "Black Flag Timer"}
    };

    static const std::unordered_map<int, std::string> TelemetryProcessor::infringementTypes = {
        {0, "Blocking by slow driving"},
        {1, "Blocking by wrong way driving"},
        {2, "Reversing off the start line"},
        {3, "Big Collision"},
        {4, "Small Collision"},
        {5, "Collision failed to hand back position single"},
        {6, "Collision failed to hand back position multiple"},
        {7, "Corner cutting gained time"},
        {8, "Corner cutting overtake single"},
        {9, "Corner cutting overtake multiple"},
        {10, "Crossed pit exit lane"},
        {11, "Ignoring blue flags"},
        {12, "Ignoring yellow flags"},
        {13, "Ignoring drive through"},
        {14, "Too many drive throughs"},
        {15, "Drive through reminder serve within n laps"},
        {16, "Drive through reminder serve this lap"},
        {17, "Pit lane speeding"},
        {18, "Parked for too long"},
        {19, "Ignoring tyre regulations"},
        {20, "Too many penalties"},
        {21, "Multiple warnings"},
        {22, "Approaching disqualification"},
        {23, "Tyre regulations select single"},
        {24, "Tyre regulations select multiple"},
        {25, "Lap invalidated corner cutting"},
        {26, "Lap invalidated running wide"},
        {27, "Corner cutting ran wide gained time minor"},
        {28, "Corner cutting ran wide gained time significant"},
        {29, "Corner cutting ran wide gained time extreme"},
        {30, "Lap invalidated wall riding"},
        {31, "Lap invalidated flashback used"},
        {32, "Lap invalidated reset to track"},
        {33, "Blocking the pitlane"},
        {34, "Jump start"},
        {35, "Safety car to car collision"},
        {36, "Safety car illegal overtake"},
        {37, "Safety car exceeding allowed pace"},
        {38, "Virtual safety car exceeding allowed pace"},
        {39, "Formation lap below allowed speed"},
        {40, "Formation lap parking"},
        {41, "Retired mechanical failure"},
        {42, "Retired terminally damaged"},
        {43, "Safety car falling too far back"},
        {44, "Black flag timer"},
        {45, "Unserved stop go penalty"},
        {46, "Unserved drive through penalty"},
        {47, "Engine component change"},
        {48, "Gearbox change"},
        {49, "Parc Fermé change"},
        {50, "League grid penalty"},
        {51, "Retry penalty"},
        {52, "Illegal time gain"},
        {53, "Mandatory pitstop"},
        {54, "Attribute assigned"}
    };

    
    static const std::unordered_map<uint32_t, std::string> buttonFlagsMap = {
        {0x00000001, "Cross or A"},
        {0x00000002, "Triangle or Y"},
        {0x00000004, "Circle or B"},
        {0x00000008, "Square or X"},
        {0x00000010, "D-pad Left"},
        {0x00000020, "D-pad Right"},
        {0x00000040, "D-pad Up"},
        {0x00000080, "D-pad Down"},
        {0x00000100, "Options or Menu"},
        {0x00000200, "L1 or LB"},
        {0x00000400, "R1 or RB"},
        {0x00000800, "L2 or LT"},
        {0x00001000, "R2 or RT"},
        {0x00002000, "Left Stick Click"},
        {0x00004000, "Right Stick Click"},
        {0x00008000, "Right Stick Left"},
        {0x00010000, "Right Stick Right"},
        {0x00020000, "Right Stick Up"},
        {0x00040000, "Right Stick Down"},
        {0x00080000, "Special"},
        {0x00100000, "UDP Action 1"},
        {0x00200000, "UDP Action 2"},
        {0x00400000, "UDP Action 3"},
        {0x00800000, "UDP Action 4"},
        {0x01000000, "UDP Action 5"},
        {0x02000000, "UDP Action 6"},
        {0x04000000, "UDP Action 7"},
        {0x08000000, "UDP Action 8"},
        {0x10000000, "UDP Action 9"},
        {0x20000000, "UDP Action 10"},
        {0x40000000, "UDP Action 11"},
        {0x80000000, "UDP Action 12"}
    };

    static const std::unordered_map<int, std::string> driverIdsMap = {
        {0, "Carlos Sainz"},
        {1, "Daniil Kvyat"},
        {2, "Daniel Ricciardo"},
        {3, "Fernando Alonso"},
        {4, "Felipe Massa"},
        {6, "Kimi Räikkönen"},
        {7, "Lewis Hamilton"},
        {9, "Max Verstappen"},
        {10, "Nico Hulkenburg"},
        {11, "Kevin Magnussen"},
        {12, "Romain Grosjean"},
        {13, "Sebastian Vettel"},
        {14, "Sergio Perez"},
        {15, "Valtteri Bottas"},
        {17, "Esteban Ocon"},
        {19, "Lance Stroll"},
        {20, "Arron Barnes"},
        {21, "Martin Giles"},
        {22, "Alex Murray"},
        {23, "Lucas Roth"},
        {24, "Igor Correia"},
        {25, "Sophie Levasseur"},
        {26, "Jonas Schiffer"},
        {27, "Alain Forest"},
        {28, "Jay Letourneau"},
        {29, "Esto Saari"},
        {30, "Yasar Atiyeh"},
        {31, "Callisto Calabresi"},
        {32, "Naota Izum"},
        {33, "Howard Clarke"},
        {34, "Wilheim Kaufmann"},
        {35, "Marie Laursen"},
        {36, "Flavio Nieves"},
        {37, "Peter Belousov"},
        {38, "Klimek Michalski"},
        {39, "Santiago Moreno"},
        {40, "Benjamin Coppens"},
        {41, "Noah Visser"},
        {42, "Gert Waldmuller"},
        {43, "Julian Quesada"},
        {44, "Daniel Jones"},
        {45, "Artem Markelov"},
        {46, "Tadasuke Makino"},
        {47, "Sean Gelael"},
        {48, "Nyck De Vries"},
        {49, "Jack Aitken"},
        {50, "George Russell"},
        {51, "Maximilian Günther"},
        {52, "Nirei Fukuzumi"},
        {53, "Luca Ghiotto"},
        {54, "Lando Norris"},
        {55, "Sérgio Sette Câmara"},
        {56, "Louis Delétraz"},
        {57, "Antonio Fuoco"},
        {58, "Charles Leclerc"},
        {59, "Pierre Gasly"},
        {62, "Alexander Albon"},
        {63, "Nicholas Latifi"},
        {64, "Dorian Boccolacci"},
        {65, "Niko Kari"},
        {66, "Roberto Merhi"},
        {67, "Arjun Maini"},
        {68, "Alessio Lorandi"},
        {69, "Ruben Meijer"},
        {70, "Rashid Nair"},
        {71, "Jack Tremblay"},
        {72, "Devon Butler"},
        {73, "Lukas Weber"},
        {74, "Antonio Giovinazzi"},
        {75, "Robert Kubica"},
        {76, "Alain Prost"},
        {77, "Ayrton Senna"},
        {78, "Nobuharu Matsushita"},
        {79, "Nikita Mazepin"},
        {80, "Guanya Zhou"},
        {81, "Mick Schumacher"},
        {82, "Callum Ilott"},
        {83, "Juan Manuel Correa"},
        {84, "Jordan King"},
        {85, "Mahaveer Raghunathan"},
        {86, "Tatiana Calderon"},
        {87, "Anthoine Hubert"},
        {88, "Guiliano Alesi"},
        {89, "Ralph Boschung"},
        {90, "Michael Schumacher"},
        {91, "Dan Ticktum"},
        {92, "Marcus Armstrong"},
        {93, "Christian Lundgaard"},
        {94, "Yuki Tsunoda"},
        {95, "Jehan Daruvala"},
        {96, "Gulherme Samaia"},
        {97, "Pedro Piquet"},
        {98, "Felipe Drugovich"},
        {99, "Robert Schwartzman"},
        {100, "Roy Nissany"},
        {101, "Marino Sato"},
        {102, "Aidan Jackson"},
        {103, "Casper Akkerman"},
        {109, "Jenson Button"},
        {110, "David Coulthard"},
        {111, "Nico Rosberg"},
        {112, "Oscar Piastri"},
        {113, "Liam Lawson"},
        {114, "Juri Vips"},
        {115, "Theo Pourchaire"},
        {116, "Richard Verschoor"},
        {117, "Lirim Zendeli"},
        {118, "David Beckmann"},
        {121, "Alessio Deledda"},
        {122, "Bent Viscaal"},
        {123, "Enzo Fittipaldi"},
        {125, "Mark Webber"},
        {126, "Jacques Villeneuve"},
        {127, "Callie Mayer"},
        {128, "Noah Bell"},
        {129, "Jake Hughes"},
        {130, "Frederik Vesti"},
        {131, "Olli Caldwell"},
        {132, "Logan Sargeant"},
        {133, "Cem Bolukbasi"},
        {134, "Ayumu Iwasa"},
        {135, "Clement Novalak"},
        {136, "Jack Doohan"},
        {137, "Amaury Cordeel"},
        {138, "Dennis Hauger"},
        {139, "Calan Williams"},
        {140, "Jamie Chadwick"},
        {141, "Kamui Kobayashi"},
        {142, "Pastor Maldonado"},
        {143, "Mika Hakkinen"},
        {144, "Nigel Mansell"}
    };



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
        
        nlohmann::json weatherArray = nlohmann::json::array();
        for(const WeatherForecastSample& weatherData : data.weatherForecastSamples){
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

    nlohmann::json TelemetryProcessor::processPacketLapData(const PacketLapData &data){
        nlohmann::json jsonLapData;
        jsonLapData["header"] = processPacketHeader(data.header);

        nlohmann::json carsData = nlohmann::json::array();

        for(const LapData& lapData : data.lapData){
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

    nlohmann::json TelemetryProcessor::eventPacketParser(const std::string &code, const EventDataDetails &data){
        EventType event = eventTypeFromCode(code);
        nlohmann::json payload;

        switch(event){
            case EventType::SessionStarted:{
                payload["data"] = true;
                return payload;
            }
            case EventType::SessionEnded:{
                payload["data"] = true;
                return payload;
            }
            case EventType::FastestLap:{
                payload["vehicleIdx"] = data.FastestLap.vehicleIdx;
                payload["lapTime"] = data.FastestLap.lapTime;
                return payload;
            }
            case EventType::Retirement:{
                payload["vehicleIdx"] = data.Retirement.vehicleIdx;
                return payload;
            }
            case EventType::DRSEnabled:{
                payload["data"] = true;
                return payload;
            }
            case EventType::DRSDisabled:{
                payload["data"] = true;
                return payload;
            }
            case EventType::TeamMateInPits:{
                payload["vehicleIdx"] = data.TeamMateInPits.vehicleIdx;
                return payload;
            }
            case EventType::ChequeredFlag:{
                payload["data"] = true;
                return payload;
            }
            case EventType::RaceWinner:{
                payload["vehicleIdx"] = data.RaceWinner.vehicleIdx;
                return payload;
            }
            case EventType::PenaltyIssued:{
                payload["penaltyType"] = mapLookup(penaltyTypeMap, static_cast<int>(data.Penalty.penaltyType));
                payload["infringementType"] = mapLookup(infringementTypes, static_cast<int>(data.Penalty.infringementType));
                payload["vehicleIdx"] = data.Penalty.vehicleIdx;
                payload["otherVehicleIdx"] = data.Penalty.otherVehicleIdx;
                payload["timeGained"] = data.Penalty.time;
                payload["lapNum"] = data.Penalty.lapNum;
                payload["placesGained"] = data.Penalty.placesGained;
                return payload;
            }
            case EventType::SpeedTrapTriggered:{
                payload["vehicleIdx"] = data.SpeedTrap.vehicleIdx;
                payload["speed"] = data.SpeedTrap.speed;
                payload["isOverallFastestInSession"] = data.SpeedTrap.isOverallFastestInSession;
                payload["isDriverFastestInSession"] = data.SpeedTrap.isDriverFastestInSession;
                payload["fastestVehicleIdxInSession"] = data.SpeedTrap.fastestVehicleIdxInSession;
                payload["fastestSpeedInSession"] = data.SpeedTrap.fastestSpeedInSession;
                return payload;
            }
            case EventType::StartLight:{
                payload["numLights"] = data.StartLights.numLights;
                return payload;
            }
            case EventType::LightsOut:{
                payload["data"] = true;
                return payload;
            }
            case EventType::DriveThroughServed:{
                payload["vehicleIdx"] = data.DriveThroughPenaltyServed.vehicleIdx;
                return payload;
            }
            case EventType::StopGoServed:{
                payload["vehicleIdx"] = data.StopGoPenaltyServed.vehicleIdx;
                return payload;
            }
            case EventType::Flashback:{
                payload["flashbackFrameIdentifier"] = data.Flashback.flashbackFrameIdentifier;
                payload["flashbackSessionTime"] = data.Flashback.flashbackSessionTime;
                return payload;
            }
            case EventType::ButtonStatus:{
                payload["button"] = mapLookup(buttonFlagsMap, data.Buttons.buttonStatus);
                return payload;
            }
            case EventType::RedFlag:{
                payload["data"] = true;
                return payload;
            }
            case EventType::Overtake:{
                payload["overtakingVehicleIdx"] = data.Overtake.overtakingVehicleIdx;
                payload["beingOvertakenVehicleIdx"] = data.Overtake.beingOvertakenVehicleIdx;
                return payload;
            }
            default:{
                payload["Unknown"] = "Unknown";
                return payload;
            }
        }
    }

    nlohmann::json TelemetryProcessor::processPacketEventData(const PacketEventData &data){
        nlohmann::json jsonEventData;
        jsonEventData["header"] = processPacketHeader(data.header);

        std::string eventCode = std::string(reinterpret_cast<const char*>(data.eventStringCode), 4);
        jsonEventData["type"] = mapLookup(eventTypeMap, eventCode);

        jsonEventData["payload"] = eventPacketParser(eventCode, data.eventDetails);
        return jsonEventData;
    }

    nlohmann::json TelemetryProcessor::processPacketParticipantsData(const PacketParticipantsData &data){
        nlohmann::json jsonParticipantsData;
        jsonParticipantsData["header"] = processPacketHeader(data.header);
        jsonParticipantsData["numActiveCars"] = data.numActiveCars;

        nlohmann::json participants = nlohmann::json::array();

        for(const ParticipantData& participantData : data.participants){
            nlohmann::json participant;

            if(participantData.driverId == 255){
                participant["driverName"] = mapLookup(driverIdsMap, static_cast<int>(participantData.driverId));
                participant["teamId"] = participantData.teamId; //map lookup
                participant["carRaceNumber"] = participantData.raceNumber;
                participant["nationality"] = participantData.nationality; // map lookup
            } else{
                participant["driverName"] = participantData.name;
                participant["networkId"] = participantData.networkId;
                participant["teamId"] = participantData.teamId; //map lookup
                participant["carRaceNumber"] = participantData.raceNumber;
                participant["nationality"] = participantData.nationality; // map lookup
            }

            participants.push_back(participant);
        }

        jsonParticipantsData["participants"] = participants;
        return jsonParticipantsData;
    }

} // namespace TelemetryProcessor