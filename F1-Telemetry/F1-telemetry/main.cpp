#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

#pragma pack(push, 1)
struct CarMotionData {
    float worldPositionX;
    float worldPositionY;
    float worldPositionZ;
    float worldVelocityX;
    float worldVelocityY;
    float worldVelocityZ;
    int16_t worldForwardDirX;
    int16_t worldForwardDirY;
    int16_t worldForwardDirZ;
    int16_t worldRightDirX;
    int16_t worldRightDirY;
    int16_t worldRightDirZ;
    float gForceLateral;
    float gForceLongitudinal;
    float gForceVertical;
    float yaw;
    float pitch;
    float roll;
};

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

struct PacketMotionData {
    PacketHeader header;
    CarMotionData carMotionData[22];
};
#pragma pack(pop)


int main() {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        std::cerr << "Socket creation failed." << std::endl;
        return 1;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(20777);

    if (bind(sock, (sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
        std::cerr << "Bind failed." << std::endl;
        close(sock);
        return 1;
    }

    std::cout << "Listening for F1 23 UDP packets on port 20777..." << std::endl;

    char buffer[2048];
    sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);

    while (true) {
        int bytesReceived = recvfrom(sock, buffer, sizeof(buffer), 0, (sockaddr*)&clientAddr, &clientAddrLen);
        if (bytesReceived == -1) {
            std::cerr << "recvfrom failed." << std::endl;
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

    close(sock);
    return 0;
}
