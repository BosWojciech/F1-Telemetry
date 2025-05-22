import argparse
import copy
from zmq.zmq_client import ZmqClient
from websocket.websocket_server import WebSocketServer
import time
import asyncio

DATA_COLLECTION_MODE = False
TOPICS = [
    "PacketMotionData",
    "PacketSessionData",
    "PacketLapData",
    "PacketEventData",
    "PacketParticipantsData",
    "PacketCarTelemetryData",
    "PacketCarStatusData",
    "PacketCarDamageData",
    "PacketSessionHistoryData",
    "PacketTyreSetsData"
]


def clean_payload(payload: dict) -> dict:
    cleaned = payload.copy()
    cleaned.pop("header", None)
    cleaned.pop("layer1Timestamp", None)
    return cleaned

async def main():
    parser = argparse.ArgumentParser(description="Telemetry system main entry point.")
    parser.add_argument(
        "mode",
        choices=["datacollection", "passthroughmode"],
        help="Mode to run the program in. Choose 'datacollection' or 'passthroughmode'."
    )

    args = parser.parse_args()
    mode = args.mode

    print(f"Running in {mode} mode...\n")
    global DATA_COLLECTION_MODE
    if mode == "datacollection":
        DATA_COLLECTION_MODE = True

    zmq = ZmqClient(address="tcp://localhost:5555", topics=TOPICS)
    zmq.connect()
    zmq.subscribe()

    ws = WebSocketServer(host="localhost", port=8765)
    await ws.start()

    last_payloads: dict[str, dict] = {}

    try:
        while True:
            topic, payload = zmq.captureData()

            if topic is None or payload is None:
                continue

            cleaned_payload = clean_payload(payload)

            if topic not in last_payloads or last_payloads[topic] != cleaned_payload:
                last_payloads[topic] = copy.deepcopy(cleaned_payload)
                payload["layer2Timestamp"] = int(time.time() * 1000)

                print(f"Forwarding updated packet for topic: {topic}")
                await ws.send_to_all({topic: payload})

                if DATA_COLLECTION_MODE:
                    # TODO: store to database
                    pass
            else:
                continue

    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())
    print("Shutting down...")
