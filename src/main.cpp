#include <iostream>
#include "UDP/udpClient.h"
#include "UDP/DataTypes.h"

int main() {
    std::cout << "Running F1 UDP Client" << std::endl;

    UdpClient client(20777);
    if (!client.initialize()) {
        return 1;
    }

    char buffer[2048];

    while (true) {
        ssize_t bytesReceived = client.receiveData(buffer, sizeof(buffer));
        if (bytesReceived == -1) {
            std::cerr << "Error receiving data." << std::endl;
            break;
        }

        if (bytesReceived < sizeof(PacketHeader)) {
            std::cerr << "Received packet too small!" << std::endl;
            continue;
        }

        auto* header = reinterpret_cast<PacketHeader*>(buffer);

        if (header->packetId == 0) {  // PacketMotionData
            auto* motionData = reinterpret_cast<PacketMotionData*>(buffer);
            uint8_t playerIndex = motionData->header.playerCarIndex;

            const CarMotionData& car = motionData->carMotionData[playerIndex];
            std::cout << "Player Car" << " -> X: " << car.worldPositionX
                      << ", Y: " << car.worldPositionY
                      << ", Z: " << car.worldPositionZ << std::endl;
        }
    }

    return 0;
}