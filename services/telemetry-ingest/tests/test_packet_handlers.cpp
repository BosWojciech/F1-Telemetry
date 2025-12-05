#include <gtest/gtest.h>
#include "core/PacketHandlers.h"
#include "core/DataTypes.h"
#include <cstring>

class PacketHandlersTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code if needed
    }

    void TearDown() override {
        // Cleanup code if needed
    }
};

TEST_F(PacketHandlersTest, ValidatePacket_CorrectSize) {
    // Test packet validation with correct size
    ssize_t bytesReceived = 1349;
    size_t correctSize = 1349;
    
    bool result = PacketHandlers::validatePacket(bytesReceived, correctSize, "TestPacket");
    
    EXPECT_TRUE(result);
}

TEST_F(PacketHandlersTest, ValidatePacket_IncorrectSize) {
    // Test packet validation with incorrect size
    ssize_t bytesReceived = 100;
    size_t correctSize = 1349;
    
    bool result = PacketHandlers::validatePacket(bytesReceived, correctSize, "TestPacket");
    
    EXPECT_FALSE(result);
}

TEST_F(PacketHandlersTest, HandlePacketMotionData_ValidPacket) {
    // Create a valid motion packet
    char buffer[PACKET_MOTION_DATA_SIZE];
    memset(buffer, 0, sizeof(buffer));
    
    // Fill in header
    PacketHeader* header = reinterpret_cast<PacketHeader*>(buffer);
    header->packetFormat = 2024;
    header->gameYear = 24;
    header->gameMajorVersion = 1;
    header->gameMinorVersion = 0;
    header->packetVersion = 1;
    header->packetId = 0;
    header->sessionUID = 12345678;
    header->sessionTime = 1.0f;
    header->frameIdentifier = 1;
    header->overallFrameIdentifier = 1;
    header->playerCarIndex = 0;
    header->secondaryPlayerCarIndex = 255;
    
    auto result = PacketHandlers::handlePacketMotionData(PACKET_MOTION_DATA_SIZE, buffer);
    
    EXPECT_TRUE(result.has_value());
    if (result.has_value()) {
        PacketMotionData data = result.value();
        EXPECT_EQ(data.header.packetFormat, 2024);
        EXPECT_EQ(data.header.packetId, 0);
    }
}

TEST_F(PacketHandlersTest, HandlePacketMotionData_InvalidSize) {
    // Create a packet with invalid size
    char buffer[100];
    memset(buffer, 0, sizeof(buffer));
    
    auto result = PacketHandlers::handlePacketMotionData(100, buffer);
    
    EXPECT_FALSE(result.has_value());
}

TEST_F(PacketHandlersTest, PacketHeader_StructSize) {
    // Verify packet header has correct size
    EXPECT_EQ(sizeof(PacketHeader), 29);
}

TEST_F(PacketHandlersTest, CarMotionData_StructSize) {
    // Verify car motion data has correct size
    EXPECT_EQ(sizeof(CarMotionData), 60);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
