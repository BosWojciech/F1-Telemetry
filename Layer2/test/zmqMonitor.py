import json
import threading
import zmq_client
import time

context = zmq_client.Context()
socket = context.socket(zmq_client.SUB)

address = input("Input address of ZMQ publisher: ")
if address == "": 
    print("Address set to default: tcp://localhost:5555")
    address = "tcp://localhost:5555"
socket.connect(address)

topics = [
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

for i, topic in enumerate(topics):
    print(f"{i+1}. {topic}")

choices = input("Choose topics (separate numbers with spaces): ").split(' ')
print()

for choice in choices:
    choice = int(choice) - 1
    socket.setsockopt_string(zmq_client.SUBSCRIBE, topics[choice])
    print(f"Subscribed to {topics[choice]}")
print()


while True:
    try:
        parts = socket.recv_multipart()
        if len(parts) != 2:
            print(f"Unexpected multipart message: {parts}")
            continue

        topic = parts[0].decode("utf-8")
        payload = json.loads(parts[1].decode("utf-8"))
        latency_ms = time.time() * 1000 - payload["layer1Timestamp"]
        print(f"\n[{topic}]\n" + json.dumps(payload, indent=2))
        print(f"LATENCY: {latency_ms}")

    except Exception as e:
        print(f"Error: {e}")



