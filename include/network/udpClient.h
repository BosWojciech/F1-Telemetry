#ifndef UDPCLIENT_H
#define UDPCLIENT_H

#include <cstddef> // For size_t

class UdpClient {
public:
    UdpClient(int port);
    bool initialize();
    ssize_t receiveData(char* buffer, size_t bufferSize);
    int getSocket() const;
    ~UdpClient();

private:
    int port_;
    int sock_;
};

#endif // UDPCLIENT_H