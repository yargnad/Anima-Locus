from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import logging
from .schemas import SetParamMessage, SetElementMessage, MessageType

from ..state import engine_manager
from ..engines.oscillator import OscillatorEngine

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("Client disconnected")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Basic dispatching
            msg_type = data.get("type")
            
            if msg_type == MessageType.SET_PARAM:
                try:
                    msg = SetParamMessage(**data)
                    logger.info(f"Param Update: {msg.engine}.{msg.param} = {msg.value}")
                    
                    # Forward to Audio Engine
                    part = engine_manager.get_part(msg.part_id)
                    if part.engine:
                        # Attempt to set parameter generically via set_frequency / set_amplitude
                        # Or generic set_param if available
                        if msg.param == 'frequency':
                            if hasattr(part.engine, 'set_frequency'):
                                part.engine.set_frequency(msg.value)
                        elif msg.param == 'amplitude':
                             if hasattr(part.engine, 'set_amplitude'):
                                part.engine.set_amplitude(msg.value)
                        # TODO: Add specific params like grain_size, density, etc. map to X/Y
                    
                except Exception as e:
                    logger.error(f"Invalid param message: {e}")
                    
            elif msg_type == MessageType.SET_ELEMENT:
                try:
                    msg = SetElementMessage(**data)
                    logger.info(f"Element Update: {msg.element} = {msg.value}")
                    # TODO: Forward to Fusion Layer
                except Exception as e:
                    logger.error(f"Invalid element message: {e}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
