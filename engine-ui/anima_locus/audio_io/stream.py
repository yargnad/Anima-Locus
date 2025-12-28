import sounddevice as sd
import numpy as np
import logging
from typing import Optional
from ..engines.manager import EngineManager

logger = logging.getLogger(__name__)

class AudioStream:
    def __init__(self, engine_manager: EngineManager, sample_rate: int = 48000, block_size: int = 1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.manager = engine_manager
        self.stream = None
        
    def _callback(self, outdata, frames, time, status):
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        # Initialize mix accumulator
        final_mix = np.zeros((frames, 2), dtype=np.float32)
        
        # Process and Sum all 4 Parts
        for part_id in ["A", "B", "C", "D"]:
            part = self.manager.parts[part_id]
            try:
                part_output = part.process(frames)
                final_mix += part_output
            except Exception as e:
                logger.error(f"Error processing Part {part_id}: {e}")
                
        # --- Global FX placeholder ---
        # final_mix = global_fx.process(final_mix)
        
        # --- Master Limiter ---
        np.clip(final_mix, -0.95, 0.95, out=final_mix)
        
        outdata[:] = final_mix

    def start(self):
        if self.stream is None:
            try:
                self.stream = sd.OutputStream(
                    samplerate=self.sample_rate,
                    blocksize=self.block_size,
                    channels=2,
                    callback=self._callback,
                    dtype=np.float32
                )
                self.stream.start()
                logger.info(f"Audio stream started at {self.sample_rate}Hz")
            except Exception as e:
                logger.error(f"Failed to start audio stream: {e}")
                raise

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            logger.info("Audio stream stopped")

# Note: We no longer create a global instance here, 
# it will be created in server.py with the manager.
