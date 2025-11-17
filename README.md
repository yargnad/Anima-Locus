# Anima Locus

**"Soul of the Place"**

A **living and breathing digital spectral/granular keyboard synthesizer** that fuses gestural control, environmental sensing, and vacuum tube analog warmth into a single expressive instrument.

**What makes it alive:**
- **Gestural interaction** via mid-air radar, E-field proximity, and depth sensing—conduct sound with your hands
- **Environmental awareness** through temperature, humidity, CO₂, and light sensors—the instrument responds to its surroundings
- **Spectral/granular synthesis** engines running on embedded Linux for deep sound design
- **Vacuum tube output stage** (Nutube 6P1) adds organic harmonic character
- **Real-time sensor fusion** on dedicated microcontroller ensures deterministic, low-latency response

This is not a traditional MIDI controller—it's an instrument that breathes with you and adapts to its environment.

---

## Project Structure (Multi-Repository)

This workspace coordinates six independent repositories:

### 1. **[hw/](./hw/)** - Hardware Design
- **License:** CERN-OHL-S v2 (Reciprocal)
- Schematics, PCBs, enclosure designs, BoMs, fabrication packages
- KiCad projects, STEP files, test fixtures

### 2. **[mcu-stm32/](./mcu-stm32/)** - Microcontroller Firmware
- **License:** AGPLv3
- STM32U585 firmware: HAL, ISR/IRQ, DMA, sensor drivers
- TinyML models (CMSIS-NN/TFLM)
- Link protocol for Linux ↔ MCU communication

### 3. **[engine-ui/](./engine-ui/)** - Audio Engine & User Interface
- **License:** AGPLv3
- **Spectral synthesis engine:** FFT-based spectral processing, freeze, morph
- **Granular synthesis engine:** Multi-grain clouds, time-stretching, pitch-shifting
- **Sampler engine:** One-shot and looping playback with envelope control
- Sensor fusion services (gesture → synthesis parameter mapping)
- WebSocket/REST API server
- Conductor HUD interface (real-time visual feedback)

### 4. **[sdk-py/](./sdk-py/)** - Python SDK
- **License:** AGPLv3
- Typed client library
- CLI tools
- Examples and Jupyter notebooks

### 5. **[sdk-ts/](./sdk-ts/)** - TypeScript SDK
- **License:** AGPLv3
- Browser and Node.js clients
- Type definitions
- Examples and demos

### 6. **[docs-site/](./docs-site/)** - Documentation
- **License:** AGPLv3 (content)
- User guides, developer docs
- API reference
- Build guides
- Contributor handbook

---

## Hardware Platform

- **Main Board:** Arduino UNO Q (Debian on application processor + STM32U585 microcontroller)
- **Display:** DSI/HDMI
- **Audio/MIDI:** Class-compliant USB
- **Optional ML:** Coral USB accelerator
- **Sensors:** I2C/UART/USB connected

### Sensor Suite

**Gestural:**
- 60-64 GHz mmWave radar (baton space tracking)
- MGC3130 E-field (near-surface gestures)
- VL53L5CX ToF depth sensor
- Beamforming mic arrays (Direction of Arrival, Voice Activity Detection)

**Environmental:**
- BME-class sensors (temperature, humidity, pressure)
- CO₂ sensor
- Thermal imaging
- Ambient light sensor (ALS)

**Analog Audio Path:**
- **Nutube 6P1 vacuum tube buffer** (real triode, analog harmonic saturation)
- Provides 2nd/3rd harmonic warmth and compression
- The "living" element—organic, non-linear response

---

## The "Living and Breathing" Philosophy

Anima‑Locus is designed to feel **alive** through:

1. **Environmental Responsiveness**
   - Temperature, humidity, air quality, and light levels subtly modulate synthesis parameters
   - Long slew rates and hysteresis prevent jarring changes—the instrument "breathes" slowly
   - Creates evolving soundscapes that change with the room's atmosphere

2. **Gestural Intimacy**
   - Hands-free control via mmWave radar (60–64 GHz) tracks baton/hand movements in 3D space
   - Near-surface E-field sensing (MGC3130) detects proximity and gesture intention
   - ToF depth imaging adds precise distance control
   - Multiple mic arrays provide spatial awareness and voice/sound triggering

3. **Organic Analog Stage**
   - Real vacuum tube (Nutube 6P1) adds harmonic complexity impossible with digital processing
   - Non-linear saturation responds dynamically to playing intensity
   - The "warmth" is not emulation—it's physics

4. **Hybrid Architecture**
   - Digital precision for spectral/granular engines (Linux on quad-core ARM)
   - Real-time determinism for sensor fusion (STM32 MCU with dedicated ISRs)
   - Analog warmth for final output (vacuum tube buffer)
   - "As analog as possible using digital parts"—the best of both worlds

---

### API-First Design
- Stable, versioned JSON over WebSocket (real-time control)
- REST API for presets/scenes
- OpenAPI specification
- Strongly typed SDKs (Python + TypeScript)

### Hybrid Compute Model
- **Linux (Application Processor):** Audio engines, UI, heavy ML
- **STM32 (Microcontroller):** Deterministic sensing, ISRs, compact tinyML
  - GPIO/INT handling
  - I2C scanning (1-10 Hz environment, 100-200 Hz IMU)
  - UART radar framing
  - CMSIS-NN/TFLM inference

### Determinism & Real-Time
- Minimal ISR execution time
- DMA for all bulk transfers
- MCU inference scheduled outside ISRs
- Compact feature frames to Linux on fixed cadences

### Observability
- Structured logging
- Metrics tagging (sensor, rate, jitter)
- Hidden `/debug` UI tab

---

## Open Licensing & Governance

### Hardware
- **CERN-OHL-S v2** (Strongly Reciprocal)
- Full fabrication sources included
- See [hw/LICENSE.cern-ohl-s](./hw/LICENSE.cern-ohl-s)

### Software
- **AGPLv3** for all userland code, MCU firmware, and SDKs
- See LICENSE files in each repository
- Third-party exceptions documented in submodules

### Defensive Publication
- Concise, citable disclosure of sensor-fusion-to-audio methods
- Establishes prior art for the community

---

## Getting Started

### Prerequisites
- **Hardware:** Arduino UNO Q board + sensors (see [docs-site/](./docs-site/) for sourcing)
- **Development:**
  - ARM cross-compiler (STM32CubeIDE or equivalent)
  - Python 3.11+
  - Node.js 20+
  - Docker (for reproducible builds)

### Quick Start
1. **Clone all repositories:**
   ```bash
   cd Anima_Locus
   git clone <hw-repo-url> hw
   git clone <mcu-repo-url> mcu-stm32
   git clone <engine-repo-url> engine-ui
   git clone <sdk-py-repo-url> sdk-py
   git clone <sdk-ts-repo-url> sdk-ts
   git clone <docs-repo-url> docs-site
   ```

2. **Follow the build guides in [docs-site/](./docs-site/)**

---

## Repository Status

| Repository | Status | Latest Release |
|------------|--------|----------------|
| hw/ | 🚧 Setup | - |
| mcu-stm32/ | 🚧 Setup | - |
| engine-ui/ | 🚧 Setup | - |
| sdk-py/ | 🚧 Setup | - |
| sdk-ts/ | 🚧 Setup | - |
| docs-site/ | 🚧 Setup | - |

---

## Contributing

Each repository has its own `CONTRIBUTING.md` with specific guidelines.

See also:
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- [SECURITY.md](./SECURITY.md)

---

## Quality Commitments

- **Deterministic control loop** on MCU (never block ISR)
- **Rate-limited, debounced** sensor reads
- **Long-slew, hysteretic** environmental parameter mapping (smooth, organic evolution)
- **Bounded impact** on pitch/brightness/envelopes (environmental changes enhance, don't dominate)
- **USB device multiplicity** (treat each USB device independently)
- **Security:** Minimal dependencies, no secrets in repo, reproducible builds, SBOM generation

---

## License Summary

- **Hardware (hw/):** [CERN-OHL-S v2](https://ohwr.org/cern_ohl_s_v2.txt)
- **Software (all others):** [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)

---

## Project Links

- **Documentation:** (Coming soon)
- **Issue Tracker:** (Coming soon)
- **Discussions:** (Coming soon)

---

*Anima Locus is part of [The Authentic Rebellion Framework](https://rebellion.musubiaccord.org) ecosystem.*
