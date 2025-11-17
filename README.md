# Anima Locus

**"Soul of the Place"**

An open, sensor-driven musical instrument that fuses mid-air conductor gestures and environmental sensing into a digital instrument with an analog post stage.

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
- Linux audio engines (granular/spectral/sampler)
- Sensor fusion services
- WebSocket/REST API server
- Conductor HUD interface

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

**Audio Post:**
- Optional Nutube stage for harmonic sheen

---

## Architecture Principles

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
- **Long-slew, hysteretic** environmental mapping
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
