import argparse
import copy
from zmq_client.zmq_client import ZmqClient
from websocket_server.websocket_server import WebsocketServer
import time
import json

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


def main():
    parser = argparse.ArgumentParser(description="Telemetry system main entry point.")
    parser.add_argument(
        "mode",
        choices=["datacollection", "passthrough"],
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

    ws_server = WebsocketServer()
    ws_server.start()
    
    last_payloads: dict[str, dict] = {}

    while True:
        try:
            topic, payload = zmq.captureData()

            if topic is None or payload is None:
                continue

            cleaned_payload = clean_payload(payload)

            if topic not in last_payloads or last_payloads[topic] != cleaned_payload:
                last_payloads[topic] = copy.deepcopy(cleaned_payload)
                payload["layer2Timestamp"] = int(time.time() * 1000)

                print(f"Forwarding updated packet for topic: {topic}")
                data_to_send = json.dumps({
                    "topic": topic,
                    "payload": payload,
                })

                ws_server.send(data_to_send)

                if DATA_COLLECTION_MODE:
                    # TODO: store to database
                    pass
            else:
                print(f"Skipping unchanged packet for topic: {topic}")

        except Exception as e:
            print(f"Error processing ZMQ data: {e}")
    

if __name__ == "__main__":
    main()
    print("Shutting down...")