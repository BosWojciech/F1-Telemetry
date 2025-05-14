#include "network/zmqPublisher.h"
#include <iostream>

// Define static members of ZmqPublisher namespace
namespace ZmqPublisher {
    zmq::context_t context(1);
    zmq::socket_t publisher(context, zmq::socket_type::pub);
}

void ZmqPublisher::initialize() {
    // Bind the publisher socket to a TCP endpoint
    ZmqPublisher::publisher.bind("tcp://*:5555");
    std::cout << "ZMQ publisher initialized and bound to tcp://*:5555" << std::endl;
}

void ZmqPublisher::send(const std::string& topic, const nlohmann::json& payload) {
    std::string msg = topic + " " + payload.dump();
    ZmqPublisher::publisher.send(zmq::buffer(msg), zmq::send_flags::none);
    //std::cout << "Sent message: " << msg << std::endl;
}
