#ifndef ZMQPUBLISHER_H
#define ZMQPUBLISHER_H

#include <string>
#include <nlohmann/json.hpp>
#include "cppzmq/zmq.hpp"

namespace ZmqPublisher {
    extern zmq::context_t context;
    extern zmq::socket_t publisher;

    void initialize();
    void send(const std::string& topic, const nlohmann::json& payload);
}

#endif // ZMQPUBLISHER_H
