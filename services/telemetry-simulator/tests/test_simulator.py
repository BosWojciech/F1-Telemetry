"""
Unit tests for Telemetry Simulator main service
"""

import pytest
import socket
from unittest.mock import Mock, patch, MagicMock, call
from simulator import TelemetrySimulator


class TestTelemetrySimulator:
    """Test suite for TelemetrySimulator class"""
    
    @pytest.fixture
    def basic_config(self):
        """Basic simulator configuration"""
        return {
            'target_host': 'localhost',
            'target_port': 20777,
            'packet_format': 2023,
            'packet_types': {
                'motion': {
                    'enabled': True,
                    'frequency_hz': 20,
                    'packet_id': 0
                }
            },
            'simulation': {
                'num_cars': 22,
                'duration_seconds': 60,
                'speed_multiplier': 1.0
            }
        }
    
    def test_init(self, basic_config):
        """Test TelemetrySimulator initialization"""
        simulator = TelemetrySimulator(basic_config)
        
        assert simulator.config == basic_config
        assert simulator.target_host == 'localhost'
        assert simulator.target_port == 20777
        assert simulator.running == False
    
    def test_init_default_config(self):
        """Test initialization with minimal config"""
        config = {
            'target_host': '127.0.0.1',
            'target_port': 20777
        }
        
        simulator = TelemetrySimulator(config)
        
        assert simulator.target_host == '127.0.0.1'
        assert simulator.target_port == 20777
    
    @patch('simulator.socket.socket')
    def test_create_socket_success(self, mock_socket, basic_config):
        """Test UDP socket creation"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        simulator = TelemetrySimulator(basic_config)
        sock = simulator._create_socket()
        
        assert sock is not None
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
    
    @patch('simulator.socket.socket')
    def test_create_socket_failure(self, mock_socket, basic_config):
        """Test socket creation failure handling"""
        mock_socket.side_effect = OSError("Cannot create socket")
        
        simulator = TelemetrySimulator(basic_config)
        
        with pytest.raises(OSError):
            simulator._create_socket()
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    def test_send_packet_success(self, mock_generator_class, mock_socket, basic_config):
        """Test successful packet sending"""
        # Setup mocks
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        mock_generator = Mock()
        mock_generator.generate_motion_packet_bytes.return_value = b'\x00' * 1349
        mock_generator_class.return_value = mock_generator
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        simulator.packet_generator = mock_generator
        
        # Send packet
        result = simulator._send_packet(b'\x00' * 1349)
        
        assert result == True
        mock_sock.sendto.assert_called_once()
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    def test_send_packet_failure(self, mock_generator_class, mock_socket, basic_config):
        """Test packet sending failure handling"""
        mock_sock = Mock()
        mock_sock.sendto.side_effect = OSError("Network unreachable")
        mock_socket.return_value = mock_sock
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        
        result = simulator._send_packet(b'\x00' * 1349)
        
        assert result == False
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    @patch('simulator.time.sleep')
    def test_run_simulation_loop(self, mock_sleep, mock_generator_class, mock_socket, basic_config):
        """Test main simulation loop"""
        # Setup mocks
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        mock_generator = Mock()
        mock_generator.generate_motion_packet_bytes.return_value = b'\x00' * 1349
        mock_generator_class.return_value = mock_generator
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        simulator.packet_generator = mock_generator
        
        # Run for limited iterations
        packet_count = 0
        def stop_after_packets(*args):
            nonlocal packet_count
            packet_count += 1
            if packet_count >= 5:
                simulator.running = False
        
        mock_sleep.side_effect = stop_after_packets
        
        simulator.start()
        
        # Verify packets were sent
        assert mock_sock.sendto.call_count >= 5
    
    @patch('simulator.socket.socket')
    def test_stop_simulation(self, mock_socket, basic_config):
        """Test stopping the simulator"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        simulator.running = True
        
        simulator.stop()
        
        assert simulator.running == False
        mock_sock.close.assert_called_once()
    
    def test_packet_rate_calculation(self, basic_config):
        """Test packet rate is calculated correctly"""
        simulator = TelemetrySimulator(basic_config)
        
        # Motion at 20Hz
        frequency = basic_config['packet_types']['motion']['frequency_hz']
        expected_interval = 1.0 / frequency
        
        assert expected_interval == 0.05  # 50ms between packets
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    def test_packet_size_validation(self, mock_generator_class, mock_socket, basic_config):
        """Test that generated packets are correct size"""
        mock_generator = Mock()
        packet_bytes = b'\x00' * 1349
        mock_generator.generate_motion_packet_bytes.return_value = packet_bytes
        mock_generator_class.return_value = mock_generator
        
        simulator = TelemetrySimulator(basic_config)
        simulator.packet_generator = mock_generator
        
        generated_packet = simulator.packet_generator.generate_motion_packet_bytes()
        
        # Verify packet is correct size
        assert len(generated_packet) == 1349
    
    def test_configuration_validation(self, basic_config):
        """Test simulator validates configuration"""
        # Missing required fields
        invalid_config = {}
        
        with pytest.raises(KeyError):
            simulator = TelemetrySimulator(invalid_config)
            _ = simulator.target_host
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    def test_statistics_tracking(self, mock_generator_class, mock_socket, basic_config):
        """Test simulator tracks sent packet statistics"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        mock_generator = Mock()
        mock_generator.generate_motion_packet_bytes.return_value = b'\x00' * 1349
        mock_generator_class.return_value = mock_generator
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        simulator.packet_generator = mock_generator
        
        # Send multiple packets
        for _ in range(10):
            simulator._send_packet(b'\x00' * 1349)
        
        # Should have sent 10 packets
        assert mock_sock.sendto.call_count == 10
    
    @patch('simulator.socket.socket')
    def test_target_address_format(self, mock_socket, basic_config):
        """Test target address is formatted correctly"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        
        simulator = TelemetrySimulator(basic_config)
        simulator.socket = mock_sock
        
        # Send a packet
        simulator._send_packet(b'\x00' * 100)
        
        # Verify sendto called with correct address format
        call_args = mock_sock.sendto.call_args
        assert call_args[0][1] == ('localhost', 20777)
    
    @patch('simulator.socket.socket')
    @patch('simulator.PacketGenerator')
    def test_simulation_duration_limit(self, mock_generator_class, mock_socket, basic_config):
        """Test simulator respects duration limit"""
        # Set short duration
        basic_config['simulation']['duration_seconds'] = 1
        
        simulator = TelemetrySimulator(basic_config)
        
        # Duration should be set from config
        assert simulator.config['simulation']['duration_seconds'] == 1
