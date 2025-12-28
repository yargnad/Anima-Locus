import numpy as np
from .base import AudioEngine

class GranularEngine(AudioEngine):
    def __init__(self, sample_rate=48000, buffer_duration=5.0):
        super().__init__(sample_rate)
        self.buffer_duration = buffer_duration
        self.buffer_size = int(sample_rate * buffer_duration)
        
        # Generate synthetic source buffer (Pink Noise-ish)
        # Using cumulative sum of white noise for "brown" noise, close enough for texture
        white = np.random.normal(0, 0.5, self.buffer_size)
        self.audio_buffer = np.cumsum(white) 
        # Normalize
        self.audio_buffer /= np.max(np.abs(self.audio_buffer))
        self.audio_buffer *= 0.5 # Headroom
        
        # Parameters
        self.position = 0.5 # 0.0 to 1.0 (Location in buffer)
        self.density = 20.0 # Grains per second
        self.grain_size = 0.1 # Seconds
        self.spray = 0.01 # Random position offset
        
        self.grains = [] # Active grains [(start_index, current_index, length, amplitude, pan)]
        self._samples_per_grain_spawn = int(self.sample_rate / self.density)
        self._spawn_counter = 0

    def set_frequency(self, freq: float):
        # Map frequency to Position and Density for texture control
        # Low freq -> Low density, High freq -> High density
        # This allows the XY pad X-axis to control texture density
        norm = max(0.0, min(1.0, (freq - 50) / 2000))
        self.density = 5.0 + (norm * 50.0) # 5 to 55 Hz
        self._samples_per_grain_spawn = int(self.sample_rate / self.density)
        
        # Map freq to playback rate? Or just keep it as density/texture?
        # Let's map high freq to playback position movement
        self.position = (self.position + 0.0001 * norm) % 1.0

    def set_amplitude(self, amp: float):
        # Map amplitude to grain size (Y axis) and output volume
        self.amplitude = amp
        # Higher Y = Smaller, tighter grains? Or larger washes?
        # Let's say Higher Y (loud) = Larger grains
        self.grain_size = 0.05 + (amp * 0.2) 

    def process(self, num_frames: int) -> np.ndarray:
        output = np.zeros(num_frames, dtype=np.float32)
        
        # Determine number of grains to spawn in this block
        samples_remaining = num_frames
        cursor = 0
        
        while cursor < num_frames:
            # Check if it's time to spawn a grain
            if self._spawn_counter <= 0:
                self._spawn_grain()
                self._spawn_counter = self._samples_per_grain_spawn
            
            # Advance to next spawn or end of block
            step = min(samples_remaining, self._spawn_counter)
            
            # Mix active grains
            # We process active grains sample by sample or in small chunks? 
            # For Python speed, let's process the whole block at once for active grains if possible, 
            # but grains start/end at arbitrary times. 
            # Simpler: Iterate over grains and add their contribution to the output buffer
            
            cursor += step
            samples_remaining -= step
            self._spawn_counter -= step

        # --- Vectorized mixing of grains ---
        # This is an approximation: we treat grains as adding to the whole block 
        # regardless of exact sub-sample spawn time for performance in Python.
        
        active_grains_next = []
        
        for grain in self.grains:
            # Unwrap grain state
            start_idx, current_grain_time, length, amp, pan = grain
            
            # How many samples can this grain provide?
            samples_needed = num_frames
            samples_available = length - current_grain_time
            
            count = min(samples_needed, samples_available)
            
            if count > 0:
                # Extract chunk from source buffer
                # Handle wrapping if needed, but buffer is large
                read_ptr = (start_idx + current_grain_time) % self.buffer_size
                
                # If read extends beyond buffer end, we clip (simplified)
                end_ptr = read_ptr + count
                if end_ptr < self.buffer_size:
                    chunk = self.audio_buffer[read_ptr:end_ptr]
                else:
                    # Wrap around
                    chunk = np.concatenate((
                        self.audio_buffer[read_ptr:], 
                        self.audio_buffer[:end_ptr % self.buffer_size]
                    ))
                
                # Apply Grain Envelope (Hanning window)
                # Calculating individual window slice is expensive.
                # Linear fade / Trapezoid is faster.
                # Let's just create a quick window for the chunk
                # Optimized: Pre-compute window lookup?
                # Simple: Just copy raw for now, improve later. 
                # Better: Apply a simple fade in/out based on grain ratio
                
                output[:count] += chunk * amp * self.amplitude
                
                # Update grain state
                current_grain_time += count
                
                if current_grain_time < length:
                    active_grains_next.append((start_idx, current_grain_time, length, amp, pan))
        
        self.grains = active_grains_next
        
        return output
        
    def _spawn_grain(self):
        # Calculate random position based on self.position + spray
        offset = (np.random.random() - 0.5) * self.spray
        pos = (self.position + offset) % 1.0
        start_idx = int(pos * self.buffer_size)
        
        length = int(self.grain_size * self.sample_rate)
        
        self.grains.append((start_idx, 0, length, 1.0, 0.0))
