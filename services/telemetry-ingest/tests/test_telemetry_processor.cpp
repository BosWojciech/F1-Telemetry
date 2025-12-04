#include <gtest/gtest.h>
#include "core/TelemetryProcessor.h"
#include "core/DataTypes.h"
#include <nlohmann/json.hpp>

class TelemetryProcessorTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code if needed
    }
};

TEST_F(TelemetryProcessorTest, ProcessPacketMotionData_ValidData) {
    PacketMotionData testData;
    memset(&testData, 0, sizeof(testData));
    
    // Set up header
    testData.header.packetFormat = 2024;
    testData.header.packetId = 0;
    testData.header.sessionUID = 12345678;
    testData.header.sessionTime = 1.5f;
    
    // Set up car motion data
    testData.carMotionData[0].worldPositionX = 100.5f;
    testData.carMotionData[0].worldPositionY = 50.0f;
    testData.carMotionData[0].worldPositionZ = 200.0f;
    
    nlohmann::json result = TelemetryProcessor::processPacketMotionData(testData);
    
    EXPECT_TRUE(result.contains("header"));
    EXPECT_TRUE(result.contains("carMotionData"));
    EXPECT_EQ(result["header"]["packetId"], 0);
    EXPECT_EQ(result["header"]["packetFormat"], 2024);
}

TEST_F(TelemetryProcessorTest, ProcessPacketMotionData_ArraySize) {
    PacketMotionData testData;
    memset(&testData, 0, sizeof(testData));
    
    nlohmann::json result = TelemetryProcessor::processPacketMotionData(testData);
    
    EXPECT_TRUE(result.contains("carMotionData"));
    EXPECT_EQ(result["carMotionData"].size(), 22);
}

TEST_F(TelemetryProcessorTest, ProcessPacketMotionData_HeaderFields) {
    PacketMotionData testData;
    memset(&testData, 0, sizeof(testData));
    
    testData.header.gameYear = 24;
    testData.header.gameMajorVersion = 1;
    testData.header.gameMinorVersion = 0;
    testData.header.playerCarIndex = 5;
    
    nlohmann::json result = TelemetryProcessor::processPacketMotionData(testData);
    
    EXPECT_EQ(result["header"]["gameYear"], 24);
    EXPECT_EQ(result["header"]["gameMajorVersion"], 1);
    EXPECT_EQ(result["header"]["gameMinorVersion"], 0);
    EXPECT_EQ(result["header"]["playerCarIndex"], 5);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
