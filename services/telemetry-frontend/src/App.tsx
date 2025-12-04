import { useEffect } from "react";
import SocketService from "./socket/socketService";


const WEBSOCKET_URL = "ws://localhost:8765";


function App() {

    useEffect(() => {
        const socketService = new SocketService(WEBSOCKET_URL);


        socketService.onMessage((data) => {
            console.log('Telemetry data received in App.tsx:', data);
        });

        socketService.connect();

        return () => {
            socketService.disconnect();
        };
    }, []);

  return (
    <>
      <h1>Telemetry Dashboard</h1>
    </>
  );
}

export default App;
