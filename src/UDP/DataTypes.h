#ifndef DATATYPES_H
#define DATATYPES_H

#include <cstdint> // For defining fixed-width integer types
#include <string>  // For using the string class

// Forward declaration of PacketHeader since it's used in other structs
struct PacketHeader;

// Interface for Participant Data
struct ParticipantData {
    uint8_t m_aiControlled;       // Whether the vehicle is AI (1) or Human (0) controlled
    uint8_t m_driverId;            // Driver id - see appendix, 255 if network human
    uint8_t m_networkId;           // Network id – unique identifier for network players
    uint8_t m_teamId;              // Team id - see appendix
    uint8_t m_myTeam;              // My team flag – 1 = My Team, 0 = otherwise
    uint8_t m_raceNumber;
    uint8_t m_nationality;
    char m_name[64];             // Name of the driver.  Max length is 64.  Use char array.
    uint8_t m_yourTelemetry;
    uint8_t m_showOnlineNames;
    uint8_t m_platform;
};

// Interface for Packet Participants Data
struct PacketParticipantsData {
    PacketHeader m_header;
    uint8_t m_numActiveCars;
    ParticipantData m_participants[22]; // Assuming a max of 22 participants
};

// Interface for Car Setup Data
struct CarSetupData {
    uint8_t m_frontWing;             // Front wing aero
    uint8_t m_rearWing;              // Rear wing aero
    uint8_t m_onThrottle;            // Differential adjustment on throttle (percentage)
    uint8_t m_offThrottle;           // Differential adjustment off throttle (percentage)
    float m_frontCamber;           // Front camber angle (suspension geometry)
    float m_rearCamber;            // Rear camber angle (suspension geometry)
    float m_frontToe;              // Front toe angle (suspension geometry)
    float m_rearToe;               // Rear toe angle (suspension geometry)
    uint8_t m_frontSuspension;       // Front suspension
    uint8_t m_rearSuspension;        // Rear suspension
    uint8_t m_frontAntiRollBar;    // Front anti-roll bar
    uint8_t m_rearAntiRollBar;     // Front anti-roll bar
    uint8_t m_frontSuspensionHeight; // Front ride height
    uint8_t m_rearSuspensionHeight;  // Rear ride height
    uint8_t m_brakePressure;         // Brake pressure (percentage)
    uint8_t m_brakeBias;             // Brake bias (percentage)
    float m_rearLeftTyrePressure;    // Rear left tyre pressure (PSI)
    float m_rearRightTyrePressure;   // Rear right tyre pressure (PSI)
    float m_frontLeftTyrePressure;   // Front left tyre pressure (PSI)
    float m_frontRightTyrePressure;  // Front right tyre pressure (PSI)
    uint8_t m_ballast;               // Ballast
    float m_fuelLoad;                // Fuel load
};

// Interface for Packet Car Setup Data
struct PacketCarSetupData {
    PacketHeader m_header;
    CarSetupData m_carSetups[22]; // Assuming 22 cars
};

// Interface for Car Telemetry Data
struct CarTelemetryData {
    uint16_t m_speed;                   // Speed of car in kilometres per hour
    float m_throttle;                 // Amount of throttle applied (0.0 to 1.0)
    float m_steer;                    // Steering (-1.0 (full lock left) to 1.0 (full lock right))
    float m_brake;                    // Amount of brake applied (0.0 to 1.0)
    uint8_t m_clutch;                   // Amount of clutch applied (0 to 100)
    int8_t m_gear;                      // Gear selected (1-8, N=0, R=-1)
    uint16_t m_engineRPM;                // Engine RPM
    uint8_t m_drs;                      // 0 = off, 1 = on
    uint8_t m_revLightsPercent;         // Rev lights indicator (percentage)
    uint16_t m_revLightsBitValue;        // Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
    uint16_t m_brakesTemperature[4];    // Brakes temperature (celsius) -  RL, RR, FL, FR
    uint16_t m_tyresSurfaceTemperature[4]; // Tyres surface temperature (celsius) - RL, RR, FL, FR
    uint16_t m_tyresInnerTemperature[4];   // Tyres inner temperature (celsius) - RL, RR, FL, FR
    uint16_t m_engineTemperature;            // Engine temperature (celsius)
    float m_tyresPressure[4];          // Tyres pressure (PSI) - RL, RR, FL, FR
    uint8_t m_surfaceType[4];            // Driving surface, see appendices - RL, RR, FL, FR
};

// Interface for Packet Car Telemetry Data
struct PacketCarTelemetryData {
    PacketHeader m_header;
    CarTelemetryData m_carTelemetryData[22];
    uint8_t m_mfdPanelIndex;
    uint8_t m_mfdPanelIndexSecondaryPlayer;
    int8_t m_suggestedGear;
};

// Interface for Car Status Data
struct CarStatusData {
    uint8_t m_traction_control;    // Traction control - 0 = off, 1 = medium, 2 = full
    uint8_t m_anti_lock_brakes;    // 0 (off) - 1 (on)
    uint8_t m_fuel_mix;            // Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
    uint8_t m_front_brake_bias;    // Front brake bias (percentage)
    uint8_t m_pit_limiter_status;  // Pit limiter status - 0 = off, 1 = on
    float m_fuel_in_tank;        // Current fuel mass
    float m_fuel_capacity;        // Fuel capacity
    float m_fuel_remaining_laps;  // Fuel remaining in terms of laps (value on MFD)
    uint16_t m_max_rpm;            // Car's max RPM, point of rev limiter
    uint16_t m_idle_rpm;           // Car's idle RPM
    uint8_t m_max_gears;           // Maximum number of gears
    uint8_t m_drs_allowed;         // 0 = not allowed, 1 = allowed
    uint16_t m_drs_activation_distance; // 0 = DRS not available, non-zero - DRS will be available in [X] meters
    uint8_t m_actual_tyre_compound;  // F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
                                   // 21 = C0, 7 = inter, 8 = wet
                                   // F1 Classic - 9 = dry, 10 = wet
                                   // F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard
                                   // 15 = wet
    uint8_t m_visual_tyre_compound;  // F1 visual (can be different from actual compound)
                                   // 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                   // F1 Classic – same as above
                                   // F2 ‘19, 15 = wet, 19 – super soft, 20 = soft
                                   // 21 = medium, 22 = hard
    uint8_t m_tyres_age_laps;      // Age in laps of the current set of tyres
    int8_t m_vehicle_fia_flags;      // -1 = invalid/unknown, 0 = none, 1 = green
                                   // 2 = blue, 3 = yellow
    uint16_t m_engine_power_ice;    // Engine power output of ICE (W)
    uint16_t m_engine_power_mguk;   // Engine power output of MGU-K (W)
    float m_ers_store_energy;      // ERS energy store in Joules
    uint8_t m_ers_deploy_mode;      // ERS deployment mode, 0 = none, 1 = medium
                                   // 2 = hotlap, 3 = overtake
    float m_ers_harvested_this_lap_mguk; // ERS energy harvested this lap by MGU-K
    float m_ers_harvested_this_lap_mguh; // ERS energy harvested this lap by MGU-H
    float m_ers_deployed_this_lap;    // ERS energy deployed this lap
    uint8_t m_network_paused;        // Whether the car is paused in a network game
};

// Interface for Packet Car Status Data
struct PacketCarStatusData {
    PacketHeader m_header;
    CarStatusData m_car_status_data[22];
};

// Interface for Final Classification Data
struct FinalClassificationData {
    uint8_t m_position;          // Finishing position
    uint8_t m_numLaps;           // Number of laps completed
    uint8_t m_gridPosition;      // Grid position of the car
    uint8_t m_points;            // Number of points scored
    uint8_t m_numPitStops;       // Number of pit stops made
    uint8_t m_resultStatus;      // Result status - 0 = invalid, 1 = inactive, 2 = active
                                 // 3 = finished, 4 = didnotfinish, 5 = disqualified
                                 // 6 = not classified, 7 = retired
    uint32_t m_bestLapTimeInMS;   // Best lap time of the session in milliseconds
    double m_totalRaceTime;
    float m_penaltiesTime;       // Total penalties accumulated in seconds
    uint8_t m_numPenalties;        // Number of penalties applied to this driver
    uint8_t m_numTyreStints;      // Number of tyre stints up to maximum
    uint8_t m_tyreStintsActual[8];  // Actual tyres used by this driver
    uint8_t m_tyreStintsVisual[8];  // Visual tyres used by this driver
    uint8_t m_tyreStintsEndLaps[8]; // The lap number stints end on
};

// Interface for Packet Final Classification Data
struct PacketFinalClassificationData {
    PacketHeader m_header;
    uint8_t m_numCars;
    FinalClassificationData m_classificationData[22];
};

// Interface for Lobby Info Data
struct LobbyInfoData {
    uint8_t m_aiControlled;    // Whether the vehicle is AI (1) or Human (0) controlled
    uint8_t m_teamId;          // Team id - see appendix (255 if no team currently selected)
    uint8_t m_nationality;
    uint8_t m_platform;        // 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
    char m_name[64];       // Name of participant. Max length is 64.
    uint8_t m_carNumber;       // Car number of the player
    uint8_t m_readyStatus;     // 0 = not ready, 1 = ready, 2 = spectating
};

// Interface for Packet Lobby Info Data
struct PacketLobbyInfoData {
    PacketHeader m_header;
    uint8_t m_numPlayers;
    LobbyInfoData m_lobbyPlayers[22];
};

// Interface for Car Damage Data
struct CarDamageData {
    uint8_t m_tyres_wear[4];           // Tyre wear (percentage) - RL, RR, FL, FR
    uint8_t m_tyres_damage[4];         // Tyre damage (percentage) - RL, RR, FL, FR
    uint8_t m_brakes_damage[4];        // Brakes damage (percentage) - RL, RR, FL, FR
    uint8_t m_front_left_wing_damage;    // Front left wing damage (percentage)
    uint8_t m_front_right_wing_damage;   // Front right wing damage (percentage)
    uint8_t m_rear_wing_damage;      // Rear wing damage (percentage)
    uint8_t m_floor_damage;          // Floor damage (percentage)
    uint8_t m_diffuser_damage;       // Diffuser damage (percentage)
    uint8_t m_sidepod_damage;        // Sidepod damage (percentage)
    uint8_t m_drs_fault;             // Indicator for DRS fault, 0 = OK, 1 = fault
    uint8_t m_ers_fault;             // Indicator for ERS fault, 0 = OK, 1 = fault
    uint8_t m_gear_box_damage;       // Gear box damage (percentage)
    uint8_t m_engine_damage;         // Engine damage (percentage)
    uint8_t m_engine_mguh_wear;      // Engine wear MGU-H (percentage)
    uint8_t m_engine_es_wear;        // Engine wear ES (percentage)
    uint8_t m_engine_ce_wear;        // Engine wear CE (percentage)
    uint8_t m_engine_ice_wear;       // Engine wear ICE (percentage)
    uint8_t m_engine_mguk_wear;      // Engine wear MGU-K (percentage)
    uint8_t m_engine_tc_wear;        // Engine wear TC (percentage)
    uint8_t m_engine_blown;          // Engine blown, 0 = OK, 1 = fault
    uint8_t m_engine_seized;         // Engine seized, 0 = OK, 1 = fault
};

// Interface for Packet Car Damage Data
struct PacketCarDamageData {
    PacketHeader m_header;
    CarDamageData m_car_damage_data[22];
};

// Interface for Lap History Data
struct LapHistoryData {
    uint32_t m_lapTimeInMS;       // Lap time in milliseconds
    uint32_t m_sector1TimeInMS;     // Sector 1 time in milliseconds
    uint8_t m_sector1TimeMinutes;   // Sector 1 whole minute part
    uint32_t m_sector2TimeInMS;     // Sector 2 time in milliseconds
    uint8_t m_sector2TimeMinutes;   // Sector 2 whole minute part
    uint32_t m_sector3TimeInMS;     // Sector 3 time in milliseconds
    uint8_t m_sector3TimeMinutes;   // Sector 3 whole minute part
    uint8_t m_lapValidBitFlags;    // 0x01 bit set-lap valid, 0x02 bit set-sector 1 valid
                                 // 0x04 bit set-sector 2 valid, 0x08 bit set-sector 3 valid
};

// Interface for Tyre Stint History Data
struct TyreStintHistoryData {
    uint8_t m_endLap;            // Lap the tyre usage ends on (255 of current tyre)
    uint8_t m_tyreActualCompound;  // Actual tyres used by this driver
    uint8_t m_tyreVisualCompound;  // Visual tyres used by this driver
};

// Interface for Packet Session History Data
struct PacketSessionHistoryData {
    PacketHeader m_header;
    uint8_t m_carIdx;
    uint8_t m_numLaps;
    uint8_t m_numTyreStints;
    uint8_t m_bestLapTimeLapNum;
    uint8_t m_bestSector1LapNum;
    uint8_t m_bestSector2LapNum;
    uint8_t m_bestSector3LapNum;
    LapHistoryData m_lapHistoryData[100];
    TyreStintHistoryData m_tyreStintsHistoryData[8];
};

// Interface for Tyre Set Data
struct TyreSetData {
    uint8_t m_actualTyreCompound;
    uint8_t m_visualTyreCompound;
    uint8_t m_wear;
    uint8_t m_available;
    uint8_t m_recommendedSession;
    uint8_t m_lifeSpan;
    uint8_t m_usableLife;
    uint32_t m_lapDeltaTime;
    uint8_t m_fitted;
};

// Interface for Packet Tyre Sets Data
struct PacketTyreSetsData {
    PacketHeader m_header;
    uint8_t m_carIdx;
    TyreSetData m_tyreSetData[20]; // 13 dry + 7 wet
    uint8_t m_fittedIdx;
};

// Interface for Packet Motion Ex Data
struct PacketMotionExData {
    PacketHeader m_header;
    float m_suspensionPosition[4];
    float m_suspensionVelocity[4];
    float m_suspensionAcceleration[4];
    float m_wheelSpeed[4];
    float m_wheelSlipRatio[4];
    float m_wheelSlipAngle[4];
    float m_wheelLatForce[4];
    float m_wheelLongForce[4];
    float m_heightOfCOGAboveGround;
    float m_localVelocityX;
    float m_localVelocityY;
    float m_localVelocityZ;
    float m_angularVelocityX;
    float m_angularVelocityY;
    float m_angularVelocityZ;
    float m_angularAccelerationX;
    float m_angularAccelerationY;
    float m_angularAccelerationZ;
    float m_frontWheelsAngle;
    float m_wheelVertForce[4];
};

// Options struct -  Removed the Options struct
// struct Options {
//     int port;
//     std::string address;
// };

// Fastest Lap Data struct
struct FastestLapData {
    uint8_t vehicleIdx;
    float lapTime;
};

// Retirement Data struct
struct RetirementData {
    uint8_t vehicleIdx;
};

// Team Mate In Pits Data struct
struct TeamMateInPitsData{
    uint8_t vehicleIdx;
};

// Race Winner Data struct
struct RaceWinnerData {
    uint8_t vehicleIdx;
};

// Penalty Data struct
struct PenaltyData {
    uint8_t penaltyType;
    uint8_t infringementType;
    uint8_t vehicleIdx;
    uint8_t otherVehicleIdx;
    float time;
    uint8_t lapNum;
    uint8_t placesGained;
};

// Speed Trap Data struct
struct SpeedTrapData {
    uint8_t vehicleIdx;
    float speed;
    uint8_t isOverallFastestInSession;
    uint8_t isDriverFastestInSession;
    uint8_t fastestVehicleIdxInSession;
    float fastestSpeedInSession;
};

// Start Lights Data struct
struct StartLightsData {
    uint8_t numLights;
};

// Drive Through Penalty Served Data struct
struct DriveThroughPenaltyServedData {
    uint8_t vehicleIdx;
};

// Stop Go Penalty Served Data struct
struct StopGoPenaltyServedData {
    uint8_t vehicleIdx;
};

// Flashback Data struct
struct FlashbackData {
    uint32_t flashbackFrameIdentifier;
    float flashbackSessionTime;
};

// Buttons Data struct
struct ButtonsData {
    uint32_t buttonStatus;
};

// Overtake Data struct
struct OvertakeData {
    uint8_t overtakingVehicleIdx;
    uint8_t beingOvertakenVehicleIdx;
};

// Packet Event Data struct
struct PacketEventData {
    PacketHeader m_header;
    char m_eventStringCode[4]; // size is 4 in the original C code
    union {
        FastestLapData fastestLap;
        RetirementData retirement;
        TeamMateInPitsData teamMateInPits;
        RaceWinnerData raceWinner;
        PenaltyData penalty;
        SpeedTrapData speedTrap;
        StartLightsData startLights;
        DriveThroughPenaltyServedData driveThroughPenaltyServed;
        StopGoPenaltyServedData stopGoPenaltyServed;
        FlashbackData flashback;
        ButtonsData buttons;
        OvertakeData overtake;
    } m_eventDetails;
};

// Packet Header struct
struct PacketHeader {
    uint16_t packetFormat;
    uint8_t gameYear;
    uint8_t gameMajorVersion;
    uint8_t gameMinorVersion;
    uint8_t packetVersion;
    uint8_t packetId;
    uint64_t sessionUID;
    float sessionTime;
    uint32_t frameIdentifier;
    uint32_t overallFrameIdentifier;
    uint8_t playerCarIndex;
    uint8_t secondaryPlayerCarIndex;
};

// Car Motion Data struct
struct CarMotionData {
    float m_worldPositionX;
    float m_worldPositionY;
    float m_worldPositionZ;
    float m_worldVelocityX;
    float m_worldVelocityY;
    float m_worldVelocityZ;
    int16_t m_worldForwardDirX;
    int16_t m_worldForwardDirY;
    int16_t m_worldForwardDirZ;
    int16_t m_worldRightDirX;
    int16_t m_worldRightDirY;
    int16_t m_worldRightDirZ;
    float m_gForceLateral;
    float m_gForceLongitudinal;
    float m_gForceVertical;
    float m_yaw;
    float m_pitch;
    float m_roll;
};

// Packet Motion Data struct
struct PacketMotionData {
    PacketHeader m_header;
    CarMotionData m_carMotionData[22];
};

// Marshal Zone struct
struct MarshalZone {
    float m_zoneStart;
    int8_t m_zoneFlag;
};

// Weather Forecast Sample struct
struct WeatherForecastSample {
    uint8_t m_sessionType;
    uint8_t m_timeOffset;
    uint8_t m_weather;
    int8_t m_trackTemperature;
    int8_t m_trackTemperatureChange;
    int8_t m_airTemperature;
    int8_t m_airTemperatureChange;
    uint8_t m_rainPercentage;
};

// Packet Session Data struct
struct PacketSessionData {
    PacketHeader m_header;
    uint8_t m_weather;
    int8_t m_trackTemperature;
    int8_t m_airTemperature;
    uint8_t m_totalLaps;
    uint16_t m_trackLength;
    uint8_t m_sessionType;
    int8_t m_trackId;
    uint8_t m_formula;
    uint16_t m_sessionTimeLeft;
    uint16_t m_sessionDuration;
    uint8_t m_pitSpeedLimit;
    uint8_t m_gamePaused;
    uint8_t m_isSpectating;
    uint8_t m_spectatorCarIndex;
    uint8_t m_sliProNativeSupport;
    uint8_t m_numMarshalZones;
    MarshalZone m_marshalZones[21]; // Max 21 marshal zones
    int8_t m_safetyCarStatus;
    uint8_t m_networkGame;
    uint8_t m_numWeatherForecastSamples;
    WeatherForecastSample m_weatherForecastSamples[56]; // Max 56 samples
    int8_t m_forecastAccuracy;
    uint8_t m_aiDifficulty;
    uint32_t m_seasonLinkIdentifier;
    uint32_t m_weekendLinkIdentifier;
    uint32_t m_sessionLinkIdentifier;
    uint8_t m_pitStopWindowIdealLap;
    uint8_t m_pitStopWindowLatestLap;
    uint8_t m_pitStopRejoinPosition;
    uint8_t m_steeringAssist;
    uint8_t m_brakingAssist;
    uint8_t m_gearboxAssist;
    uint8_t m_pitAssist;
    uint8_t m_pitReleaseAssist;
    uint8_t m_ERSAssist;
    uint8_t m_DRSAssist;
    uint8_t m_dynamicRacingLine;
    uint8_t m_dynamicRacingLineType;
    uint8_t m_gameMode;
    uint8_t m_ruleSet;
    uint32_t m_timeOfDay;
    uint8_t m_sessionLength;
    int8_t m_speedUnitsLeadPlayer;
    int8_t m_temperatureUnitsLeadPlayer;
    int8_t m_speedUnitsSecondaryPlayer;
    int8_t m_temperatureUnitsSecondaryPlayer;
    uint8_t m_numSafetyCarPeriods;
    uint8_t m_numVirtualSafetyCarPeriods;
    uint8_t m_numRedFlagPeriods;
};

// Interface for Lap Data
struct LapData {
    uint32_t m_lastLapTimeInMS;
    uint32_t m_currentLapTimeInMS;
    uint16_t m_sector1TimeInMS;
    uint8_t m_sector1TimeMinutes;
    uint16_t m_sector2TimeInMS;
    uint8_t m_sector2TimeMinutes;
    uint16_t m_deltaToCarInFrontInMS;
    uint16_t m_deltaToRaceLeaderInMS;
    float m_lapDistance;
    float m_totalDistance;
    float m_safetyCarDelta;
    uint8_t m_carPosition;
    uint8_t m_currentLapNum;
    uint8_t m_pitStatus;
    uint8_t m_numPitStops;
    uint8_t m_sector;
    uint8_t m_currentLapInvalid;
    uint8_t m_penalties;
    uint8_t m_totalWarnings;
    uint8_t m_cornerCuttingWarnings;
    uint8_t m_numUnservedDriveThroughPens;
    uint8_t m_numUnservedStopGoPens;
    uint8_t m_gridPosition;
    uint8_t m_driverStatus;
    uint8_t m_resultStatus;
    uint8_t m_pitLaneTimerActive;
    uint16_t m_pitLaneTimeInLaneInMS;
    uint16_t m_pitStopTimerInMS;
    uint8_t m_pitStopShouldServePen;
};

// Interface for Packet Lap Data
struct PacketLapData {
    PacketHeader m_header;
    LapData m_lapData[22];
    int8_t m_timeTrialPBCarIdx;
    int8_t m_timeTrialRivalCarIdx;
};

#endif // DATATYPES_H
