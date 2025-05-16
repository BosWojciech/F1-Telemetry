#ifndef ZMQPUBLISHER_H
#define ZMQPUBLISHER_H

#include <string>
#include <nlohmann/json.hpp>
#include "cppzmq/zmq.hpp"

namespace ZmqPublisher {
    extern zmq::context_t context;
    extern zmq::socket_t publisher;

    void initialize(const std::string &endpoint);
    void send(const std::string& topic, nlohmann::json& payload);
    void shutdown();
}

#endif // ZMQPUBLISHER_H
