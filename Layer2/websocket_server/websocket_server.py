import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
import logging

class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: set[WebSocketServerProtocol] = set()
        self.server = None

    async def handler(self, websocket: WebSocketServerProtocol):
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        try:
            # Wait for the connection to close (send-only server)
            await websocket.wait_closed()
        except Exception as e:
            print(f"Error with client {websocket.remote_address}: {e}")
        finally:
            self.clients.discard(websocket)
            print(f"Client removed: {websocket.remote_address}")

    async def start(self):
        """Start the WebSocket server and keep it running"""
        print(f"Starting WebSocket server on ws://{self.host}:{self.port}")
        
        async with websockets.serve(self.handler, self.host, self.port) as server:
            self.server = server
            print(f"WebSocket server is running on ws://{self.host}:{self.port}")
            
            await asyncio.Future()

    async def send_to_all(self, message: dict):
        """Send message to all connected clients"""
        if not self.clients:
            print("No clients connected, skipping message send")
            return
        
        data = json.dumps(message)
        print(f"Sending message to {len(self.clients)} clients: {data[:100]}...")
        
        send_tasks = []
        disconnected_clients = []
        
        for client in self.clients.copy():
            if client.open:
                send_tasks.append(self.send_to_client(client, data))
            else:
                disconnected_clients.append(client)
        
        for client in disconnected_clients:
            self.clients.discard(client)
        
        if send_tasks:
            results = await asyncio.gather(*send_tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Error sending to client: {result}")

    async def send_to_client(self, client: WebSocketServerProtocol, data: str):
        """Send data to a specific client with error handling"""
        try:
            await client.send(data)
        except websockets.exceptions.ConnectionClosed:
            print(f"Client {client.remote_address} connection closed during send")
            self.clients.discard(client)
        except Exception as e:
            print(f"Error sending to client {client.remote_address}: {e}")
            self.clients.discard(client)