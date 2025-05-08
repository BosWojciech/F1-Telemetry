#include "network/udpClient.h"
#include "core/DataTypes.h"
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h> // Also include here for consistency and portability
#include <cstring>
#include <sys/types.h> // Ensure ssize_t is defined

UdpClient::UdpClient(int port) : port_(port), sock_(-1) {}

bool UdpClient::initialize() {
    sock_ = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock_ == -1) {
        std::cerr << "Socket creation failed." << std::endl;
        return false;
    }

    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(port_);

    if (bind(sock_, (sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
        std::cerr << "Bind failed on port " << port_ << "." << std::endl;
        close(sock_);
        sock_ = -1;
        return false;
    }

    std::cout << "Listening for UDP packets on port " << port_ << "..." << std::endl;
    return true;
}

ssize_t UdpClient::receiveData(char* buffer, size_t bufferSize) {
    if (sock_ == -1) {
        std::cerr << "Socket not initialized." << std::endl;
        return -1;
    }

    sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);
    ssize_t bytesReceived = recvfrom(sock_, buffer, bufferSize, 0, (sockaddr*)&clientAddr, &clientAddrLen);
    return bytesReceived;
}

int UdpClient::getSocket() const {
    return sock_;
}

UdpClient::~UdpClient() {
    if (sock_ != -1) {
        close(sock_);
    }
}