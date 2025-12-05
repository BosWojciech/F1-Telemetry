"""
F1 Telemetry Processor Service

Middleware service that:
1. Subscribes to telemetry data from the ingest service via ZeroMQ
2. Processes and filters data based on operational mode
3. Forwards data to frontend clients via WebSocket
4. Optionally stores data for analysis (datacollection mode)
"""

import argparse
import signal
import sys
import time
import json

from zmq_client.zmq_client import ZmqClient
from websocket_server.websocket_server import WebsocketServer


class TelemetryProcessor:
    """Main service orchestrator for telemetry processing"""
    
    def __init__(self, mode: str):
        self.mode = mode
        self.zmq_client = None
        self.websocket_server = None
        self.running = False
        
        print(f"[INFO] Telemetry Processor initialized in {mode} mode")
    
    def start(self):
        """Start the telemetry processor service"""
        self.running = True
        
        try:
            # Initialize and start WebSocket server (runs in separate thread)
            print("[INFO] Starting WebSocket server...")
            self.websocket_server = WebsocketServer(host="0.0.0.0", port=8765)
            self.websocket_server.start()
            time.sleep(1)  # Give server time to start
            
            # Initialize ZMQ client
            print("[INFO] Connecting to ZMQ publisher...")
            zmq_address = "tcp://telemetry-ingest:5555"
            self.zmq_client = ZmqClient(zmq_address, [''])
            self.zmq_client.connect()
            self.zmq_client.subscribe()
            
            print(f"[INFO] Telemetry Processor started successfully!")
            print(f"[INFO] Mode: {self.mode}")
            print(f"[INFO] Listening for telemetry data...")
            
            # Main loop - continuously receive and process data
            while self.running:
                topic, payload = self.zmq_client.captureData()
                
                if topic and payload:
                    self._handle_telemetry_data(topic, payload)
            
        except KeyboardInterrupt:
            print("\n[INFO] Received shutdown signal")
            self.stop()
        except Exception as e:
            print(f"[ERROR] Telemetry processor error: {e}")
            import traceback
            traceback.print_exc()
            self.stop()
            raise
    
    def _handle_telemetry_data(self, topic: str, payload: dict):
        """
        Process incoming telemetry data and forward to WebSocket clients
        
        Args:
            topic: ZMQ topic
            payload: Parsed telemetry data from ZMQ
        """
        try:
            if self.mode == "passthrough":
                # Simply forward data to WebSocket clients
                data_str = json.dumps(payload)
                self.websocket_server.send(data_str)
            
            elif self.mode == "datacollection":
                # TODO: Implement data deduplication and storage
                # For now, still forward to clients
                data_str = json.dumps(payload)
                self.websocket_server.send(data_str)
                # self._store_data(payload)
            
        except Exception as e:
            print(f"[ERROR] Data processing error: {e}")
    
    def stop(self):
        """Gracefully stop the service"""
        print("[INFO] Stopping Telemetry Processor...")
        self.running = False
        
        if self.zmq_client:
            self.zmq_client.stop = True
        
        print("[INFO] Telemetry Processor stopped")


def main(mode: str):
    """Main entry point"""
    processor = TelemetryProcessor(mode=mode)
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print(f"\n[INFO] Shutdown signal received: {sig}")
        processor.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        processor.start()
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        processor.stop()
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F1 Telemetry Processor Service")
    parser.add_argument(
        "--mode",
        choices=["passthrough", "datacollection"],
        default="passthrough",
        help="Operation mode: passthrough or datacollection"
    )
    
    args = parser.parse_args()
    
    try:
        main(args.mode)
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        sys.exit(1)
