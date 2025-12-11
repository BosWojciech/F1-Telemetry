"""F1 Telemetry Simulator - FastAPI Backend"""

from fastapi import FastAPI

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
