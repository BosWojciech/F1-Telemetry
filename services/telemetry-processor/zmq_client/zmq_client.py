import zmq
import json

class ZmqClient:


    def __init__(self, address: str, topics: list[str]):
        """
        Sets all the necessary data for connection to ZeroMQ

        Args:
            address (str): address of ZeroMQ publisher
            topics (list[str]): list of topics for subscribing
        """
        self.address = address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topics = topics
        self.stop = False

    def connect(self):
        """
        Attempts connection to the publisher address
        """
        try:
            self.socket.connect(self.address)
            print(f"Socket connect succes to {self.address}")
        except Exception as e:
            print(f"Failed to connect to {self.address}")
            print(f"Error: {e}")
            return

    def subscribe(self):
        """
        Subscribes to topics from given list
        """
        for topic in self.topics:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            print(f"Subscribed to {topic}")

    def captureData(self):
        """
        Receive packets from ZeroMQ

        Returns:
            topic: topic of received data or None
            payload: json data given from ZeroMQ or None
        """

        try:
            parts = self.socket.recv_multipart()

            if len(parts) != 2:
                print(f"Unexpected multipart message: {parts}")
                return None, None
            else:
                topic = parts[0].decode("utf-8")
                payload = json.loads(parts[1].decode("utf-8"))
                print(f"Received packet: {topic}")
                return topic, payload
                
        except Exception as e:
            print(f"Error: {e}")


        
