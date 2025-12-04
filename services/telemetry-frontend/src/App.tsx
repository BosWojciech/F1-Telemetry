import { useEffect, useState } from "react";
import SocketService from "./socket/socketService";

// Use environment variable or fallback to localhost for development
// In Docker, this should point to the processor service
const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL || "ws://localhost:8765";

interface TelemetryData {
  header?: any;
  [key: string]: any;
}

function App() {
  const [connected, setConnected] = useState(false);
  const [lastPacket, setLastPacket] = useState<TelemetryData | null>(null);
  const [packetCount, setPacketCount] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log(`Connecting to WebSocket at: ${WEBSOCKET_URL}`);
    const socketService = new SocketService(WEBSOCKET_URL);

    // Handle connection status
    const checkConnection = () => {
      setConnected(true);
      setError(null);
      console.log('✓ WebSocket connected successfully');
    };

    const handleError = (err: string) => {
      setConnected(false);
      setError(err);
      console.error('✗ WebSocket error:', err);
    };

    // Handle incoming telemetry data
    socketService.onMessage((data) => {
      console.log('Telemetry data received:', data);
      setLastPacket(data);
      setPacketCount(prev => prev + 1);
      setConnected(true);
      setError(null);
    });

    // Connect to WebSocket
    socketService.connect();

    // Simulate connection check (the actual service should expose this)
    setTimeout(checkConnection, 1000);

    return () => {
      console.log('Disconnecting from WebSocket');
      socketService.disconnect();
    };
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🏎️ F1 Telemetry Dashboard</h1>
      
      <div style={{ 
        padding: '10px', 
        marginBottom: '20px', 
        backgroundColor: connected ? '#d4edda' : '#f8d7da',
        border: `1px solid ${connected ? '#c3e6cb' : '#f5c6cb'}`,
        borderRadius: '5px'
      }}>
        <strong>WebSocket Status:</strong> {connected ? '✓ Connected' : '✗ Disconnected'}
        <br />
        <strong>URL:</strong> {WEBSOCKET_URL}
        <br />
        <strong>Packets Received:</strong> {packetCount}
        {error && (
          <>
            <br />
            <strong style={{ color: 'red' }}>Error:</strong> {error}
          </>
        )}
      </div>

      {lastPacket && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#e7f3ff',
          border: '1px solid #b3d9ff',
          borderRadius: '5px',
          maxHeight: '500px',
          overflow: 'auto'
        }}>
          <h2>Latest Packet</h2>
          <pre style={{ fontSize: '12px', whiteSpace: 'pre-wrap' }}>
            {JSON.stringify(lastPacket, null, 2)}
          </pre>
        </div>
      )}

      {!lastPacket && connected && (
        <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
          Waiting for telemetry data...
        </div>
      )}

      {!connected && !error && (
        <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
          Connecting to telemetry service...
        </div>
      )}
    </div>
  );
}

export default App;
