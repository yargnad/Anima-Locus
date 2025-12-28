from enum import Enum
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field

# --- Enums ---

class MessageType(str, Enum):
    SET_PARAM = "set_param"
    SET_ELEMENT = "set_element"
    TELEMETRY = "telemetry"
    ELEMENTS = "elements"

class EngineType(str, Enum):
    GRANULAR = "granular"
    SPECTRAL = "spectral"
    SAMPLER = "sampler"
    EFFECTS = "effects"
    OSCILLATOR = "oscillator"

class ElementType(str, Enum):
    EARTH = "earth"
    AIR = "air"
    WATER = "water"
    FIRE = "fire"

# --- WebSocket Messages (Client -> Server) ---

class WSMessage(BaseModel):
    type: MessageType

class SetParamMessage(WSMessage):
    type: MessageType = MessageType.SET_PARAM
    part_id: str = Field(..., pattern="^[ABCD]$", description="Part ID (A, B, C, D)")
    engine: EngineType
    param: str
    value: float

class SetElementMessage(WSMessage):
    type: MessageType = MessageType.SET_ELEMENT
    element: ElementType
    value: float = Field(..., ge=0.0, le=1.0, description="Normalized value 0-1")

# --- WebSocket Messages (Server -> Client) ---

class ElementBusFrame(WSMessage):
    type: MessageType = MessageType.ELEMENTS
    values: Dict[ElementType, float]

class TelemetryMessage(WSMessage):
    type: MessageType = MessageType.TELEMETRY
    sensors: Dict[str, Any]
    audio: Dict[str, Any]

# --- REST Resources ---

class Preset(BaseModel):
    id: str
    name: str
    engines: Dict[str, Any]
    mappings: Dict[str, str]

class Scene(BaseModel):
    id: str
    name: str
    presets: List[str]
