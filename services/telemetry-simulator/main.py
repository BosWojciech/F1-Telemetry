from fastapi import FastAPI
from src.models.request_models import TelemetryRequest

app = FastAPI(
    title="F1 Telemetry Simulator",
    description="FastAPI backend for F1 telemetry packet simulation",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint - Hello World"""
    return {
        "message": "Hello World from F1 Telemetry Simulator!",
        "service": "telemetry-simulator",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/send-packet")
async def send_packet(request: TelemetryRequest):
    """Endpoint to send a telemetry packet"""
    print(f"Received packet of type: {request.packet_type} with data: {request.data}")
    return {"status": "packet sent"}
