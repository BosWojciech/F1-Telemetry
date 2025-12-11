from pydantic import BaseModel
from proto.enums_pb2 import PacketType

PacketType(
    
)

class TelemetryRequest(BaseModel):
    packet_type: str
    data: dict
