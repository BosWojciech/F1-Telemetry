#include <iostream>
#include <nlohmann/json.hpp>


namespace ZmqServer {
    void initialise();
    void send(const std::string& topic, const nlohmann::json& payload);
}