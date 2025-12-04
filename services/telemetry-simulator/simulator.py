"""
F1 Telemetry Simulator

Simulates F1 game UDP telemetry packets for testing without the actual game.
Configurable packet generation based on config.json.
"""

import socket
import time
import json
import logging
import argparse
import signal
import sys
from pathlib import Path
from typing import Dict, Any

from packet_generator import PacketGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelemetrySimulator:
    """Main simulator class for generating and sending telemetry packets"""
    
    def __init__(self, config_path: str):
        """
        Initialize the telemetry simulator
        
        Args:
            config_path: Path to the configuration JSON file
        """
        self.running = False
        self.config = self._load_config(config_path)
        self.packet_generator = PacketGenerator(self.config)
        
        # UDP socket configuration
        self.target_host = self.config.get('target_host', 'telemetry-ingest')
        self.target_port = self.config.get('target_port', 20777)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        logger.info(f"Telemetry Simulator initialized")
        logger.info(f"Target: {self.target_host}:{self.target_port}")
        logger.info(f"Simulation mode: {self.config.get('mode', 'race')}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def start(self):
        """Start the telemetry simulation"""
        self.running = True
        logger.info("Starting telemetry simulation...")
        
        packet_counts = {}
        total_packets = 0
        
        try:
            while self.running:
                # Get next packet from generator
                packet_data = self.packet_generator.generate_next_packet()
                
                if packet_data:
                    packet_type = packet_data['type']
                    data = packet_data['data']
                    
                    # Send UDP packet
                    try:
                        self.sock.sendto(data, (self.target_host, self.target_port))
                        
                        # Track packet counts
                        packet_counts[packet_type] = packet_counts.get(packet_type, 0) + 1
                        total_packets += 1
                        
                        if total_packets % 100 == 0:
                            logger.info(f"Sent {total_packets} packets. Distribution: {packet_counts}")
                    
                    except socket.error as e:
                        logger.error(f"Failed to send packet: {e}")
                
                # Control simulation speed
                time.sleep(packet_data.get('delay', 0.016))  # Default ~60Hz
        
        except KeyboardInterrupt:
            logger.info("Simulation interrupted by user")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the simulation and cleanup"""
        logger.info("Stopping telemetry simulation...")
        self.running = False
        self.sock.close()
        logger.info("Simulation stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="F1 Telemetry Simulator")
    parser.add_argument(
        "--config",
        default="config/race_simulation.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--target-host",
        default=None,
        help="Override target host (default: from config)"
    )
    parser.add_argument(
        "--target-port",
        type=int,
        default=None,
        help="Override target port (default: from config)"
    )
    
    args = parser.parse_args()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start simulator
    simulator = TelemetrySimulator(args.config)
    
    # Override config if specified
    if args.target_host:
        simulator.target_host = args.target_host
    if args.target_port:
        simulator.target_port = args.target_port
    
    logger.info("=" * 60)
    logger.info("F1 Telemetry Simulator")
    logger.info("=" * 60)
    logger.info(f"Config: {args.config}")
    logger.info(f"Target: {simulator.target_host}:{simulator.target_port}")
    logger.info("=" * 60)
    
    simulator.start()


if __name__ == "__main__":
    main()
