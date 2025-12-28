import sounddevice as sd
import numpy as np

try:
    print("Querying devices...")
    print(sd.query_devices())
    
    fs = 44000
    duration = 1.0  # seconds
    f = 440.0
    
    print(f"Generating tone at {f}Hz...")
    t = np.arange(int(fs * duration)) / fs
    audio = 0.5 * np.sin(2 * np.pi * f * t)
    
    print("Playing...")
    sd.play(audio, fs)
    sd.wait()
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
