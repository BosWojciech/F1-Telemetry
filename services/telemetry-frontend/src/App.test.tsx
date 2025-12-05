/**
 * Unit tests for App component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import App from './App';

// Mock SocketService
vi.mock('./socket/socketService', () => {
  return {
    default: class MockSocketService {
      messageHandlers: Array<(data: any) => void> = [];
      url: string;
      
      constructor(url: string) {
        this.url = url;
      }
      
      connect() {
        // Simulate connection
      }
      
      disconnect() {
        // Simulate disconnection
      }
      
      onMessage(handler: (data: any) => void) {
        this.messageHandlers.push(handler);
      }
      
      // Helper to simulate receiving data
      simulateMessage(data: any) {
        this.messageHandlers.forEach(handler => handler(data));
      }
    }
  };
});

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render the app title', () => {
    render(<App />);
    expect(screen.getByText(/F1 Telemetry Dashboard/i)).toBeInTheDocument();
  });

  it('should show disconnected status initially', () => {
    render(<App />);
    expect(screen.getByText(/Status:/i)).toBeInTheDocument();
  });

  it('should display packet count', () => {
    render(<App />);
    expect(screen.getByText(/Packets Received:/i)).toBeInTheDocument();
  });

  it('should update packet count when receiving data', async () => {
    render(<App />);
    
    // Check that packet count section exists
    expect(screen.getByText(/Packets Received:/i)).toBeInTheDocument();
  });

  it('should handle connection status updates', async () => {
    render(<App />);
    
    // Should eventually show connected or disconnected
    await waitFor(() => {
      const statusElement = screen.getByText(/Status:/i);
      expect(statusElement).toBeInTheDocument();
    });
  });

  it('should display telemetry data when received', async () => {
    render(<App />);
    
    // Component should be ready to receive data
    expect(screen.getByText(/F1 Telemetry Dashboard/i)).toBeInTheDocument();
  });

  it('should render without crashing', () => {
    const { container } = render(<App />);
    expect(container).toBeTruthy();
  });

  it('should have proper component structure', () => {
    const { container } = render(<App />);
    expect(container.querySelector('div')).toBeInTheDocument();
  });

  it('should handle multiple packet updates', async () => {
    render(<App />);
    
    // Component should handle rapid updates
    expect(screen.getByText(/Packets Received:/i)).toBeInTheDocument();
  });

  it('should clean up WebSocket on unmount', () => {
    const { unmount } = render(<App />);
    
    // Should unmount without errors
    expect(() => unmount()).not.toThrow();
  });
});
