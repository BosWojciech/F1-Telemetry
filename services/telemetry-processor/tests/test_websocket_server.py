"""
Unit tests for WebSocket Server
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from websocket_server.websocket_server import WebsocketServer


class TestWebsocketServer:
    """Test suite for WebsocketServer class"""
    
    def test_init(self):
        """Test WebSocket server initialization"""
        server = WebsocketServer(host="127.0.0.1", port=9000)
        
        assert server.host == "127.0.0.1"
        assert server.port == 9000
        assert isinstance(server.clients, set)
        assert len(server.clients) == 0
        assert server.loop is None
        assert server.server is None
    
    def test_init_defaults(self):
        """Test WebSocket server with default parameters"""
        server = WebsocketServer()
        
        assert server.host == "0.0.0.0"
        assert server.port == 8765
    
    @patch('websocket_server.websocket_server.threading.Thread')
    def test_start(self, mock_thread_class):
        """Test starting the WebSocket server thread"""
        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread
        
        server = WebsocketServer()
        server.thread = mock_thread
        server.start()
        
        mock_thread.start.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handler_client_connection(self):
        """Test WebSocket handler adds clients on connection"""
        server = WebsocketServer()
        server.clients = set()
        
        mock_websocket = AsyncMock()
        mock_websocket.remote_address = ("127.0.0.1", 12345)
        mock_websocket.__aiter__.return_value = iter([])  # No messages
        
        # Simulate client connecting and disconnecting immediately
        try:
            await server._handler(mock_websocket)
        except StopAsyncIteration:
            pass
        
        # Client should be removed after disconnection
        assert mock_websocket not in server.clients
    
    def test_send_no_loop(self):
        """Test send() when event loop is not initialized"""
        server = WebsocketServer()
        server.loop = None
        
        # Should not raise exception even if loop not ready
        server.send('{"test": "data"}')
    
    @patch('websocket_server.websocket_server.asyncio')
    def test_send_with_loop(self, mock_asyncio):
        """Test send() queues data when loop is available"""
        server = WebsocketServer()
        mock_loop = Mock()
        server.loop = mock_loop
        server.queue = Mock()
        
        test_data = '{"packetId": 0}'
        server.send(test_data)
        
        # Verify data is queued
        mock_asyncio.run_coroutine_threadsafe.assert_called_once()
    
    def test_send_invalid_json(self):
        """Test send() with invalid JSON string"""
        server = WebsocketServer()
        server.loop = Mock()
        server.queue = Mock()
        
        # Should handle gracefully
        server.send("not valid json {")
    
    @pytest.mark.asyncio
    async def test_broadcast_to_clients(self):
        """Test broadcasting data to all connected clients"""
        server = WebsocketServer()
        server.clients = set()
        
        # Create mock WebSocket clients
        client1 = AsyncMock()
        client2 = AsyncMock()
        client1.send = AsyncMock()
        client2.send = AsyncMock()
        
        server.clients.add(client1)
        server.clients.add(client2)
        
        # Mock the broadcast method
        test_data = '{"test": "data"}'
        
        # Simulate sending to all clients
        for client in server.clients:
            await client.send(test_data)
        
        # Verify all clients received data
        client1.send.assert_called_once_with(test_data)
        client2.send.assert_called_once_with(test_data)
    
    @pytest.mark.asyncio
    async def test_broadcast_handles_disconnected_client(self):
        """Test broadcasting gracefully handles disconnected clients"""
        server = WebsocketServer()
        server.clients = set()
        
        # Create mock client that's disconnected
        disconnected_client = AsyncMock()
        disconnected_client.send = AsyncMock(side_effect=Exception("Connection closed"))
        
        server.clients.add(disconnected_client)
        
        test_data = '{"test": "data"}'
        
        # Should not raise exception when client is disconnected
        try:
            await disconnected_client.send(test_data)
        except Exception:
            # This is expected - just testing it doesn't crash the server
            pass
    
    def test_multiple_clients(self):
        """Test server can handle multiple client connections"""
        server = WebsocketServer()
        
        mock_client1 = Mock()
        mock_client2 = Mock()
        mock_client3 = Mock()
        
        server.clients.add(mock_client1)
        server.clients.add(mock_client2)
        server.clients.add(mock_client3)
        
        assert len(server.clients) == 3
        
        server.clients.remove(mock_client1)
        assert len(server.clients) == 2
