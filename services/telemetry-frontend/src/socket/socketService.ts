// socketService.ts

/**
 * @class SocketService
 * @description Handles WebSocket communication, including connecting,
 * receiving messages, and managing the connection lifecycle.
 */
class SocketService {
    private ws: WebSocket | null = null; // Stores the WebSocket instance
    private url: string;                 // The WebSocket server URL
    private messageHandler: ((data: any) => void) | null = null; // Callback for handling messages

    /**
     * @constructor
     * @param {string} url - The URL of the WebSocket server.
     */
    constructor(url: string) {
        this.url = url;
    }

    /**
     * @method connect
     * @description Establishes a connection to the WebSocket server.
     * Sets up event listeners for open, message, error, and close events.
     */
    public connect(): void {
        // Ensure only one WebSocket connection is active at a time
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            console.log('WebSocket is already connected.');
            return;
        }

        console.log(`Attempting to connect to WebSocket at: ${this.url}`);
        this.ws = new WebSocket(this.url);

        // Event listener for when the connection is successfully opened
        this.ws.onopen = () => {
            console.log('WebSocket connection established.');
        };

        // Event listener for incoming messages from the server
        this.ws.onmessage = (event: MessageEvent) => {
            console.log('Received message:', event.data);
            // If a message handler is provided, call it with the received data
            if (this.messageHandler) {
                try {
                    // Attempt to parse the data as JSON, assuming telemetry data is often JSON
                    const parsedData = JSON.parse(event.data);
                    this.messageHandler(parsedData);
                } catch (e) {
                    // If parsing fails, pass the raw string data
                    this.messageHandler(event.data);
                }
            }
        };

        // Event listener for any errors that occur with the WebSocket
        this.ws.onerror = (error: Event) => {
            console.error('WebSocket error:', error);
        };

        // Event listener for when the connection is closed
        this.ws.onclose = (event: CloseEvent) => {
            console.log('WebSocket connection closed:', event.code, event.reason);
            // Optionally, implement reconnect logic here if needed
            // For now, we just log the closure
        };
    }

    /**
     * @method disconnect
     * @description Closes the WebSocket connection if it's open.
     */
    public disconnect(): void {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.close();
            console.log('WebSocket connection closed by client.');
        } else {
            console.log('WebSocket is not connected or already closing/closed.');
        }
    }

    /**
     * @method onMessage
     * @description Sets a callback function to be executed when a message is received.
     * @param {(data: any) => void} handler - The function to call with the received data.
     */
    public onMessage(handler: (data: any) => void): void {
        this.messageHandler = handler;
    }
}

export default SocketService;
