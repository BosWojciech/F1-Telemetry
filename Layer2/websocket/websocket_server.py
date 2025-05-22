import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol

class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: set[WebSocketServerProtocol] = set()

    async def handler(self, websocket: WebSocketServerProtocol):
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected: {websocket.remote_address}")

    async def start(self):
        await websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")

    async def send_to_all(self, message: dict):
        if not self.clients:
            return
        data = json.dumps(message)
        await asyncio.gather(
            *(client.send(data) for client in self.clients if client.open),
            return_exceptions=True
        )
