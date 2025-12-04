import asyncio
import threading
import websockets

class WebsocketServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.loop = None
        self.server = None
        self.queue = asyncio.Queue()
        self.thread = threading.Thread(target=self._start_loop, daemon=True)

    def start(self):
        self.thread.start()

    def _start_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        async def start_server():
            print(f"Starting server on {self.host}:{self.port} with handler: {self._handler}")

            server = await websockets.serve(self._handler, self.host, self.port)
            print(f"WebSocket Server started at ws://{self.host}:{self.port}")

            self.loop.create_task(self._broadcast_from_queue())

            return server

        self.server = self.loop.run_until_complete(start_server())

        self.loop.run_forever()


    async def _handler(self, websocket):

        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        try:
            async for _ in websocket:
                pass
        except websockets.ConnectionClosed:
            print(f"Client disconnected: {websocket.remote_address}")
        finally:
            self.clients.remove(websocket)

    async def _broadcast_from_queue(self):
        while True:
            data = await self.queue.get()
            if self.clients:
                await asyncio.gather(*(client.send(data) for client in self.clients))


    def send(self, data):
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.queue.put(data), self.loop)
        else:
            print("Event loop not running, can't send data")

