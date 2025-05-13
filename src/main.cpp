#include <iostream>
#include <cstdint>
#include <cstring>
#include "network/udpClient.h"
#include "core/DataTypes.h"
#include "core/PacketHandlers.h"
#include "core/TelemetryProcessor.h"
#include "network/zmqPublisher.h"
#include "nlohmann/json.hpp"


// Define the expected size of PacketCarTelemetryData based on documentation

int main()
{
    std::cout << "Running F1 UDP Client" << std::endl;
    ZmqPublisher::initialize();

    // Check structure size at runtime
    if (sizeof(PacketCarTelemetryData) != PACKET_CAR_TELEMETRY_DATA_SIZE)
    {
        std::cerr << "ERROR: PacketCarTelemetryData size mismatch!" << std::endl;
        std::cerr << "  Struct size: " << sizeof(PacketCarTelemetryData)
                  << ", Expected: " << PACKET_CAR_TELEMETRY_DATA_SIZE << std::endl;
        return 1;
    }

    UdpClient client(20777);
    if (!client.initialize())
    {
        return 1;
    }

    char buffer[2048];

    while (true)
    {

        // clearing console
        std::cout << "\033[2J\033[H";

        ssize_t bytesReceived = client.receiveData(buffer, sizeof(buffer));
        if (bytesReceived == -1)
        {
            std::cerr << "Error receiving data." << std::endl;
            break;
        }

        if (static_cast<size_t>(bytesReceived) < sizeof(PacketHeader))
        {
            std::cerr << "Received packet too small for header!" << std::endl;
            continue;
        }

        PacketHeader header;
        std::memcpy(&header, buffer, sizeof(PacketHeader));

        switch (header.packetId)
        {
        case 0:
        { // PacketMotionData
            auto maybeData = PacketHandlers::handlePacketMotionData(bytesReceived, buffer);
            if (!maybeData.has_value()) break;

            PacketMotionData data = maybeData.value();

            nlohmann::json processedData = TelemetryProcessor::processPacketMotionData(data);
            ZmqPublisher::send("PacketMotionData", processedData);
            break;
        }
        case 1:
        { // PacketSessionData
            auto maybeData = PacketHandlers::handlePacketSessionData(bytesReceived, buffer);
            if(!maybeData.has_value()) break;

            PacketSessionData data = maybeData.value();

            nlohmann::json processedData = TelemetryProcessor::processPacketSessionData(data);
            ZmqPublisher::send("PacketSessionData", processedData);
            break;
        }
        case 2:
        { // PacketLapData
            auto maybeData = PacketHandlers::handlePacketLapData(bytesReceived, buffer);
            if(!maybeData.has_value()) break;

            PacketLapData data = maybeData.value();

            nlohmann::json processedData = TelemetryProcessor::processPacketLapData(data);
            ZmqPublisher::send("PacketLapData", processedData);
            break;
        }
        case 3:
        { // PacketEventData
            auto maybeData = PacketHandlers::handlePacketEventData(bytesReceived, buffer);
            if(!maybeData.has_value()) break;

            PacketEventData data = maybeData.value();

            nlohmann::json processedData = TelemetryProcessor::processPacketEventData(data);
            Zmq::send("PacketEventData", processedData);
            break;
        }
        case 4:
        { // PacketParticipantsData
            break;
        }
        case 5:
        { // PacketCarSetupData
            break;
        }
        case 6:
        { // PacketCarTelemetryData
            //PacketCarTelemetryData data = PacketHandlers::handlePacketCarTelemetryData(bytesReceived, buffer);
            break;
        }
        case 7:
        { // PacketCarStatusData
            break;
        }
        case 8:
        { // PacketFinalClassificationData
            break;
        }
        case 9:
        { // PacketLobbyInfoData
            break;
        }
        case 10:
        { // PacketCarDamageData
            break;
        }
        case 11:
        { // PacketSessionHistoryData
            break;
        }
        case 12:
        { // PacketTyreSetsData
            break;
        }
        case 13:
        { // PacketMotionExData
            break;
        }
        default:
        {
            break;
        }
        }
    }

    return 0;
}
