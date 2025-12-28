import numpy as np
from .base import AudioEngine

class OscillatorEngine(AudioEngine):
    def __init__(self, sample_rate: int = 48000, frequency: float = 440.0, amplitude: float = 0.1):
        super().__init__(sample_rate)
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = 0.0
        # 2 * pi * f / fs
        self._phase_increment = 2 * np.pi * self.frequency / self.sample_rate

    def set_frequency(self, frequency: float):
        self.frequency = frequency
        self._phase_increment = 2 * np.pi * self.frequency / self.sample_rate

    def set_amplitude(self, amplitude: float):
        self.amplitude = np.clip(amplitude, 0.0, 1.0)

    def process(self, num_frames: int) -> np.ndarray:
        if self.amplitude <= 0.001:
            return np.zeros(num_frames, dtype=np.float32)

        # Create phase array for this block
        phases = self.phase + np.arange(num_frames) * self._phase_increment
        
        # Wrap phases to stay within reasonable bounds (optional but good for long running)
        # Note: simplistic wrapping here; for perfect continuity usually utilize a persistent phase accumulator
        # But this is "good enough" for a test oscillator
        
        # Generate sine wave
        audio = self.amplitude * np.sin(phases)
        
        # Update phase for next block
        self.phase = (self.phase + num_frames * self._phase_increment) % (2 * np.pi)
        
        return audio.astype(np.float32)
