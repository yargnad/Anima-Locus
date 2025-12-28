import numpy as np
from .base import AudioEngine

class SpectralEngine(AudioEngine):
    def __init__(self, sample_rate=48000):
        super().__init__(sample_rate)
        self.phase = 0.0
        self.center_freq = 440.0
        self.bandwidth = 100.0
        
        # State for a simple IIR Bandpass filter
        # y[n] = b0*x[n] - a1*y[n-1] - a2*y[n-2] ...
        # Simplified Resonator
        self.v1 = 0.0
        self.v2 = 0.0
        
    def set_frequency(self, freq: float):
        self.center_freq = freq

    def set_amplitude(self, amp: float):
        self.amplitude = amp
        # Map amplitude to "Q" or bandwidth (brighter/sharper when loud)
        self.bandwidth = 50.0 + (1.0 - amp) * 500.0

    def process(self, num_frames: int) -> np.ndarray:
        # Generate White Noise
        noise = np.random.normal(0, 0.2, num_frames)
        
        # Apply Resonant Filter (State Variable or similar) around center_freq
        # To simulate "Spectral" freezing/focus
        
        # Simple Chamberlin State Variable Filter for resonance
        # f = 2 * sin(pi * freq / rate)
        # q = 1 / Q
        
        f = 2.0 * np.sin(np.pi * self.center_freq / self.sample_rate)
        q = self.bandwidth / self.center_freq # Crude approximation
        
        # Stability limit
        f = min(f, 0.9)
        
        output = np.zeros(num_frames, dtype=np.float32)
        
        # Sample-by-sample processing typically required for IIR, 
        # but numba/scipy is better. For pure numpy, we can only approximate 
        # or use very slow python loop. 
        # Let's do a trick: Overlap-Add with FFT is the *real* spectral way.
        
        # --- FFT Based Spectral Processing (Simplified) ---
        # 1. Generate Noise
        # 2. FFT
        # 3. Apply brickwall bandpass mask
        # 4. IFFT
        
        # For block size ~1024 this is fast enough in Python
        
        spectrum = np.fft.rfft(noise)
        freqs = np.fft.rfftfreq(num_frames, 1/self.sample_rate)
        
        # Create Spectral Mask
        # Gaussian centered at center_freq
        mask = np.exp(-0.5 * ((freqs - self.center_freq) / (self.bandwidth + 1.0))**2)
        
        filtered_spectrum = spectrum * mask
        filtered_audio = np.fft.irfft(filtered_spectrum, n=num_frames)
        
        return (filtered_audio * self.amplitude * 10.0).astype(np.float32) # Boost gain
