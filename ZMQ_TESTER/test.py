import zmq
import json
from pprint import pprint
import os

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    os.system("clear")
    message = socket.recv_string()

    topic, json_payload = message.split(" ", 1)

    try:
        data_dict = json.loads(json_payload)
    except json.JSONDecodeError:
        print("Error decoding JSON payload")
        continue


    #print(f"Received Topic: {topic}")
    
    #player_car_index = data_dict["header"]["playerCarIndex"]
    #print(data_dict["cars"][player_car_index]["worldPositionX"])
    #print(data_dict["cars"][player_car_index]["worldPositionY"])
    #print(data_dict["cars"][player_car_index]["worldPositionZ"])
    print(len(data_dict["cars"]))
