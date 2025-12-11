"""
Packet Generator for F1 Telemetry Simulator

Generates realistic F1 telemetry packets based on configuration.
"""

import random
import time
from typing import Dict, Any, Optional
import sys
import os

# Import generated protobuf classes
# Ensure the directory is in path
sys.path.append(os.path.dirname(__file__))
from proto import packet_definitions_pb2


class PacketGenerator:
    """Generates F1 telemetry packets using Protobuf"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize packet generator with configuration
        
        Args:
            config: Simulation configuration dictionary
        """
        self.config = config
        self.packet_types = config.get('packet_types', {})
        self.simulation_time = 0.0
        self.lap_number = 1
        self.session_time = 0.0
        
        # Packet format version (F1 2023/2024)
        self.packet_format = config.get('packet_format', 2023)
        
        # Initialize packet sequence
        self._init_packet_sequence()
    
    def _init_packet_sequence(self):
        """Initialize the sequence of packets to generate"""
        self.packet_sequence = []
        
        for packet_type, settings in self.packet_types.items():
            if settings.get('enabled', True):
                frequency = settings.get('frequency_hz', 1)
                self.packet_sequence.append({
                    'type': packet_type,
                    'frequency': frequency,
                    'last_sent': 0.0,
                    'settings': settings
                })
    
    def generate_next_packet(self) -> Optional[Dict[str, Any]]:
        """
        Generate the next packet in the sequence
        
        Returns:
            Dictionary containing packet type and binary data
        """
        current_time = time.time()
        
        # Find packet due to be sent
        for packet_info in self.packet_sequence:
            interval = 1.0 / packet_info['frequency']
            if current_time - packet_info['last_sent'] >= interval:
                packet_info['last_sent'] = current_time
                
                packet_type = packet_info['type']
                packet_data = self._generate_packet(packet_type, packet_info['settings'])
                
                return {
                    'type': packet_type,
                    'data': packet_data,
                    'delay': interval
                }
        
        return None
    
    def _generate_packet(self, packet_type: str, settings: Dict[str, Any]) -> bytes:
        """Generate specific packet type"""
        
        if packet_type == 'SessionData':
            return self._generate_session_packet(settings)
        elif packet_type == 'LapData':
            return self._generate_lap_packet(settings)
        elif packet_type == 'CarTelemetry':
            return self._generate_telemetry_packet(settings)
        elif packet_type == 'CarStatus':
            return self._generate_car_status_packet(settings)
        elif packet_type == 'Motion':
            return self._generate_motion_packet(settings)
        elif packet_type == 'Participants':
            return self._generate_participants_packet(settings)
        else:
            return b''
    
    def _create_packet_header(self, packet_id: int) -> packet_definitions_pb2.PacketHeader:
        """Generate common packet header"""
        header = packet_definitions_pb2.PacketHeader()
        header.packet_format = self.packet_format
        header.game_year = 23
        header.game_major_version = 1
        header.game_minor_version = 0
        header.packet_version = 1
        header.packet_id = packet_id
        header.session_uid = 12345678
        header.session_time = self.session_time
        header.frame_identifier = int(self.simulation_time * 60)
        header.overall_frame_identifier = int(self.simulation_time * 60)
        header.player_car_index = 0
        header.secondary_player_car_index = 255
        
        self.session_time += 0.016  # Increment by ~1 frame at 60Hz
        return header
    
    def _generate_session_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate session data packet (ID: 1)"""
        packet = packet_definitions_pb2.PacketSessionData()
        packet.header.CopyFrom(self._create_packet_header(1))
        
        packet.weather = settings.get('weather', 0)
        packet.track_temperature = int(settings.get('track_temperature', 25))
        packet.air_temperature = int(settings.get('air_temperature', 20))
        packet.total_laps = 58
        packet.track_length = 5303
        packet.session_type = 10 # Race
        packet.track_id = 0 # Melbourne
        packet.formula = 0 # F1 Modern
        packet.session_time_left = 3600
        packet.session_duration = 7200
        packet.pit_speed_limit = 80
        packet.game_paused = 0
        packet.is_spectating = 0
        packet.spectator_car_index = 0
        packet.sli_pro_native_support = 0
        packet.num_marshal_zones = 0
        packet.safety_car_status = 0
        packet.network_game = 0
        packet.num_weather_forecast_samples = 0
        
        return packet.SerializeToString()
    
    def _generate_lap_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate lap data packet (ID: 2)"""
        packet = packet_definitions_pb2.PacketLapData()
        packet.header.CopyFrom(self._create_packet_header(2))
        
        for i in range(22):
            lap_data = packet.lap_data.add()
            if i == 0:  # Player car
                lap_time = random.uniform(85.0, 95.0)
                sector1 = random.uniform(25.0, 30.0)
                sector2 = random.uniform(28.0, 33.0)
            else:
                lap_time = random.uniform(85.0, 100.0)
                sector1 = random.uniform(25.0, 35.0)
                sector2 = random.uniform(28.0, 38.0)
            
            lap_data.last_lap_time_in_ms = int(lap_time * 1000)
            lap_data.current_lap_time_in_ms = int(lap_time * 1000) # Simplified
            lap_data.sector1_time_in_ms = int(sector1 * 1000)
            lap_data.sector2_time_in_ms = int(sector2 * 1000)
            lap_data.car_position = self.lap_number if i == 0 else random.randint(1, 20)
            lap_data.current_lap_num = self.lap_number
            lap_data.num_pit_stops = 1
            
        return packet.SerializeToString()
    
    def _generate_telemetry_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate car telemetry packet (ID: 6)"""
        packet = packet_definitions_pb2.PacketCarTelemetryData()
        packet.header.CopyFrom(self._create_packet_header(6))
        
        for i in range(22):
            car_telemetry = packet.car_telemetry_data.add()
            if i == 0:  # Player car
                speed = random.uniform(200, 320)
                throttle = random.uniform(0.5, 1.0)
                brake = random.uniform(0.0, 0.3)
                gear = random.randint(5, 8)
            else:
                speed = random.uniform(150, 320)
                throttle = random.uniform(0.3, 1.0)
                brake = random.uniform(0.0, 0.5)
                gear = random.randint(3, 8)
            
            car_telemetry.speed = int(speed)
            car_telemetry.throttle = throttle
            car_telemetry.brake = brake
            car_telemetry.gear = gear
            car_telemetry.engine_rpm = random.randint(8000, 12000)
            car_telemetry.drs = 0
            car_telemetry.rev_lights_percent = random.randint(50, 100)
            
            car_telemetry.brakes_temperature.extend([random.randint(400, 600) for _ in range(4)])
            car_telemetry.tyres_surface_temperature.extend([random.randint(70, 90) for _ in range(4)])
            car_telemetry.tyres_inner_temperature.extend([random.randint(70, 90) for _ in range(4)])
            car_telemetry.engine_temperature = 90
            car_telemetry.tyres_pressure.extend([23.0] * 4)
            car_telemetry.surface_type.extend([0] * 4)

        return packet.SerializeToString()
    
    def _generate_car_status_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate car status packet (ID: 7)"""
        packet = packet_definitions_pb2.PacketCarStatusData()
        packet.header.CopyFrom(self._create_packet_header(7))
        
        for i in range(22):
            status = packet.car_status_data.add()
            status.traction_control = 1
            status.anti_lock_brakes = 0
            status.fuel_mix = 1
            status.front_brake_bias = 50
            status.pit_limiter_status = 0
            status.fuel_in_tank = 20.0
            status.fuel_capacity = 100.0
            status.max_rpm = 13500
            status.idle_rpm = 3000
            status.max_gears = 8
            status.drs_allowed = 0
            status.actual_tyre_compound = 16
            status.visual_tyre_compound = 16
            
        return packet.SerializeToString()
    
    def _generate_motion_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate motion packet (ID: 0)"""
        packet = packet_definitions_pb2.PacketMotionData()
        packet.header.CopyFrom(self._create_packet_header(0))
        
        for i in range(22):
            motion = packet.car_motion_data.add()
            motion.world_position_x = random.uniform(-1000, 1000)
            motion.world_position_y = random.uniform(-100, 100)
            motion.world_position_z = random.uniform(-1000, 1000)
            motion.world_velocity_x = random.uniform(-100, 100)
            motion.world_velocity_y = random.uniform(-100, 100)
            motion.world_velocity_z = random.uniform(-100, 100)
            
            motion.world_forward_dir_x = random.randint(-32768, 32767)
            motion.world_forward_dir_y = random.randint(-32768, 32767)
            motion.world_forward_dir_z = random.randint(-32768, 32767)
            
            motion.g_force_lateral = random.uniform(-5, 5)
            motion.g_force_longitudinal = random.uniform(-5, 5)
            motion.g_force_vertical = random.uniform(-5, 5)
            motion.yaw = random.uniform(-3.14, 3.14)
            motion.pitch = random.uniform(-1.57, 1.57)
            motion.roll = random.uniform(-1.57, 1.57)
            
        return packet.SerializeToString()
    
    def _generate_participants_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate participants packet (ID: 4)"""
        packet = packet_definitions_pb2.PacketParticipantsData()
        packet.header.CopyFrom(self._create_packet_header(4))
        
        num_cars = settings.get('num_cars', 20)
        packet.num_active_cars = num_cars
        
        for i in range(22):
            participant = packet.participants.add()
            if i < num_cars:
                participant.ai_controlled = 1
                participant.driver_id = i
                participant.name = f"Driver {i}"
                participant.nationality = 1
                participant.race_number = i + 1
                participant.team_id = i % 10
            
        return packet.SerializeToString()
    

