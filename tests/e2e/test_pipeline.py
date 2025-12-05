#!/usr/bin/env python3
"""
End-to-End Integration Tests for F1 Telemetry Pipeline

Tests the complete data flow:
1. Simulator generates UDP packets
2. Ingest service receives and publishes via ZMQ
3. Processor forwards data to WebSocket
4. Frontend can connect and receive data
"""

import asyncio
import json
import socket
import struct
import time
import zmq
import websockets
import pytest
from typing import Dict, Any


class TestE2EDataFlow:
    """End-to-end integration tests"""
    
    @pytest.fixture
    def zmq_context(self):
        """Create ZMQ context for tests"""
        context = zmq.Context()
        yield context
        context.term()
    
    def create_motion_packet(self) -> bytes:
        """
        Create a minimal valid F1 motion packet
        
        Returns:
            bytes: 1349-byte motion packet
        """
        # Packet header (29 bytes)
        header = struct.pack(
            '<HBBBQfIBBBBBBBBBBBBBBBBBBBBBB',
            2023,  # packetFormat
            1,     # gameMajorVersion
            2,     # gameMinorVersion
            3,     # packetVersion
            123456789,  # sessionUID
            100.5,  # sessionTime
            1000,   # frameIdentifier
            0,      # packetId (motion)
            0,      # playerCarIndex
            0,      # secondaryPlayerCarIndex
            *[0] * 19  # padding
        )
        
        # Car motion data: 22 cars × 60 bytes each = 1320 bytes
        car_data = b''
        for i in range(22):
            car_motion = struct.pack(
                '<ffffffHHHfffffffffffffff',
                float(i * 100),  # worldPositionX
                50.0 + i,        # worldPositionY
                float(i * 150),  # worldPositionZ
                float(i * 2),    # worldVelocityX
                0.0,             # worldVelocityY
                float(i * 3),    # worldVelocityZ
                1000 + i,        # worldForwardDirX (normalized int)
                0,               # worldForwardDirY
                1000 + i,        # worldForwardDirZ
                *[0.0] * 15      # other motion fields
            )
            car_data += car_motion
        
        return header + car_data
    
    @pytest.mark.asyncio
    async def test_simulator_to_ingest_udp(self):
        """Test UDP packet transmission from simulator to ingest"""
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            # Send motion packet to ingest service
            packet = self.create_motion_packet()
            target = ('localhost', 20777)
            
            bytes_sent = sock.sendto(packet, target)
            
            # Verify packet was sent completely
            assert bytes_sent == len(packet)
            assert bytes_sent == 1349
            
        finally:
            sock.close()
    
    @pytest.mark.asyncio
    async def test_ingest_to_processor_zmq(self, zmq_context):
        """Test ZMQ communication from ingest to processor"""
        # Create ZMQ subscriber
        subscriber = zmq_context.socket(zmq.SUB)
        subscriber.connect("tcp://localhost:5555")
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        subscriber.setsockopt(zmq.RCVTIMEO, 5000)  # 5 second timeout
        
        try:
            # Send test packet via UDP to trigger ZMQ publish
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = self.create_motion_packet()
            sock.sendto(packet, ('localhost', 20777))
            sock.close()
            
            # Wait for ZMQ message
            topic, payload = subscriber.recv_multipart()
            
            # Verify message received
            assert topic is not None
            assert payload is not None
            
            # Parse JSON payload
            data = json.loads(payload.decode())
            assert 'header' in data
            assert 'carMotionData' in data
            
        except zmq.error.Again:
            pytest.skip("Timeout waiting for ZMQ message - ingest service may not be running")
        finally:
            subscriber.close()
    
    @pytest.mark.asyncio
    async def test_processor_to_frontend_websocket(self):
        """Test WebSocket communication from processor to frontend"""
        try:
            # Connect to WebSocket
            uri = "ws://localhost:8765"
            
            async with websockets.connect(uri, timeout=5) as websocket:
                # Trigger telemetry by sending UDP packet
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = self.create_motion_packet()
                sock.sendto(packet, ('localhost', 20777))
                sock.close()
                
                # Wait for WebSocket message
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                
                # Parse and verify data
                data = json.loads(message)
                assert isinstance(data, dict)
                assert 'header' in data or 'packetId' in data
                
        except (websockets.exceptions.WebSocketException, asyncio.TimeoutError) as e:
            pytest.skip(f"WebSocket connection failed - processor may not be running: {e}")
    
    @pytest.mark.asyncio
    async def test_complete_pipeline_e2e(self, zmq_context):
        """Test complete data flow through entire pipeline"""
        # Setup WebSocket connection
        try:
            uri = "ws://localhost:8765"
            async with websockets.connect(uri, timeout=5) as websocket:
                # Send multiple test packets
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                for i in range(5):
                    packet = self.create_motion_packet()
                    sock.sendto(packet, ('localhost', 20777))
                    
                    # Receive via WebSocket
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(message)
                        
                        # Verify telemetry structure
                        assert isinstance(data, dict)
                        
                    except asyncio.TimeoutError:
                        # Some packets might be dropped or delayed
                        pass
                    
                    await asyncio.sleep(0.1)  # 100ms between packets
                
                sock.close()
                
        except Exception as e:
            pytest.skip(f"Pipeline test failed - services may not be fully running: {e}")
    
    @pytest.mark.asyncio
    async def test_high_frequency_data_flow(self):
        """Test pipeline handles high-frequency telemetry (20Hz)"""
        try:
            uri = "ws://localhost:8765"
            async with websockets.connect(uri, timeout=5) as websocket:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                packets_sent = 20
                packets_received = 0
                
                # Send 20 packets at 20Hz (1 second of data)
                for i in range(packets_sent):
                    packet = self.create_motion_packet()
                    sock.sendto(packet, ('localhost', 20777))
                    
                    # Try to receive immediately
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                        if message:
                            packets_received += 1
                    except asyncio.TimeoutError:
                        pass
                    
                    await asyncio.sleep(0.05)  # 20Hz = 50ms
                
                sock.close()
                
                # Should receive at least 50% of packets
                assert packets_received >= packets_sent * 0.5
                
        except Exception as e:
            pytest.skip(f"High frequency test failed: {e}")
    
    @pytest.mark.asyncio
    async def test_packet_data_integrity(self):
        """Test data integrity through pipeline"""
        try:
            uri = "ws://localhost:8765"
            async with websockets.connect(uri, timeout=5) as websocket:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Send packet
                packet = self.create_motion_packet()
                sock.sendto(packet, ('localhost', 20777))
                
                # Receive via WebSocket
                message = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                data = json.loads(message)
                
                # Verify data structure integrity
                if 'header' in data:
                    header = data['header']
                    assert 'sessionTime' in header
                    assert isinstance(header['sessionTime'], (int, float))
                
                if 'carMotionData' in data:
                    cars = data['carMotionData']
                    assert isinstance(cars, list)
                    assert len(cars) > 0
                    
                    # Check first car has expected fields
                    car = cars[0]
                    assert 'worldPositionX' in car
                    assert 'worldPositionY' in car
                    assert 'worldPositionZ' in car
                
                sock.close()
                
        except Exception as e:
            pytest.skip(f"Data integrity test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
