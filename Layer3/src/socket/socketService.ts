import { dispatchPacket } from "../redux/packetDispatcher";

class SocketService {
  private socket: WebSocket | null = null;

  connect(url: string) {
    if (this.socket) return;

    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log("Websocket Connected");
    };

    this.socket.onmessage = (event: MessageEvent) => {
      const packet = JSON.parse(event.data);
      dispatchPacket(packet);
    };

    this.socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  disconnect() {
    this.socket?.close();
    this.socket = null;
  }
}
