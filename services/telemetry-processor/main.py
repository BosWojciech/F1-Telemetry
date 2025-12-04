"""
F1 Telemetry Processor Service

Middleware service that:
1. Subscribes to telemetry data from the ingest service via ZeroMQ
2. Processes and filters data based on operational mode
3. Forwards data to frontend clients via WebSocket
4. Optionally stores data for analysis (datacollection mode)
"""

import asyncio
import argparse
import logging
import signal
import sys
from typing import Optional

from dotenv import load_dotenv
import structlog

from zmq_client.zmq_client import ZMQClient
from websocket_server.websocket_server import WebSocketServer


# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class TelemetryProcessor:
    """Main service orchestrator for telemetry processing"""
    
    def __init__(self, mode: str):
        self.mode = mode
        self.zmq_client: Optional[ZMQClient] = None
        self.websocket_server: Optional[WebSocketServer] = None
        self.running = False
        
        logger.info("telemetry_processor_initialized", mode=mode)
    
    async def start(self):
        """Start the telemetry processor service"""
        self.running = True
        
        try:
            # Initialize ZMQ client
            self.zmq_client = ZMQClient()
            
            # Initialize WebSocket server
            self.websocket_server = WebSocketServer()
            
            # Start WebSocket server
            websocket_task = asyncio.create_task(self.websocket_server.start())
            
            # Start ZMQ client with message handler
            zmq_task = asyncio.create_task(
                self.zmq_client.start(self._handle_telemetry_data)
            )
            
            logger.info("telemetry_processor_started", mode=self.mode)
            
            # Wait for both tasks
            await asyncio.gather(websocket_task, zmq_task)
            
        except Exception as e:
            logger.error("telemetry_processor_error", error=str(e), exc_info=True)
            raise
    
    async def _handle_telemetry_data(self, data: dict):
        """
        Process incoming telemetry data and forward to WebSocket clients
        
        Args:
            data: Parsed telemetry data from ZMQ
        """
        try:
            if self.mode == "passthrough":
                # Simply forward data to WebSocket clients
                await self.websocket_server.broadcast(data)
            
            elif self.mode == "datacollection":
                # TODO: Implement data deduplication and storage
                # For now, still forward to clients
                await self.websocket_server.broadcast(data)
                # await self._store_data(data)
            
        except Exception as e:
            logger.error("data_processing_error", error=str(e), exc_info=True)
    
    async def stop(self):
        """Gracefully stop the service"""
        logger.info("telemetry_processor_stopping")
        self.running = False
        
        if self.zmq_client:
            await self.zmq_client.stop()
        
        if self.websocket_server:
            await self.websocket_server.stop()
        
        logger.info("telemetry_processor_stopped")


async def main(mode: str):
    """Main entry point"""
    processor = TelemetryProcessor(mode=mode)
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    
    def signal_handler():
        logger.info("shutdown_signal_received")
        asyncio.create_task(processor.stop())
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await processor.start()
    except KeyboardInterrupt:
        logger.info("keyboard_interrupt")
    finally:
        await processor.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F1 Telemetry Processor Service")
    parser.add_argument(
        "--mode",
        choices=["passthrough", "datacollection"],
        default="passthrough",
        help="Operation mode: passthrough or datacollection"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(message)s"
    )
    
    try:
        asyncio.run(main(args.mode))
    except Exception as e:
        logger.error("fatal_error", error=str(e), exc_info=True)
        sys.exit(1)
