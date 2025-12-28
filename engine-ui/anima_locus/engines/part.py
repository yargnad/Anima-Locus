import numpy as np
from typing import Optional
from .base import AudioEngine

class AudioPart:
    """Represents one of the 4 timbral parts (A, B, C, D)."""
    
    def __init__(self, part_id: str, sample_rate: int = 48000):
        self.part_id = part_id
        self.sample_rate = sample_rate
        self.engine: Optional[AudioEngine] = None
        
        # Mixer controls
        self.volume = 1.0
        self.pan = 0.0  # -1.0 (L) to 1.0 (R)
        self.mute = False
        
    def assign_engine(self, engine: AudioEngine):
        """Assigns an active engine to this part."""
        self.engine = engine
        # Ensure engine sample rate matches
        # In a real system, we might need resampling here
        if hasattr(self.engine, 'sample_rate') and self.engine.sample_rate != self.sample_rate:
             pass # TODO: Handle mismatch
             
    def process(self, num_frames: int) -> np.ndarray:
        """
        Generates audio for this part, applying volume and pan.
        Returns stereo numpy array [frames, 2].
        """
        if self.mute or self.engine is None:
            return np.zeros((num_frames, 2), dtype=np.float32)
            
        # Get raw engine output
        raw_output = self.engine.process(num_frames)
        
        # Ensure stereo
        if raw_output.ndim == 1:
            stereo_out = np.column_stack((raw_output, raw_output))
        else:
            stereo_out = raw_output
            
        # Apply Volume
        stereo_out *= self.volume
        
        # Apply Pan (Linear pan law for simplicity, constant power is better for prod)
        # Left channel gain
        left_gain = np.clip((1.0 - self.pan) * 0.5 + 0.5, 0.0, 1.0) if self.pan > 0 else 1.0
        if self.pan < 0:
             # If panning left, right channel reduces
             right_gain = np.clip((1.0 + self.pan) * 0.5 + 0.5, 0.0, 1.0) 
        else:
             right_gain = 1.0
             
        # Re-calc simple linear pan for now
        # L = (1-pan)/2 * 2 ? No, let's stick to standard linear
        # L = 1, R = 1 when pan = 0
        
        l_gain = 1.0 - max(0.0, self.pan)
        r_gain = 1.0 + min(0.0, self.pan) # wait, pan is -1 to 1.
        
        # Correct Linear Pan:
        # P = (pan + 1) / 2  (0=L, 0.5=C, 1=R)
        # L = 1.0 - P
        # R = P
        # But we want center to be 1.0, 1.0 usually? Or -3dB?
        # Let's simple: Scale gains
        
        # Let's use simple balance controls for now
        # If pan < 0 (Left): Left=1, Right=1+pan 
        # If pan > 0 (Right): Left=1-pan, Right=1
        
        if self.pan < 0:
            l_gain = 1.0
            r_gain = 1.0 + self.pan
        else:
            l_gain = 1.0 - self.pan
            r_gain = 1.0
            
        stereo_out[:, 0] *= l_gain
        stereo_out[:, 1] *= r_gain
        
        return stereo_out
