from abc import ABC, abstractmethod
import numpy as np

class AudioEngine(ABC):
    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    @abstractmethod
    def process(self, num_frames: int) -> np.ndarray:
        """
        Generate audio samples.
        
        Args:
            num_frames: Number of frames to generate.
            
        Returns:
            numpy.ndarray: Audio data. Can be 1D (mono) or 2D (stereo, shape=[frames, channels]).
        """
        pass
