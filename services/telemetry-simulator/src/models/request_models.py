from pydantic import BaseModel

class TelemetryRequest(BaseModel):
    packet_type: str
    data: dict
