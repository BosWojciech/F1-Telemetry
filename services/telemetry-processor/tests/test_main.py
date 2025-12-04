"""
Unit tests for Telemetry Processor main service
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from main import TelemetryProcessor


class TestTelemetryProcessor:
    """Test suite for TelemetryProcessor class"""
    
    def test_init_passthrough_mode(self):
        """Test processor initialization in passthrough mode"""
        processor = TelemetryProcessor(mode="passthrough")
        
        assert processor.mode == "passthrough"
        assert processor.zmq_client is None
        assert processor.websocket_server is None
        assert processor.running == False
    
    def test_init_datacollection_mode(self):
        """Test processor initialization in datacollection mode"""
        processor = TelemetryProcessor(mode="datacollection")
        
        assert processor.mode == "datacollection"
        assert processor.running == False
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_handle_telemetry_passthrough(self, mock_zmq, mock_ws):
        """Test telemetry data handling in passthrough mode"""
        processor = TelemetryProcessor(mode="passthrough")
        
        # Setup mock WebSocket server
        mock_ws_instance = Mock()
        processor.websocket_server = mock_ws_instance
        
        # Test data
        test_topic = "telemetry"
        test_payload = {
            "packetId": 0,
            "sessionTime": 123.45,
            "carMotionData": [
                {"worldPositionX": 100.5, "worldPositionY": 200.3, "worldPositionZ": 50.1}
            ]
        }
        
        # Handle data
        processor._handle_telemetry_data(test_topic, test_payload)
        
        # Verify data was sent to WebSocket
        mock_ws_instance.send.assert_called_once()
        sent_data = json.loads(mock_ws_instance.send.call_args[0][0])
        assert sent_data == test_payload
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_handle_telemetry_datacollection(self, mock_zmq, mock_ws):
        """Test telemetry data handling in datacollection mode"""
        processor = TelemetryProcessor(mode="datacollection")
        
        # Setup mock WebSocket server
        mock_ws_instance = Mock()
        processor.websocket_server = mock_ws_instance
        
        test_topic = "telemetry"
        test_payload = {"packetId": 1, "frameIdentifier": 100}
        
        # Handle data
        processor._handle_telemetry_data(test_topic, test_payload)
        
        # Should still forward to WebSocket in current implementation
        mock_ws_instance.send.assert_called_once()
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_handle_telemetry_with_invalid_json(self, mock_zmq, mock_ws):
        """Test handling telemetry with data that can't be serialized"""
        processor = TelemetryProcessor(mode="passthrough")
        
        mock_ws_instance = Mock()
        mock_ws_instance.send.side_effect = TypeError("Not JSON serializable")
        processor.websocket_server = mock_ws_instance
        
        # Should not crash on serialization error
        processor._handle_telemetry_data("topic", {"invalid": object()})
    
    def test_stop(self):
        """Test graceful shutdown of processor"""
        processor = TelemetryProcessor(mode="passthrough")
        processor.running = True
        
        mock_zmq = Mock()
        processor.zmq_client = mock_zmq
        
        processor.stop()
        
        assert processor.running == False
        assert mock_zmq.stop == True
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_process_multiple_packets(self, mock_zmq, mock_ws):
        """Test processing multiple telemetry packets"""
        processor = TelemetryProcessor(mode="passthrough")
        
        mock_ws_instance = Mock()
        processor.websocket_server = mock_ws_instance
        
        # Process multiple packets
        packets = [
            {"packetId": 0, "sessionTime": 1.0},
            {"packetId": 0, "sessionTime": 1.1},
            {"packetId": 0, "sessionTime": 1.2},
        ]
        
        for packet in packets:
            processor._handle_telemetry_data("telemetry", packet)
        
        # Verify all packets were processed
        assert mock_ws_instance.send.call_count == len(packets)
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_handle_empty_payload(self, mock_zmq, mock_ws):
        """Test handling of empty telemetry payload"""
        processor = TelemetryProcessor(mode="passthrough")
        
        mock_ws_instance = Mock()
        processor.websocket_server = mock_ws_instance
        
        # Empty payload should still be handled
        processor._handle_telemetry_data("telemetry", {})
        
        mock_ws_instance.send.assert_called_once()
        sent_data = json.loads(mock_ws_instance.send.call_args[0][0])
        assert sent_data == {}
    
    @patch('main.WebsocketServer')
    @patch('main.ZmqClient')
    def test_handle_large_payload(self, mock_zmq, mock_ws):
        """Test handling of large telemetry payload with 22 cars"""
        processor = TelemetryProcessor(mode="passthrough")
        
        mock_ws_instance = Mock()
        processor.websocket_server = mock_ws_instance
        
        # Simulate full motion packet with 22 cars
        large_payload = {
            "packetId": 0,
            "sessionTime": 100.5,
            "carMotionData": [
                {
                    "worldPositionX": i * 10.0,
                    "worldPositionY": i * 20.0,
                    "worldPositionZ": i * 5.0,
                    "worldVelocityX": i * 2.0,
                    "worldVelocityY": 0.0,
                    "worldVelocityZ": i * 3.0
                }
                for i in range(22)
            ]
        }
        
        processor._handle_telemetry_data("telemetry", large_payload)
        
        mock_ws_instance.send.assert_called_once()
        sent_data = json.loads(mock_ws_instance.send.call_args[0][0])
        assert len(sent_data["carMotionData"]) == 22
