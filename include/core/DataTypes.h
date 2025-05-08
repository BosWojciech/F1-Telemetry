#ifndef DATATYPES_H
#define DATATYPES_H

#include <cstdint>
#include <string>

#pragma pack(push, 1)

const size_t PACKET_CAR_TELEMETRY_DATA_SIZE = 1352;

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

// Car Telemetry Data struct
struct CarTelemetryData {
    uint16_t speed;                          // Speed of car in kilometres per hour
    float throttle;                          // Throttle applied (0.0 to 1.0)
    float steer;                             // Steering (-1.0 to 1.0)
    float brake;                             // Brake applied (0.0 to 1.0)
    uint8_t clutch;                          // Clutch applied (0 to 100)
    int8_t gear;                             // Gear (1-8, N=0, R=-1)
    uint16_t engineRPM;                      // Engine RPM
    uint8_t drs;                             // 0 = off, 1 = on
    uint8_t revLightsPercent;                // Rev lights percentage
    uint16_t revLightsBitValue;             // Rev lights bitfield
    uint16_t brakesTemperature[4];           // Brakes temperature (celsius)
    uint8_t tyresSurfaceTemperature[4];      // Tyres surface temperature (celsius)
    uint8_t tyresInnerTemperature[4];        // Tyres inner temperature (celsius)
    uint16_t engineTemperature;              // Engine temperature (celsius)
    float tyresPressure[4];                  // Tyres pressure (PSI)
    uint8_t surfaceType[4];                  // Driving surface type
};

// Packet Car Telemetry Data struct
struct PacketCarTelemetryData {
    PacketHeader header;                     // Header
    CarTelemetryData carTelemetryData[22];   // Telemetry data for all cars (22 total)
    uint8_t mfdPanelIndex;                   // MFD panel index (0–4 or 255 = closed)
    uint8_t mfdPanelIndexSecondaryPlayer;    // Secondary player MFD panel index
    int8_t suggestedGear;                    // Suggested gear (1–8, 0 = none)
};


#pragma pack(pop)
#endif // DATATYPES_H
