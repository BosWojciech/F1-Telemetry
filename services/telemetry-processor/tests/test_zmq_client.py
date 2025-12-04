"""
Unit tests for ZMQ Client
"""

import pytest
import zmq
import json
from unittest.mock import Mock, patch, MagicMock
from zmq_client.zmq_client import ZmqClient


class TestZmqClient:
    """Test suite for ZmqClient class"""
    
    def test_init(self):
        """Test ZmqClient initialization"""
        address = "tcp://localhost:5555"
        topics = ["telemetry", "motion"]
        
        client = ZmqClient(address, topics)
        
        assert client.address == address
        assert client.topics == topics
        assert client.stop == False
        assert client.context is not None
        assert client.socket is not None
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_connect_success(self, mock_context):
        """Test successful ZMQ connection"""
        mock_socket = Mock()
        mock_context.return_value.socket.return_value = mock_socket
        
        client = ZmqClient("tcp://localhost:5555", [""])
        client.connect()
        
        mock_socket.connect.assert_called_once_with("tcp://localhost:5555")
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_connect_failure(self, mock_context):
        """Test ZMQ connection failure handling"""
        mock_socket = Mock()
        mock_socket.connect.side_effect = zmq.ZMQError("Connection failed")
        mock_context.return_value.socket.return_value = mock_socket
        
        client = ZmqClient("tcp://invalid:5555", [""])
        # Should not raise exception, just print error
        client.connect()
        
        mock_socket.connect.assert_called_once()
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_subscribe(self, mock_context):
        """Test subscription to topics"""
        mock_socket = Mock()
        mock_context.return_value.socket.return_value = mock_socket
        
        topics = ["telemetry", "motion", "lap"]
        client = ZmqClient("tcp://localhost:5555", topics)
        client.subscribe()
        
        # Verify each topic was subscribed
        assert mock_socket.setsockopt_string.call_count == len(topics)
        for topic in topics:
            mock_socket.setsockopt_string.assert_any_call(zmq.SUBSCRIBE, topic)
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_capture_data_success(self, mock_context):
        """Test successful data capture from ZMQ"""
        mock_socket = Mock()
        mock_context.return_value.socket.return_value = mock_socket
        
        # Mock ZMQ receiving data
        test_topic = b"telemetry"
        test_payload = {"packetId": 0, "speed": 200}
        test_payload_json = json.dumps(test_payload).encode()
        
        mock_socket.recv_multipart.return_value = [test_topic, test_payload_json]
        
        client = ZmqClient("tcp://localhost:5555", [""])
        topic, payload = client.captureData()
        
        assert topic == test_topic.decode()
        assert payload == test_payload
        assert isinstance(payload, dict)
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_capture_data_invalid_json(self, mock_context):
        """Test handling of invalid JSON from ZMQ"""
        mock_socket = Mock()
        mock_context.return_value.socket.return_value = mock_socket
        
        # Mock receiving invalid JSON
        test_topic = b"telemetry"
        invalid_json = b"not valid json {"
        
        mock_socket.recv_multipart.return_value = [test_topic, invalid_json]
        
        client = ZmqClient("tcp://localhost:5555", [""])
        topic, payload = client.captureData()
        
        # Should handle gracefully and return None
        assert topic is None or payload is None
    
    @patch('zmq_client.zmq_client.zmq.Context')
    def test_capture_data_zmq_error(self, mock_context):
        """Test handling of ZMQ errors during data capture"""
        mock_socket = Mock()
        mock_socket.recv_multipart.side_effect = zmq.ZMQError("Connection lost")
        mock_context.return_value.socket.return_value = mock_socket
        
        client = ZmqClient("tcp://localhost:5555", [""])
        topic, payload = client.captureData()
        
        # Should handle error gracefully
        assert topic is None
        assert payload is None
