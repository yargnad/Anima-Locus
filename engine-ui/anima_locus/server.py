from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api.websocket import router as ws_router
from .api.rest import router as rest_router
from .state import audio_stream, engine_manager
from .engines.oscillator import OscillatorEngine
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing Audio System...")
    try:
        audio_stream.start()
    except Exception as e:
        logger.error(f"Audio start failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Audio System...")
    audio_stream.stop()

app = FastAPI(
    title="Anima Locus Engine",
    description="Audio Engine and Sensor Fusion Server",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # Default Frontend port
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)
app.include_router(rest_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "anima-locus-engine"}

@app.post("/test/part/{part_id}/frequency/{freq}")
async def set_part_frequency(part_id: str, freq: float):
    try:
        part = engine_manager.get_part(part_id)
        # Check if the part has an engine and if it's an oscillator
        if part.engine and isinstance(part.engine, OscillatorEngine):
            part.engine.set_frequency(freq)
            return {"part": part_id, "frequency": freq}
        else:
            raise HTTPException(status_code=400, detail="Part has no oscillator assigned")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/test/part/{part_id}/amplitude/{amp}")
async def set_part_amplitude(part_id: str, amp: float):
    try:
        part = engine_manager.get_part(part_id)
        if part.engine and isinstance(part.engine, OscillatorEngine):
            part.engine.set_amplitude(amp)
            return {"part": part_id, "amplitude": amp}
        else:
             raise HTTPException(status_code=400, detail="Part has no oscillator assigned")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/v1/panic")
async def panic_button():
    engine_manager.panic()
    return {"status": "panicked", "message": "All engines silenced."}

@app.get("/")
async def root():
    return {"message": "Anima Locus Engine Online", "docs": "/docs"}
