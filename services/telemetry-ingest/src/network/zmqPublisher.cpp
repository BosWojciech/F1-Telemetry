#include "network/zmqPublisher.h"
#include <nlohmann/json.hpp>
#include <iostream>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>

// Define static members of ZmqPublisher namespace
namespace ZmqPublisher {
    zmq::context_t context(1);
    zmq::socket_t publisher(context, zmq::socket_type::pub);
}

void ZmqPublisher::initialize(const std::string &endpoint) {
    try{
        ZmqPublisher::publisher.bind(endpoint);
        std::cout << "ZMQ publisher initialized and bound to "<< endpoint << std::endl;
    }catch (const zmq::error_t& e) {
        std::cerr << "ZMQ bind failed: " << e.what() << std::endl;
    }
    
}

void ZmqPublisher::send(const std::string& topic, nlohmann::json& payload) {
    try {
        auto now = std::chrono::system_clock::now();
        auto millis = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()).count();

        payload["layer1Timestamp"] = millis;
        std::cout << "[" << topic << "]: Sending payload" << std::endl;
        ZmqPublisher::publisher.send(zmq::buffer(topic), zmq::send_flags::sndmore);
        ZmqPublisher::publisher.send(zmq::buffer(payload.dump()), zmq::send_flags::none);
    } catch (const zmq::error_t& e) {
        std::cerr << "ZMQ send failed: " << e.what() << std::endl;
    }
}

void ZmqPublisher::shutdown() {
    ZmqPublisher::publisher.close();
    ZmqPublisher::context.close();
    std::cout << "ZMQ publisher shut down." << std::endl;
}
