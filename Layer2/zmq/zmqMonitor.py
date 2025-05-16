import json
import threading
import zmq


context = zmq.Context()
socket = context.socket(zmq.SUB)

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
    socket.setsockopt_string(zmq.SUBSCRIBE, topics[choice])
    print(f"Subscribed to {topics[choice]}")
print()


while True:
    msg = socket.recv_string()
    
    try:
        topic, payload = msg.split(' ', 1)
        parsed = json.loads(payload)
        print(f"\n[{topic}]\n" + json.dumps(parsed, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print(f"RAW: {msg}")


