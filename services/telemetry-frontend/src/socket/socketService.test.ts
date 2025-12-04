/**
 * Unit tests for SocketService
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import SocketService from './socketService';

// Mock WebSocket with proper constants
const WS_CONNECTING = 0;
const WS_OPEN = 1;
const WS_CLOSING = 2;
const WS_CLOSED = 3;

class MockWebSocket {
  url: string;
  readyState: number = WS_OPEN; // Start as OPEN for tests
  onopen: ((event: Event) => void) | null = null;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;
  
  // Add static constants
  static CONNECTING = WS_CONNECTING;
  static OPEN = WS_OPEN;
  static CLOSING = WS_CLOSING;
  static CLOSED = WS_CLOSED;
  
  CONNECTING = WS_CONNECTING;
  OPEN = WS_OPEN;
  CLOSING = WS_CLOSING;
  CLOSED = WS_CLOSED;

  constructor(url: string) {
    this.url = url;
    // Call onopen immediately in next tick
    setTimeout(() => {
      if (this.onopen) {
        this.onopen(new Event('open'));
      }
    }, 0);
  }

  send(_data: string) {
    // Mock send
  }

  close() {
    this.readyState = WS_CLOSED;
    if (this.onclose) {
      this.onclose(new CloseEvent('close'));
    }
  }
}

describe('SocketService', () => {
  let originalWebSocket: typeof WebSocket;

  beforeEach(() => {
    // Save original WebSocket and replace with mock
    originalWebSocket = globalThis.WebSocket;
    globalThis.WebSocket = MockWebSocket as any;
  });

  afterEach(() => {
    // Restore original WebSocket
    globalThis.WebSocket = originalWebSocket;
  });

  it('should initialize with correct URL', () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    expect(service).toBeDefined();
  });

  it('should connect to WebSocket server', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    service.connect();
    
    // Wait for async connection
    await new Promise(resolve => setTimeout(resolve, 10));
    
    expect(service.isConnected()).toBe(true);
  });

  it('should handle incoming messages', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    const messageHandler = vi.fn();
    service.onMessage(messageHandler);
    
    service.connect();
    
    // Wait for connection
    await new Promise(resolve => setTimeout(resolve, 10));
    
    // Simulate receiving a message
    const testData = { packetId: 0, sessionTime: 123.45 };
    const messageEvent = new MessageEvent('message', {
      data: JSON.stringify(testData)
    });
    
    // Access private ws property using bracket notation
    const ws = (service as any).ws;
    if (ws?.onmessage) {
      ws.onmessage(messageEvent);
    }
    
    expect(messageHandler).toHaveBeenCalledWith(testData);
  });

  it('should handle invalid JSON messages gracefully', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    const messageHandler = vi.fn();
    service.onMessage(messageHandler);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    // Simulate receiving invalid JSON
    const messageEvent = new MessageEvent('message', {
      data: 'invalid json {'
    });
    
    const ws = (service as any).ws;
    if (ws?.onmessage) {
      ws.onmessage(messageEvent);
    }
    
    // Should call handler with raw string data when JSON parsing fails
    expect(messageHandler).toHaveBeenCalledWith('invalid json {');
  });

  it('should handle connection errors', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    // Simulate error
    const ws = (service as any).ws;
    if (ws?.onerror) {
      ws.onerror(new Event('error'));
    }
    
    // Service should handle error gracefully
    expect(service.isConnected()).toBe(true); // Still shows connected until closed
  });

  it('should disconnect properly', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    expect(service.isConnected()).toBe(true);
    
    service.disconnect();
    
    expect(service.isConnected()).toBe(false);
  });

  it('should handle multiple message handlers', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    const handler1 = vi.fn();
    const handler2 = vi.fn();
    
    service.onMessage(handler1);
    service.onMessage(handler2);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    const testData = { packetId: 0 };
    const messageEvent = new MessageEvent('message', {
      data: JSON.stringify(testData)
    });
    
    const ws = (service as any).ws;
    if (ws?.onmessage) {
      ws.onmessage(messageEvent);
    }
    
    // All handlers should be called
    expect(handler1).toHaveBeenCalledWith(testData);
    expect(handler2).toHaveBeenCalledWith(testData);
  });

  it('should handle connection close', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    // Simulate close
    const ws = (service as any).ws;
    if (ws?.onclose) {
      ws.readyState = WS_CLOSED; // Update readyState before calling onclose
      ws.onclose(new CloseEvent('close'));
    }
    
    expect(service.isConnected()).toBe(false);
  });

  it('should not fail when disconnecting before connection', () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    // Should not throw error
    expect(() => service.disconnect()).not.toThrow();
  });

  it('should parse telemetry data correctly', async () => {
    const url = 'ws://localhost:8765';
    const service = new SocketService(url);
    
    const messageHandler = vi.fn();
    service.onMessage(messageHandler);
    
    service.connect();
    await new Promise(resolve => setTimeout(resolve, 10));
    
    const telemetryData = {
      header: {
        packetId: 0,
        sessionTime: 123.45,
        frameIdentifier: 100
      },
      carMotionData: [
        { worldPositionX: 100, worldPositionY: 50, worldPositionZ: 200 }
      ]
    };
    
    const messageEvent = new MessageEvent('message', {
      data: JSON.stringify(telemetryData)
    });
    
    const ws = (service as any).ws;
    if (ws?.onmessage) {
      ws.onmessage(messageEvent);
    }
    
    expect(messageHandler).toHaveBeenCalledWith(telemetryData);
    expect(messageHandler.mock.calls[0][0].header.packetId).toBe(0);
  });
});
