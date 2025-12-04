"""
Packet Generator for F1 Telemetry Simulator

Generates realistic F1 telemetry packets based on configuration.
"""

import struct
import random
import time
from typing import Dict, Any, Optional


class PacketGenerator:
    """Generates F1 telemetry packets"""
    
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
            return self._generate_generic_packet(settings)
    
    def _generate_packet_header(self, packet_id: int) -> bytes:
        """Generate common packet header"""
        # Header: packetFormat, gameYear, gameMajorVersion, gameMinorVersion, packetVersion, packetId, 
        #         sessionUID, sessionTime, frameIdentifier, overallFrameIdentifier, playerCarIndex, secondaryPlayerCarIndex
        header = struct.pack(
            '<HBBBBBQfIIBB',
            self.packet_format,  # packetFormat (uint16)
            24,  # gameYear (uint8) - F1 2024
            1,  # gameMajorVersion (uint8)
            0,  # gameMinorVersion (uint8)
            1,  # packetVersion (uint8)
            packet_id,  # packetId (uint8)
            12345678,  # sessionUID (uint64)
            self.session_time,  # sessionTime (float)
            int(self.simulation_time * 60),  # frameIdentifier (uint32)
            int(self.simulation_time * 60),  # overallFrameIdentifier (uint32)
            0,  # playerCarIndex (uint8)
            255   # secondaryPlayerCarIndex (uint8) - 255 means no second player
        )
        
        self.session_time += 0.016  # Increment by ~1 frame at 60Hz
        return header
    
    def _generate_session_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate session data packet (ID: 1)"""
        header = self._generate_packet_header(1)
        
        # Session data
        weather = settings.get('weather', 0)  # Clear
        track_temp = settings.get('track_temperature', 25)
        air_temp = settings.get('air_temperature', 20)
        
        session_data = struct.pack(
            '<BBhhBBBBBBHHHHHBBBBBBBBBBB',
            weather,  # weather
            int(track_temp),  # trackTemperature
            int(air_temp),  # airTemperature
            0,  # totalLaps
            2000,  # trackLength
            1,  # sessionType (race)
            1,  # trackId (Melbourne)
            1,  # formula (F1 Modern)
            3600,  # sessionTimeLeft
            3600,  # sessionDuration
            100,  # pitSpeedLimit
            0,  # gamePaused
            0,  # isSpectating
            0,  # spectatorCarIndex
            0,  # sliProNativeSupport
            22,  # numMarshalZones
            # Marshal zones (simplified)
            *[0] * 22,  # zoneStart
            *[0] * 22,  # zoneFlag
        )
        
        return header + session_data
    
    def _generate_lap_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate lap data packet (ID: 2)"""
        header = self._generate_packet_header(2)
        
        # Lap data for all 22 cars
        lap_data = b''
        for i in range(22):
            if i == 0:  # Player car
                lap_time = random.uniform(85.0, 95.0)
                sector1 = random.uniform(25.0, 30.0)
                sector2 = random.uniform(28.0, 33.0)
            else:
                lap_time = random.uniform(85.0, 100.0)
                sector1 = random.uniform(25.0, 35.0)
                sector2 = random.uniform(28.0, 38.0)
            
            car_lap_data = struct.pack(
                '<IfHHHHBBBBBBBBfBBHff',
                int(lap_time * 1000),  # lastLapTimeInMS
                lap_time,  # currentLapTimeInMS
                int(sector1 * 1000),  # sector1TimeInMS
                int(sector2 * 1000),  # sector2TimeInMS
                0,  # lapDistance
                0,  # totalDistance
                0,  # safetyCarDelta
                self.lap_number if i == 0 else random.randint(1, 5),  # carPosition
                self.lap_number,  # currentLapNum
                0,  # pitStatus
                1,  # numPitStops
                0,  # sector
                0,  # currentLapInvalid
                0,  # penalties
                0,  # warnings
                0,  # numUnservedDriveThroughPens
                0,  # numUnservedStopGoPens
                0,  # gridPosition
                0,  # driverStatus
                0.0,  # resultStatus
                0.0,  # pitLaneTimerActive
                0.0   # pitLaneTimeInLaneInMS
            )
            lap_data += car_lap_data
        
        return header + lap_data
    
    def _generate_telemetry_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate car telemetry packet (ID: 6)"""
        header = self._generate_packet_header(6)
        
        # Telemetry data for all 22 cars
        telemetry_data = b''
        for i in range(22):
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
            
            car_telemetry = struct.pack(
                '<HffBbHBBBBHHHHBBBB',
                int(speed),  # speed
                throttle,  # throttle
                brake,  # brake (simplified steering)
                brake,  # brake
                gear,  # gear
                random.randint(8000, 12000),  # engineRPM
                0,  # drs
                random.randint(50, 100),  # revLightsPercent
                random.randint(50, 100),  # revLightsBitValue
                random.randint(400, 600),  # brakesTemperature[0]
                random.randint(400, 600),  # brakesTemperature[1]
                random.randint(400, 600),  # brakesTemperature[2]
                random.randint(400, 600),  # brakesTemperature[3]
                random.randint(70, 90),  # tyresSurfaceTemperature[0]
                random.randint(70, 90),  # tyresSurfaceTemperature[1]
                random.randint(70, 90),  # tyresSurfaceTemperature[2]
                random.randint(70, 90),  # tyresSurfaceTemperature[3]
            )
            telemetry_data += car_telemetry
        
        # MFD panel and button status
        mfd_data = struct.pack('<BB', 0, 0)
        
        return header + telemetry_data + mfd_data
    
    def _generate_car_status_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate car status packet (ID: 7)"""
        header = self._generate_packet_header(7)
        
        # Simplified car status for all 22 cars
        status_data = b''
        for i in range(22):
            car_status = struct.pack(
                '<BBBBBBBBBBBBBBBBBBB',
                1,  # tractionControl
                0,  # antiLockBrakes
                random.randint(50, 100),  # fuelMix
                0,  # frontBrakeBias
                0,  # pitLimiterStatus
                random.randint(30, 50),  # fuelInTank
                100,  # fuelCapacity
                random.randint(0, 5),  # fuelRemainingLaps
                0,  # maxRPM
                0,  # idleRPM
                8,  # maxGears
                0,  # drsAllowed
                0,  # drsActivationDistance
                16,  # actualTyreCompound
                2,  # visualTyreCompound
                0,  # tyresAgeLaps
                -1,  # vehicleFiaFlags
                0,  # ersStoreEnergy
                0,  # ersDeployMode
            )
            status_data += car_status
        
        return header + status_data
    
    def _generate_motion_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate motion packet (ID: 0)"""
        header = self._generate_packet_header(0)
        
        # PacketMotionData = Header (29 bytes) + 22 CarMotionData structs
        # Expected total: 1349 bytes, so motion data = 1349 - 29 = 1320 bytes
        # That's 1320 / 22 = 60 bytes per car
        # CarMotionData: 6 floats (24 bytes) + 6 int16 (12 bytes) + 6 floats (24 bytes) = 60 bytes ✓
        
        motion_data = b''
        for car in range(22):  # 22 cars
            # 6 position/velocity floats
            car_data = struct.pack('<' + 'f' * 6, 
                random.uniform(-1000, 1000),  # worldPositionX
                random.uniform(-100, 100),     # worldPositionY
                random.uniform(-1000, 1000),  # worldPositionZ
                random.uniform(-100, 100),     # worldVelocityX
                random.uniform(-100, 100),     # worldVelocityY
                random.uniform(-100, 100))     # worldVelocityZ
            
            # 6 direction int16s
            car_data += struct.pack('<' + 'h' * 6,
                *[random.randint(-32768, 32767) for _ in range(6)])
            
            # 6 force/rotation floats
            car_data += struct.pack('<' + 'f' * 6,
                random.uniform(-5, 5),    # gForceLateral
                random.uniform(-5, 5),    # gForceLongitudinal
                random.uniform(-5, 5),    # gForceVertical
                random.uniform(-3.14, 3.14),  # yaw
                random.uniform(-1.57, 1.57),  # pitch
                random.uniform(-1.57, 1.57))  # roll
            
            motion_data += car_data
        
        return header + motion_data
    
    def _generate_participants_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate participants packet (ID: 4)"""
        header = self._generate_packet_header(4)
        
        num_cars = settings.get('num_cars', 20)
        participants_data = struct.pack('<B', num_cars)
        
        # Simplified participant data for each car
        for i in range(22):
            if i < num_cars:
                participant = struct.pack(
                    '<BB48sBBBBBBBB',
                    1 if i < num_cars else 0,  # aiControlled
                    i,  # driverId
                    f"Driver {i}".encode('utf-8').ljust(48, b'\x00'),  # name
                    0,  # networkId
                    0,  # teamId
                    0,  # myTeam
                    0,  # raceNumber
                    0,  # nationality
                    0,  # yourTelemetry
                    0,  # showOnlineNames
                    0   # platform
                )
            else:
                participant = struct.pack('<BB48sBBBBBBBB', *[0] * 58)
            
            participants_data += participant
        
        return header + participants_data
    
    def _generate_generic_packet(self, settings: Dict[str, Any]) -> bytes:
        """Generate a generic packet when specific type is not implemented"""
        header = self._generate_packet_header(255)
        # Add some dummy data
        dummy_data = bytes([0] * 100)
        return header + dummy_data
