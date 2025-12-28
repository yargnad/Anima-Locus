from typing import Dict
from .part import AudioPart
from .base import AudioEngine
import logging

logger = logging.getLogger(__name__)

class EngineManager:
    """Manages the 4 multitimbral parts (A, B, C, D)."""
    
    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate
        self.parts: Dict[str, AudioPart] = {
            "A": AudioPart("A", sample_rate),
            "B": AudioPart("B", sample_rate),
            "C": AudioPart("C", sample_rate),
            "D": AudioPart("D", sample_rate),
        }
        
    def get_part(self, part_id: str) -> AudioPart:
        part = self.parts.get(part_id.upper())
        if not part:
            raise ValueError(f"Invalid part ID: {part_id}")
        return part
        
    def assign_engine_to_part(self, part_id: str, engine: AudioEngine):
        part = self.get_part(part_id)
        part.assign_engine(engine)
        logger.info(f"Assigned {engine.__class__.__name__} to Part {part_id}")

    def panic(self):
        """Silences all active engines immediately."""
        logger.warning("PANIC TRIGGERED: Silencing all parts.")
        for part in self.parts.values():
            if part.engine:
                if hasattr(part.engine, 'set_amplitude'):
                    part.engine.set_amplitude(0.0)
                # Force reset amplitude in engine if property exists
                part.engine.amplitude = 0.0
