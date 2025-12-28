from .engines.manager import EngineManager
from .audio_io.stream import AudioStream
from .engines.oscillator import OscillatorEngine
from .engines.granular import GranularEngine
from .engines.spectral import SpectralEngine

# Singleton Instances
engine_manager = EngineManager()
audio_stream = AudioStream(engine_manager)

# Initialize Parts
# Part A: Granular (Texture)
eng_a = GranularEngine()
engine_manager.assign_engine_to_part("A", eng_a)

# Part B: Spectral (Pad)
eng_b = SpectralEngine()
engine_manager.assign_engine_to_part("B", eng_b)

# Part C: Oscillator (Bass)
eng_c = OscillatorEngine(frequency=110.0, amplitude=0.4)
engine_manager.assign_engine_to_part("C", eng_c)

# Part D: Oscillator (Lead)
eng_d = OscillatorEngine(frequency=660.0, amplitude=0.2)
engine_manager.assign_engine_to_part("D", eng_d)
