"""
Unit tests for Packet Generator
"""

import pytest
import struct
from unittest.mock import Mock, patch
from packet_generator import PacketGenerator


class TestPacketGenerator:
    """Test suite for PacketGenerator class"""
    
    @pytest.fixture
    def basic_config(self):
        """Basic configuration for testing"""
        return {
            'packet_format': 2023,
            'packet_types': {
                'motion': {
                    'enabled': True,
                    'frequency_hz': 20,
                    'packet_id': 0
                },
                'session': {
                    'enabled': True,
                    'frequency_hz': 2,
                    'packet_id': 1
                }
            },
            'simulation': {
                'num_cars': 22,
                'duration_seconds': 300
            }
        }
    
    def test_init(self, basic_config):
        """Test PacketGenerator initialization"""
        generator = PacketGenerator(basic_config)
        
        assert generator.config == basic_config
        assert generator.packet_format == 2023
        assert generator.simulation_time == 0.0
        assert generator.lap_number == 1
        assert generator.session_time == 0.0
    
    def test_init_packet_sequence(self, basic_config):
        """Test packet sequence initialization"""
        generator = PacketGenerator(basic_config)
        
        # Should have sequences for enabled packet types
        assert len(generator.packet_sequence) == 2
        
        # Check motion packet in sequence
        motion_seq = next((p for p in generator.packet_sequence if p['type'] == 'motion'), None)
        assert motion_seq is not None
        assert motion_seq['frequency'] == 20
    
    def test_generate_motion_packet_structure(self, basic_config):
        """Test motion packet structure and size"""
        generator = PacketGenerator(basic_config)
        
        # Generate motion packet
        packet = generator.generate_motion_packet()
        
        # Verify packet structure
        assert 'header' in packet
        assert 'carMotionData' in packet
        
        # Should have 22 cars
        assert len(packet['carMotionData']) == 22
        
        # Each car should have required fields
        for car_data in packet['carMotionData']:
            assert 'worldPositionX' in car_data
            assert 'worldPositionY' in car_data
            assert 'worldPositionZ' in car_data
            assert 'worldVelocityX' in car_data
            assert 'worldVelocityY' in car_data
            assert 'worldVelocityZ' in car_data
    
    def test_generate_motion_packet_size(self, basic_config):
        """Test motion packet generates correct byte size"""
        generator = PacketGenerator(basic_config)
        
        # Generate and serialize packet
        packet_data = generator.generate_motion_packet_bytes()
        
        # Motion packet should be 1349 bytes
        # Header (29 bytes) + 22 cars (60 bytes each) = 1349 bytes
        expected_size = 29 + (22 * 60)
        assert len(packet_data) == expected_size
        assert len(packet_data) == 1349
    
    def test_packet_header_fields(self, basic_config):
        """Test packet header contains required fields"""
        generator = PacketGenerator(basic_config)
        
        packet = generator.generate_motion_packet()
        header = packet['header']
        
        # Check required header fields
        assert 'packetFormat' in header
        assert 'packetId' in header
        assert 'packetVersion' in header
        assert 'sessionTime' in header
        assert 'frameIdentifier' in header
        
        # Verify types
        assert isinstance(header['packetFormat'], int)
        assert isinstance(header['sessionTime'], float)
    
    def test_car_motion_data_realistic_values(self, basic_config):
        """Test car motion data contains realistic racing values"""
        generator = PacketGenerator(basic_config)
        
        packet = generator.generate_motion_packet()
        car_data = packet['carMotionData'][0]  # First car
        
        # Position values should be reasonable (track coordinates)
        assert -10000 <= car_data['worldPositionX'] <= 10000
        assert -1000 <= car_data['worldPositionY'] <= 1000
        assert -10000 <= car_data['worldPositionZ'] <= 10000
        
        # Velocity values should be reasonable for F1 (m/s)
        assert -150 <= car_data['worldVelocityX'] <= 150
        assert -50 <= car_data['worldVelocityY'] <= 50
        assert -150 <= car_data['worldVelocityZ'] <= 150
    
    def test_generate_multiple_packets(self, basic_config):
        """Test generating multiple sequential packets"""
        generator = PacketGenerator(basic_config)
        
        packets = []
        for _ in range(10):
            packet = generator.generate_motion_packet()
            packets.append(packet)
            generator.simulation_time += 0.05  # 20Hz = 50ms
        
        # Verify all packets generated successfully
        assert len(packets) == 10
        
        # Session time should increase
        assert packets[-1]['header']['sessionTime'] > packets[0]['header']['sessionTime']
    
    def test_packet_id_correct(self, basic_config):
        """Test packet ID is set correctly"""
        generator = PacketGenerator(basic_config)
        
        motion_packet = generator.generate_motion_packet()
        
        # Motion packet should have ID 0
        assert motion_packet['header']['packetId'] == 0
    
    def test_disabled_packet_type(self):
        """Test disabled packet types are not generated"""
        config = {
            'packet_format': 2023,
            'packet_types': {
                'motion': {
                    'enabled': False,
                    'frequency_hz': 20,
                    'packet_id': 0
                }
            }
        }
        
        generator = PacketGenerator(config)
        
        # Should not have motion in sequence if disabled
        motion_seq = next((p for p in generator.packet_sequence if p['type'] == 'motion'), None)
        assert motion_seq is None
    
    def test_packet_frequency_timing(self, basic_config):
        """Test packet generation respects frequency settings"""
        generator = PacketGenerator(basic_config)
        
        # Motion at 20Hz should generate every 0.05 seconds
        motion_interval = 1.0 / 20
        
        # Get motion packet settings
        motion_seq = next(p for p in generator.packet_sequence if p['type'] == 'motion')
        
        # Verify frequency calculation
        expected_interval = 1.0 / motion_seq['frequency']
        assert abs(expected_interval - motion_interval) < 0.001
    
    def test_session_time_progression(self, basic_config):
        """Test session time progresses correctly"""
        generator = PacketGenerator(basic_config)
        
        initial_time = generator.session_time
        
        # Simulate some time passing
        generator.simulation_time = 10.5
        packet = generator.generate_motion_packet()
        
        # Session time should be updated
        assert packet['header']['sessionTime'] >= initial_time
    
    def test_generate_bytes_returns_bytes(self, basic_config):
        """Test packet bytes generation returns bytes type"""
        generator = PacketGenerator(basic_config)
        
        packet_bytes = generator.generate_motion_packet_bytes()
        
        assert isinstance(packet_bytes, bytes)
        assert len(packet_bytes) > 0
    
    def test_multiple_car_data_uniqueness(self, basic_config):
        """Test that different cars have different telemetry data"""
        generator = PacketGenerator(basic_config)
        
        packet = generator.generate_motion_packet()
        car_data = packet['carMotionData']
        
        # At least some cars should have different positions
        positions = [(c['worldPositionX'], c['worldPositionZ']) for c in car_data[:5]]
        unique_positions = set(positions)
        
        # Should have some variation (not all cars at exact same position)
        assert len(unique_positions) > 1
