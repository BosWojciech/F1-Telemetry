#ifndef DATATYPES_H
#define DATATYPES_H

#include <cstdint>
#include <string>

const size_t PACKET_MOTION_DATA_SIZE = 1349;
const size_t PACKET_CAR_TELEMETRY_DATA_SIZE = 1352;
const size_t PACKET_SESSION_DATA_SIZE = 644;
const size_t PACKET_LAP_DATA_SIZE = 1131;
const size_t PACKET_EVENT_DATA_SIZE = 45;
const size_t PACKET_PARTICIPANTS_DATA_SIZE = 1306;
const size_t PACKET_CAR_SETUP_DATA_SIZE = 1107;
const size_t PACKET_CAR_TELEMETRY_DATA_SIZE = 1352;
const size_t PACKET_CAR_STATUS_DATA_SIZE = 1239;
const size_t PACKET_FINAL_CLASSIFICATION_DATA_SIZE = 1020;
const size_t PACKET_LOBBY_INFO_DATA_SIZE = 1218;
const size_t PACKET_CAR_DAMAGE_DATA_SIZE = 953;
const size_t PACKET_SESSION_HISTORY_DATA_SIZE = 1460;
const size_t PACKET_TYRE_SETS_DATA_SIZE = 231;
const size_t PACKET_MOTION_EX_DATA_SIZE = 217;

#pragma pack(push, 1)

// Packet Header struct
struct PacketHeader
{
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
struct CarMotionData
{
    float m_worldPositionX;     // World space X position - meters
    float m_worldPositionY;     // World space Y position
    float m_worldPositionZ;     // World space Z position
    float m_worldVelocityX;     // Velocity in world space X - meters/s
    float m_worldVelocityY;     // Velocity in world space Y
    float m_worldVelocityZ;     // Velocity in world space Z
    int16_t m_worldForwardDirX; // World space forward X direction (normalized)
    int16_t m_worldForwardDirY; // World space forward Y direction (normalized)
    int16_t m_worldForwardDirZ; // World space forward Z direction (normalized)
    int16_t m_worldRightDirX;   // World space right X direction (normalized)
    int16_t m_worldRightDirY;   // World space right Y direction (normalized)
    int16_t m_worldRightDirZ;   // World space right Z direction (normalized)
    float m_gForceLateral;      // Lateral G-Force component
    float m_gForceLongitudinal; // Longitudinal G-Force component
    float m_gForceVertical;     // Vertical G-Force component
    float m_yaw;                // Yaw angle in radians
    float m_pitch;              // Pitch angle in radians
    float m_roll;               // Roll angle in radians
};

// Packet Motion Data struct
struct PacketMotionData
{
    PacketHeader m_header;             // Header
    CarMotionData m_carMotionData[22]; // Data for all cars on track
};

// Car Telemetry Data struct
struct CarTelemetryData
{
    uint16_t speed;                     // Speed of car in kilometres per hour
    float throttle;                     // Throttle applied (0.0 to 1.0)
    float steer;                        // Steering (-1.0 to 1.0)
    float brake;                        // Brake applied (0.0 to 1.0)
    uint8_t clutch;                     // Clutch applied (0 to 100)
    int8_t gear;                        // Gear (1-8, N=0, R=-1)
    uint16_t engineRPM;                 // Engine RPM
    uint8_t drs;                        // 0 = off, 1 = on
    uint8_t revLightsPercent;           // Rev lights percentage
    uint16_t revLightsBitValue;         // Rev lights bitfield
    uint16_t brakesTemperature[4];      // Brakes temperature (celsius)
    uint8_t tyresSurfaceTemperature[4]; // Tyres surface temperature (celsius)
    uint8_t tyresInnerTemperature[4];   // Tyres inner temperature (celsius)
    uint16_t engineTemperature;         // Engine temperature (celsius)
    float tyresPressure[4];             // Tyres pressure (PSI)
    uint8_t surfaceType[4];             // Driving surface type
};

// Packet Car Telemetry Data struct
struct PacketCarTelemetryData
{
    PacketHeader header;                   // Header
    CarTelemetryData carTelemetryData[22]; // Telemetry data for all cars (22 total)
    uint8_t mfdPanelIndex;                 // MFD panel index (0–4 or 255 = closed)
    uint8_t mfdPanelIndexSecondaryPlayer;  // Secondary player MFD panel index
    int8_t suggestedGear;                  // Suggested gear (1–8, 0 = none)
};

// Marshal Zone struct
struct MarshalZone
{
    float m_zoneStart; // Fraction (0..1) of way through the lap the marshal zone starts
    int8_t m_zoneFlag; // -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
};

// Weather Forecast Sample struct
struct WeatherForecastSample
{
    uint8_t m_sessionType;           // 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P,
                                     // 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ,
                                     // 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
    uint8_t m_timeOffset;            // Time in minutes the forecast is for
    uint8_t m_weather;               // Weather - 0 = clear, 1 = light cloud, 2 = overcast,
                                     // 3 = light rain, 4 = heavy rain, 5 = storm
    int8_t m_trackTemperature;       // Track temp. in degrees Celsius
    int8_t m_trackTemperatureChange; // Track temp. change – 0 = up, 1 = down, 2 = no change
    int8_t m_airTemperature;         // Air temp. in degrees Celsius
    int8_t m_airTemperatureChange;   // Air temp. change – 0 = up, 1 = down, 2 = no change
    uint8_t m_rainPercentage;        // Rain percentage (0–100)
};

// Packet Session Data struct
struct PacketSessionData
{
    PacketHeader m_header; // Header

    uint8_t m_weather;                                  // Weather - 0 = clear, 1 = light cloud, 2 = overcast,
                                                        // 3 = light rain, 4 = heavy rain, 5 = storm
    int8_t m_trackTemperature;                          // Track temp. in degrees Celsius
    int8_t m_airTemperature;                            // Air temp. in degrees Celsius
    uint8_t m_totalLaps;                                // Total number of laps in this race
    uint16_t m_trackLength;                             // Track length in metres
    uint8_t m_sessionType;                              // 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P,
                                                        // 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ,
                                                        // 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
    int8_t m_trackId;                                   // -1 for unknown, see appendix
    uint8_t m_formula;                                  // Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2,
                                                        // 3 = F1 Generic, 4 = Beta, 5 = Supercars,
                                                        // 6 = Esports, 7 = F2 2021
    uint16_t m_sessionTimeLeft;                         // Time left in session in seconds
    uint16_t m_sessionDuration;                         // Session duration in seconds
    uint8_t m_pitSpeedLimit;                            // Pit speed limit in kilometres per hour
    uint8_t m_gamePaused;                               // Whether the game is paused – network game only
    uint8_t m_isSpectating;                             // Whether the player is spectating
    uint8_t m_spectatorCarIndex;                        // Index of the car being spectated
    uint8_t m_sliProNativeSupport;                      // SLI Pro support, 0 = inactive, 1 = active
    uint8_t m_numMarshalZones;                          // Number of marshal zones to follow
    MarshalZone m_marshalZones[21];                     // List of marshal zones – max 21
    uint8_t m_safetyCarStatus;                          // 0 = no safety car, 1 = full,
                                                        // 2 = virtual, 3 = formation lap
    uint8_t m_networkGame;                              // 0 = offline, 1 = online
    uint8_t m_numWeatherForecastSamples;                // Number of weather samples to follow
    WeatherForecastSample m_weatherForecastSamples[56]; // Array of weather forecast samples
    uint8_t m_forecastAccuracy;                         // 0 = Perfect, 1 = Approximate
    uint8_t m_aiDifficulty;                             // AI Difficulty rating – 0-110
    uint32_t m_seasonLinkIdentifier;                    // Identifier for season - persists across saves
    uint32_t m_weekendLinkIdentifier;                   // Identifier for weekend - persists across saves
    uint32_t m_sessionLinkIdentifier;                   // Identifier for session - persists across saves
    uint8_t m_pitStopWindowIdealLap;                    // Ideal lap to pit on for current strategy (player)
    uint8_t m_pitStopWindowLatestLap;                   // Latest lap to pit on for current strategy (player)
    uint8_t m_pitStopRejoinPosition;                    // Predicted position to rejoin at (player)
    uint8_t m_steeringAssist;                           // 0 = off, 1 = on
    uint8_t m_brakingAssist;                            // 0 = off, 1 = low, 2 = medium, 3 = high
    uint8_t m_gearboxAssist;                            // 1 = manual, 2 = manual & suggested gear, 3 = auto
    uint8_t m_pitAssist;                                // 0 = off, 1 = on
    uint8_t m_pitReleaseAssist;                         // 0 = off, 1 = on
    uint8_t m_ERSAssist;                                // 0 = off, 1 = on
    uint8_t m_DRSAssist;                                // 0 = off, 1 = on
    uint8_t m_dynamicRacingLine;                        // 0 = off, 1 = corners only, 2 = full
    uint8_t m_dynamicRacingLineType;                    // 0 = 2D, 1 = 3D
    uint8_t m_gameMode;                                 // Game mode id - see appendix
    uint8_t m_ruleSet;                                  // Ruleset - see appendix
    uint32_t m_timeOfDay;                               // Local time of day - minutes since midnight
    uint8_t m_sessionLength;                            // 0 = None, 2 = Very Short, 3 = Short, 4 = Medium,
                                                        // 5 = Medium Long, 6 = Long, 7 = Full
    uint8_t m_speedUnitsLeadPlayer;                     // 0 = MPH, 1 = KPH
    uint8_t m_temperatureUnitsLeadPlayer;               // 0 = Celsius, 1 = Fahrenheit
    uint8_t m_speedUnitsSecondaryPlayer;                // 0 = MPH, 1 = KPH
    uint8_t m_temperatureUnitsSecondaryPlayer;          // 0 = Celsius, 1 = Fahrenheit
    uint8_t m_numSafetyCarPeriods;                      // Number of safety cars called during session
    uint8_t m_numVirtualSafetyCarPeriods;               // Number of virtual safety cars called
    uint8_t m_numRedFlagPeriods;                        // Number of red flags called during session
};

// Lap Data struct
struct LapData
{
    uint32_t lastLapTimeInMS;            // Last lap time in milliseconds
    uint32_t currentLapTimeInMS;         // Current time around the lap in milliseconds
    uint16_t sector1TimeInMS;            // Sector 1 time in milliseconds
    uint8_t sector1TimeMinutes;          // Sector 1 whole minute part
    uint16_t sector2TimeInMS;            // Sector 2 time in milliseconds
    uint8_t sector2TimeMinutes;          // Sector 2 whole minute part
    uint16_t deltaToCarInFrontInMS;      // Time delta to car in front in milliseconds
    uint16_t deltaToRaceLeaderInMS;      // Time delta to race leader in milliseconds
    float lapDistance;                   // Distance vehicle is around current lap in metres – could be negative if line hasn't been crossed yet
    float totalDistance;                 // Total distance travelled in session in metres – could be negative if line hasn't been crossed yet
    float safetyCarDelta;                // Delta in seconds for safety car
    uint8_t carPosition;                 // Car race position
    uint8_t currentLapNum;               // Current lap number
    uint8_t pitStatus;                   // 0 = none, 1 = pitting, 2 = in pit area
    uint8_t numPitStops;                 // Number of pit stops taken in this race
    uint8_t sector;                      // 0 = sector1, 1 = sector2, 2 = sector3
    uint8_t currentLapInvalid;           // Current lap invalid - 0 = valid, 1 = invalid
    uint8_t penalties;                   // Accumulated time penalties in seconds to be added
    uint8_t totalWarnings;               // Accumulated number of warnings issued
    uint8_t cornerCuttingWarnings;       // Accumulated number of corner cutting warnings issued
    uint8_t numUnservedDriveThroughPens; // Num drive-through pens left to serve
    uint8_t numUnservedStopGoPens;       // Num stop-go pens left to serve
    uint8_t gridPosition;                // Grid position the vehicle started the race in
    uint8_t driverStatus;                // Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
    uint8_t resultStatus;                // Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = did not finish, 5 = disqualified, 6 = not classified, 7 = retired
    uint8_t pitLaneTimerActive;          // Pit lane timing, 0 = inactive, 1 = active
    uint16_t pitLaneTimeInLaneInMS;      // If active, the current time spent in the pit lane in ms
    uint16_t pitStopTimerInMS;           // Time of the actual pit stop in ms
    uint8_t pitStopShouldServePen;       // Whether the car should serve a penalty at this stop
};

// Packet Lap Data struct
struct PacketLapData
{
    PacketHeader header;          // Header
    LapData lapData[22];          // Lap data for all cars on track
    uint8_t timeTrialPBCarIdx;    // Index of Personal Best car in time trial (255 if invalid)
    uint8_t timeTrialRivalCarIdx; // Index of Rival car in time trial (255 if invalid)
};

struct FastestLapData
{
    uint8_t vehicleIdx; // Vehicle index of the car setting the fastest lap
    float lapTime;      // Lap time in seconds
};

struct RetirementData
{
    uint8_t vehicleIdx; // Vehicle index of the car that retired
};

struct TeamMateInPitsData
{
    uint8_t vehicleIdx; // Vehicle index of the team mate
};

struct RaceWinnerData
{
    uint8_t vehicleIdx; // Vehicle index of the race winner
};

struct PenaltyData
{
    uint8_t penaltyType;      // Penalty type – see docs
    uint8_t infringementType; // Infringement type – see docs
    uint8_t vehicleIdx;       // Vehicle index of the car the penalty is applied to
    uint8_t otherVehicleIdx;  // Vehicle index of the other car involved
    uint8_t time;             // Time gained, or time spent doing action in seconds
    uint8_t lapNum;           // Lap the penalty occurred on
    uint8_t placesGained;     // Number of places gained by this
};

struct SpeedTrapData
{
    uint8_t vehicleIdx;                 // Vehicle index of the car triggering the speed trap
    float speed;                        // Top speed achieved in kilometres per hour
    uint8_t isOverallFastestInSession;  // Overall fastest in session
    uint8_t isDriverFastestInSession;   // Fastest for driver in session
    uint8_t fastestVehicleIdxInSession; // Vehicle index of the fastest vehicle in the session
    float fastestSpeedInSession;        // Speed of the fastest vehicle in the session
};

struct StartLightsData
{
    uint8_t numLights; // Number of lights showing
};

struct DriveThroughPenaltyServedData
{
    uint8_t vehicleIdx; // Vehicle index of the car serving drive-through
};

struct StopGoPenaltyServedData
{
    uint8_t vehicleIdx; // Vehicle index of the car serving stop-go
};

struct FlashbackData
{
    uint32_t flashbackFrameIdentifier; // Frame identifier flashed back to
    float flashbackSessionTime;        // Session time flashed back to
};

struct ButtonsData
{
    uint32_t buttonStatus; // Bit flags specifying which buttons are being pressed
};

struct OvertakeData
{
    uint8_t overtakingVehicleIdx;     // Vehicle index of the overtaking car
    uint8_t beingOvertakenVehicleIdx; // Vehicle index of the car being overtaken
};

union EventDataDetails
{
    FastestLapData FastestLap;
    RetirementData Retirement;
    TeamMateInPitsData TeamMateInPits;
    RaceWinnerData RaceWinner;
    PenaltyData Penalty;
    SpeedTrapData SpeedTrap;
    StartLightsData StartLights;
    DriveThroughPenaltyServedData DriveThroughPenaltyServed;
    StopGoPenaltyServedData StopGoPenaltyServed;
    FlashbackData Flashback;
    ButtonsData Buttons;
    OvertakeData Overtake;
};

struct PacketEventData
{
    PacketHeader header;           // Header
    uint8_t eventStringCode[4];    // Event string code
    EventDataDetails eventDetails; // Event details - should be interpreted based on event string code
};

struct ParticipantData
{
    uint8_t aiControlled;    // Whether the vehicle is AI (1) or Human (0) controlled
    uint8_t driverId;        // Driver id - see appendix, 255 if network human
    uint8_t networkId;       // Network id – unique identifier for network players
    uint8_t teamId;          // Team id - see appendix
    uint8_t myTeam;          // My team flag – 1 = My Team, 0 = otherwise
    uint8_t raceNumber;      // Race number of the car
    uint8_t nationality;     // Nationality of the driver
    uint8_t name[48];        // Name of participant in UTF-8 format – null terminated
                             // Will be truncated with … (U+2026) if too long
    uint8_t yourTelemetry;   // The player's UDP setting, 0 = restricted, 1 = public
    uint8_t showOnlineNames; // The player's show online names setting, 0 = off, 1 = on
    uint8_t platform;        // 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
};

struct PacketParticipantsData
{
    PacketHeader header;              // Header
    uint8_t numActiveCars;            // Number of active cars in the data – should match number of cars on HUD
    ParticipantData participants[22]; // Participant data array
};

struct CarSetupData
{
    uint8_t frontWing;             // Front wing aero
    uint8_t rearWing;              // Rear wing aero
    uint8_t onThrottle;            // Differential adjustment on throttle (percentage)
    uint8_t offThrottle;           // Differential adjustment off throttle (percentage)
    float frontCamber;             // Front camber angle (suspension geometry)
    float rearCamber;              // Rear camber angle (suspension geometry)
    float frontToe;                // Front toe angle (suspension geometry)
    float rearToe;                 // Rear toe angle (suspension geometry)
    uint8_t frontSuspension;       // Front suspension
    uint8_t rearSuspension;        // Rear suspension
    uint8_t frontAntiRollBar;      // Front anti-roll bar
    uint8_t rearAntiRollBar;       // Rear anti-roll bar
    uint8_t frontSuspensionHeight; // Front ride height
    uint8_t rearSuspensionHeight;  // Rear ride height
    uint8_t brakePressure;         // Brake pressure (percentage)
    uint8_t brakeBias;             // Brake bias (percentage)
    float rearLeftTyrePressure;    // Rear left tyre pressure (PSI)
    float rearRightTyrePressure;   // Rear right tyre pressure (PSI)
    float frontLeftTyrePressure;   // Front left tyre pressure (PSI)
    float frontRightTyrePressure;  // Front right tyre pressure (PSI)
    uint8_t ballast;               // Ballast
    float fuelLoad;                // Fuel load
};

struct PacketCarSetupData
{
    PacketHeader header;        // Header
    CarSetupData carSetups[22]; // Setup data for all cars
};

struct CarTelemetryData
{
    uint16_t speed;                     // Speed of car in kilometres per hour
    float throttle;                     // Amount of throttle applied (0.0 to 1.0)
    float steer;                        // Steering (-1.0 (full lock left) to 1.0 (full lock right))
    float brake;                        // Amount of brake applied (0.0 to 1.0)
    uint8_t clutch;                     // Amount of clutch applied (0 to 100)
    int8_t gear;                        // Gear selected (1-8, N=0, R=-1)
    uint16_t engineRPM;                 // Engine RPM
    uint8_t drs;                        // 0 = off, 1 = on
    uint8_t revLightsPercent;           // Rev lights indicator (percentage)
    uint16_t revLightsBitValue;         // Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
    uint16_t brakesTemperature[4];      // Brakes temperature (celsius)
    uint8_t tyresSurfaceTemperature[4]; // Tyres surface temperature (celsius)
    uint8_t tyresInnerTemperature[4];   // Tyres inner temperature (celsius)
    uint16_t engineTemperature;         // Engine temperature (celsius)
    float tyresPressure[4];             // Tyres pressure (PSI)
    uint8_t surfaceType[4];             // Driving surface, see appendices
};

struct PacketCarTelemetryData
{
    PacketHeader header;                   // Header
    CarTelemetryData carTelemetryData[22]; // Telemetry data for all cars
    uint8_t mfdPanelIndex;                 // Index of MFD panel open - 255 = MFD closed
                                           // Single player, race – 0 = Car setup, 1 = Pits
                                           // 2 = Damage, 3 = Engine, 4 = Temperatures
                                           // May vary depending on game mode
    uint8_t mfdPanelIndexSecondaryPlayer;  // See above
    int8_t suggestedGear;                  // Suggested gear for the player (1-8)
                                           // 0 if no gear suggested
};

struct CarStatusData
{
    uint8_t traction_control;          // Traction control - 0 = off, 1 = medium, 2 = full
    uint8_t anti_lock_brakes;          // 0 (off) - 1 (on)
    uint8_t fuel_mix;                  // Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
    uint8_t front_brake_bias;          // Front brake bias (percentage)
    uint8_t pit_limiter_status;        // Pit limiter status - 0 = off, 1 = on
    float fuel_in_tank;                // Current fuel mass
    float fuel_capacity;               // Fuel capacity
    float fuel_remaining_laps;         // Fuel remaining in terms of laps (value on MFD)
    uint16_t max_rpm;                  // Car's max RPM, point of rev limiter
    uint16_t idle_rpm;                 // Car's idle RPM
    uint8_t max_gears;                 // Maximum number of gears
    uint8_t drs_allowed;               // 0 = not allowed, 1 = allowed
    uint16_t drs_activation_distance;  // 0 = DRS not available, non-zero - DRS will be available in [X] meters
    uint8_t actual_tyre_compound;      // F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
                                       // 21 = C0, 7 = inter, 8 = wet
                                       // F1 Classic - 9 = dry, 10 = wet
                                       // F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard
                                       // 15 = wet
    uint8_t visual_tyre_compound;      // F1 visual (can be different from actual compound)
                                       // 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                       // F1 Classic – same as above
                                       // F2 ‘19, 15 = wet, 19 – super soft, 20 = soft
                                       // 21 = medium, 22 = hard
    uint8_t tyres_age_laps;            // Age in laps of the current set of tyres
    int8_t vehicle_fia_flags;          // -1 = invalid/unknown, 0 = none, 1 = green
                                       // 2 = blue, 3 = yellow
    float engine_power_ice;            // Engine power output of ICE (W)
    float engine_power_mguk;           // Engine power output of MGU-K (W)
    float ers_store_energy;            // ERS energy store in Joules
    uint8_t ers_deploy_mode;           // ERS deployment mode, 0 = none, 1 = medium
                                       // 2 = hotlap, 3 = overtake
    float ers_harvested_this_lap_mguk; // ERS energy harvested this lap by MGU-K
    float ers_harvested_this_lap_mguh; // ERS energy harvested this lap by MGU-H
    float ers_deployed_this_lap;       // ERS energy deployed this lap
    uint8_t network_paused;            // Whether the car is paused in a network game
};

struct PacketCarStatusData
{
    PacketHeader header;               // Header
    CarStatusData car_status_data[22]; // Car status data for all cars
};

struct FinalClassificationData
{
    uint8_t position;             // Finishing position
    uint8_t numLaps;              // Number of laps completed
    uint8_t gridPosition;         // Grid position of the car
    uint8_t points;               // Number of points scored
    uint8_t numPitStops;          // Number of pit stops made
    uint8_t resultStatus;         // Result status - 0 = invalid, 1 = inactive, 2 = active
                                  // 3 = finished, 4 = didnotfinish, 5 = disqualified
                                  // 6 = not classified, 7 = retired
    uint32_t bestLapTimeInMS;     // Best lap time of the session in milliseconds
    double totalRaceTime;         // Total race time in seconds without penalties
    uint8_t penaltiesTime;        // Total penalties accumulated in seconds
    uint8_t numPenalties;         // Number of penalties applied to this driver
    uint8_t numTyreStints;        // Number of tyre stints up to maximum
    uint8_t tyreStintsActual[8];  // Actual tyres used by this driver
    uint8_t tyreStintsVisual[8];  // Visual tyres used by this driver
    uint8_t tyreStintsEndLaps[8]; // The lap number stints end on
};

struct PacketFinalClassificationData
{
    PacketHeader header;                            // Header
    uint8_t numCars;                                // Number of cars in the final classification
    FinalClassificationData classificationData[22]; // Classification data for each car
};

struct LobbyInfoData
{
    uint8_t aiControlled; // Whether the vehicle is AI (1) or Human (0) controlled
    uint8_t teamId;       // Team id - see appendix (255 if no team currently selected)
    uint8_t nationality;  // Nationality of the driver
    uint8_t platform;     // 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
    uint8_t name[48];     // Name of participant in UTF-8 format – null terminated
                          // Will be truncated with ... (U+2026) if too long
    uint8_t carNumber;    // Car number of the player
    uint8_t readyStatus;  // 0 = not ready, 1 = ready, 2 = spectating
};

struct PacketLobbyInfoData
{
    PacketHeader header;            // Header
    uint8_t numPlayers;             // Number of players in the lobby data
    LobbyInfoData lobbyPlayers[22]; // Lobby player information
};

struct CarDamageData
{
    float tyres_wear[4];             // Tyre wear (percentage)
    uint8_t tyres_damage[4];         // Tyre damage (percentage)
    uint8_t brakes_damage[4];        // Brakes damage (percentage)
    uint8_t front_left_wing_damage;  // Front left wing damage (percentage)
    uint8_t front_right_wing_damage; // Front right wing damage (percentage)
    uint8_t rear_wing_damage;        // Rear wing damage (percentage)
    uint8_t floor_damage;            // Floor damage (percentage)
    uint8_t diffuser_damage;         // Diffuser damage (percentage)
    uint8_t sidepod_damage;          // Sidepod damage (percentage)
    uint8_t drs_fault;               // Indicator for DRS fault, 0 = OK, 1 = fault
    uint8_t ers_fault;               // Indicator for ERS fault, 0 = OK, 1 = fault
    uint8_t gear_box_damage;         // Gear box damage (percentage)
    uint8_t engine_damage;           // Engine damage (percentage)
    uint8_t engine_mguh_wear;        // Engine wear MGU-H (percentage)
    uint8_t engine_es_wear;          // Engine wear ES (percentage)
    uint8_t engine_ce_wear;          // Engine wear CE (percentage)
    uint8_t engine_ice_wear;         // Engine wear ICE (percentage)
    uint8_t engine_mguk_wear;        // Engine wear MGU-K (percentage)
    uint8_t engine_tc_wear;          // Engine wear TC (percentage)
    uint8_t engine_blown;            // Engine blown, 0 = OK, 1 = fault
    uint8_t engine_seized;           // Engine seized, 0 = OK, 1 = fault
};

struct PacketCarDamageData
{
    PacketHeader header;               // Header
    CarDamageData car_damage_data[22]; // Car damage data for 22 cars
};

struct LapHistoryData
{
    uint32_t lapTimeInMS;       // Lap time in milliseconds
    uint16_t sector1TimeInMS;   // Sector 1 time in milliseconds
    uint8_t sector1TimeMinutes; // Sector 1 whole minute part
    uint16_t sector2TimeInMS;   // Sector 2 time in milliseconds
    uint8_t sector2TimeMinutes; // Sector 2 whole minute part
    uint16_t sector3TimeInMS;   // Sector 3 time in milliseconds
    uint8_t sector3TimeMinutes; // Sector 3 whole minute part
    uint8_t lapValidBitFlags;   // 0x01 bit set-lap valid, 0x02 bit set-sector 1 valid
                                // 0x04 bit set-sector 2 valid, 0x08 bit set-sector 3 valid
};

struct TyreStintHistoryData
{
    uint8_t endLap;             // Lap the tyre usage ends on (255 if current tyre)
    uint8_t tyreActualCompound; // Actual tyres used by this driver
    uint8_t tyreVisualCompound; // Visual tyres used by this driver
};

struct PacketSessionHistoryData
{
    PacketHeader header;                // Header
    uint8_t carIdx;                     // Index of the car this lap data relates to
    uint8_t numLaps;                    // Number of laps in the data (including current partial lap)
    uint8_t numTyreStints;              // Number of tyre stints in the data
    uint8_t bestLapTimeLapNum;          // Lap the best lap time was achieved on
    uint8_t bestSector1LapNum;          // Lap the best Sector 1 time was achieved on
    uint8_t bestSector2LapNum;          // Lap the best Sector 2 time was achieved on
    uint8_t bestSector3LapNum;          // Lap the best Sector 3 time was achieved on
    LapHistoryData lapHistoryData[100]; // 100 laps of data max
    TyreStintHistoryData tyreStintsHistoryData[8];
};

// Tyre Set Data struct
struct TyreSetData
{
    uint8_t m_actualTyreCompound; // Actual tyre compound used
    uint8_t m_visualTyreCompound; // Visual tyre compound used
    uint8_t m_wear;               // Tyre wear (percentage)
    uint8_t m_available;          // Whether this set is currently available
    uint8_t m_recommendedSession; // Recommended session for tyre set
    uint8_t m_lifeSpan;           // Laps left in this tyre set
    uint8_t m_usableLife;         // Max number of laps recommended for this compound
    int16_t m_lapDeltaTime;       // Lap delta time in milliseconds compared to fitted set
    uint8_t m_fitted;             // Whether the set is fitted or not
};

// Packet Tyre Sets Data struct
struct PacketTyreSetsData
{
    PacketHeader m_header;         // Header
    uint8_t m_carIdx;              // Index of the car this data relates to
    TyreSetData m_tyreSetData[20]; // 13 (dry) + 7 (wet)
    uint8_t m_fittedIdx;           // Index into array of fitted tyre
};

// Packet Motion Extended Data struct
struct PacketMotionExData
{
    PacketHeader m_header;             // Header
    float m_suspensionPosition[4];     // Suspension position for each wheel (RL, RR, FL, FR)
    float m_suspensionVelocity[4];     // Suspension velocity for each wheel
    float m_suspensionAcceleration[4]; // Suspension acceleration for each wheel
    float m_wheelSpeed[4];             // Speed of each wheel
    float m_wheelSlipRatio[4];         // Slip ratio for each wheel
    float m_wheelSlipAngle[4];         // Slip angles for each wheel
    float m_wheelLatForce[4];          // Lateral forces for each wheel
    float m_wheelLongForce[4];         // Longitudinal forces for each wheel
    float m_heightOfCOGAboveGround;    // Height of centre of gravity above ground
    float m_localVelocityX;            // Velocity in local space – metres/s
    float m_localVelocityY;            // Velocity in local space
    float m_localVelocityZ;            // Velocity in local space
    float m_angularVelocityX;          // Angular velocity x-component – radians/s
    float m_angularVelocityY;          // Angular velocity y-component
    float m_angularVelocityZ;          // Angular velocity z-component
    float m_angularAccelerationX;      // Angular acceleration x-component – radians/s/s
    float m_angularAccelerationY;      // Angular acceleration y-component
    float m_angularAccelerationZ;      // Angular acceleration z-component
    float m_frontWheelsAngle;          // Current front wheels angle in radians
    float m_wheelVertForce[4];         // Vertical forces for each wheel
};

#pragma pack(pop)
#endif // DATATYPES_H
