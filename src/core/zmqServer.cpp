#include "cppzmq/zmq.hpp"

static zmq::context_t context(1);
static zmq::socket_t publisher(context, zmq::socket_type::pub);

void ZmqServer::initialize() {
    publisher.bind("tcp://*:5555");
}

void ZmqServer::send(const std::string& topic, const nlohmann::json& payload) {
    std::string msg = topic + " " + payload.dump();
    publisher.send(zmq::buffer(msg), zmq::send_flags::none);
}
