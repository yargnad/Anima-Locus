# Anima Locus

**"Soul of the Place"**

A **living and breathing 4-part multitimbral spectral/granular synthesizer** that fuses gestural control, environmental sensing, and vacuum tube analog warmth into a single expressive instrument.

**What makes it alive:**

- **Gestural interaction** via mid-air radar, E-field proximity, and depth sensing—conduct sound with your hands
- **Environmental awareness** through temperature, humidity, CO₂, and light sensors—the instrument "breathes" with its surroundings
- **Multitimbral Design:** 4 Parts (A/B/C/D) with 16 total stereo voices
- **Vacuum tube output stage** (Nutube 6P1) adds organic harmonic character
- **Real-time sensor fusion** on dedicated STM32 microcontroller
- **Performer-controlled terroir**—from subtle room-breathing to wild environmental modulation

This is not a traditional MIDI controller—it's a playable keyboard synthesizer with an optional "terroir layer" that captures the sonic character of each performance space.

Who it’s for — short pitch:

- **Performing synth players** who want a site‑specific character
- **Live sound designers** who want crowd‑aware correction
- **Experimental composers** who want reproducible "aura" captures

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
- **Multitimbral Target:** 4 Parts (A/B/C/D) with 16 total stereo voices.
- **Global FX:** Shared reverb/delay bus + Analog Output Stage (Nutube).
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

- **Main Board:** Arduino UNO Q (Dual-Brain Architecture)
  - **Application Processor:** Quad-core Arm Cortex-A53 (QRB2210) @ ~2.0 GHz running Debian. Handles audio engines (16 voices), UI, and API.
  - **Microcontroller:** STM32U585 (Cortex-M33) handling real-time sensing, ISRs, and tinyML.
  - **Memory:** 2GB RAM (Application Processor) + ~786KB SRAM (MCU).
  - **Connectivity:** USB-C (Host/Device), DSI Display, I2C/SPI Sensor Buses.
  - **Practical Tip:** Use a powered USB-C hub for peripherals (Audio Interface, Cameras, Radar). Prefer built-in analog I/O only for testing; use Class-Compliant USB Audio for performance.
- **Display:** 3.5-4.3" touchscreen OLED (DSI/SPI)
- **Audio/MIDI:** Class-compliant USB
- **Optional ML:** Coral USB accelerator
- **Sensors:** I2C/UART/USB connected
- **Power:** USB-C PD (12V @ 3A)
- **Analog Stage:** Nutube 6P1 vacuum tube buffer

### Product Vision

**Standard Model (Sensor Node):**

- Arduino UNO Q-based sensor-to-OSC/MIDI bridge
- Sends hysteretic, weighted terroir data to DAW/existing synths
- Integrates with Ableton, Max/MSP, VCV Rack, etc.
- Accessible entry point (~$400-600 target)

**Pro Model (Standalone Instrument):**

- All-in-one synthesizer with onboard engines
- Built-in terroir controls and ER file recording/playback
- Hardware knobs, touchscreen UI, no computer required
- Tour-ready performance instrument (~$1500-2500 target)

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

**Implementation note (Standard vs Pro):**

- For the first Standard Model prototype, we suggest a reduced sensor set (e.g., ToF + E-field + CO₂ + ALS) to reduce BOM cost and complexity. Save mmWave radar, thermal imaging, and full mic arrays for the Pro model unless the Standard BOM and market position justify them.

**Analog Audio Path:**

- **Nutube 6P1 vacuum tube buffer** (real triode, analog harmonic saturation)
- Provides 2nd/3rd harmonic warmth and compression
- The "living" element—organic, non-linear response

**Nutube / Analog Cautions:**

- The Nutube stage requires a dedicated filament/high-voltage supply and is sensitive to RF and mechanical microphonics. Keep the Nutube physically and electrically isolated from mmWave radars and radio modules, and place mechanical damping and shielding around the tube. The Nutube should be driven by an analog preamp stage, not directly from logic-level DAC outputs.

## Terms & definitions — quick glossary

- **Terroir:** bounded environmental modulation (RH / temperature / CO₂ / pressure / ALS) with long‑slew and hysteresis characteristics that create a venue‑specific sound fingerprint. Baseline calibration sets the "quiet room" state; `Terroir Depth` mixes the delta into DSP control buses.

---

## The "Living and Breathing" Philosophy

Anima‑Locus is designed to feel **alive** through four core principles:

### 1. Environmental Responsiveness ("Sonic Terroir")

- Temperature, humidity, CO₂, and atmospheric pressure create a unique "terroir" for each performance space
- **Baseline calibration:** Capture the "quiet room" before the show, then modulate based on delta changes
- As the crowd arrives, their breath (CO₂), warmth, and humidity subtly shift the sound
- **Practical benefits:** Automatic room correction (HF boost when crowd absorbs sound, proximity effect compensation)
- **Artistic benefits:** Non-reproducible character—each venue has its own sonic fingerprint
- **Performer control:** Terroir depth from 0% (clean synth) to 100%+ (full environmental coupling)
- Long slew rates and hysteresis prevent jarring changes—the instrument "breathes" slowly with the space

### 2. Gestural Intimacy

- Hands-free control via mmWave radar (60–64 GHz) tracks baton/hand movements in 3D space
- Near-surface E-field sensing (MGC3130) detects proximity and gesture intention
- ToF depth imaging adds precise distance control
- Multiple mic arrays provide spatial awareness and voice/sound triggering
- Fast response (<10ms) for expressive, immediate control

  - Determinism note: the end-to-end gesture → parameter path should target <10ms latency with bounded jitter. To support this, keep feature frames compact and deterministic; prefer MCU preprocessing, timestamped frames, and lockless FIFOs/ring buffers or shared RAM for Linux ↔ MCU transfers.

### 3. Organic Analog Stage

- Real vacuum tube (Nutube 6P1) adds harmonic complexity impossible with digital processing
- Non-linear saturation responds dynamically to playing intensity
- The "warmth" is not emulation—it's physics
- Each tube has subtle variations—truly non-reproducible character

### 4. Hybrid Architecture

- Digital precision for spectral/granular engines (Linux on quad-core ARM)
- Real-time determinism for sensor fusion (STM32 MCU with dedicated ISRs)
- Analog warmth for final output (vacuum tube buffer)
- **"As analog as possible using digital parts"**—the best of both worlds

### Environmental Response (ER) Files

- Record the "aura" of great performances (timestamped sensor data)
  - **Privacy & retention:** ER Files are user‑triggered and opt‑in. Recordings should default to local device storage, be exportable as JSON or compressed binary archives, and include an optional consent flag if uploaded or shared.
- Replay terroir from specific shows in the studio
- Blend live + recorded terroir (60% live + 40% Brooklyn 2025-11-15)
- Capture lightning in a bottle—make album versions with the energy of your best night

### User Experience

- **OP-1/Organelle-inspired interface:** Minimal menu diving, intuitive controls with modifiers
- **Live-performance focused:** Muscle memory for critical controls (Terroir Depth knob, Baseline Set button)
- **Real-time visualization:** Radial sensor delta display shows terroir activity at a glance
- **Familiar foundation:** Works as a standard granular keyboard synth (terroir optional, not forced)

### Conductor HUD

The Conductor HUD is the single‑page live control experience for performers. It should provide:

- Beat & Dynamics (tempo lock and energy view)
- Four macros & XY pad for expressive control
- Environment strip showing normalized terroir deltas (RH, CO₂, temp, ALS)
- Beamforming DoA indicator for mic arrays (simple left / right / focus)
- Baseline Set button and Terroir Depth control for quick performance resets

Design principle: keep the HUD single‑screen and modifier‑driven to reduce onstage menu navigation.

---

### API-First Design

- Stable, versioned JSON over WebSocket (real-time control)
- REST API for presets/scenes
- OpenAPI specification
- Strongly typed SDKs (Python + TypeScript)
- OpenAPI+WS schemas: The `engine-ui/` repo will publish the contract (OpenAPI for REST and a stable JSON schema for WebSocket messages) used by `sdk-py` and `sdk-ts` for contract‑driven client implementations.
- Security note: `SECURITY.md` documents a temporary lack of auth in early prototypes — do not expose the engine WebSocket/REST APIs directly to untrusted networks. Plan for JWT/TLS integration in `engine-ui/` as soon as possible.

### Hybrid Compute Model

- **Linux (Application Processor):** Audio engines, UI, heavy ML
- **STM32 (Microcontroller):** Deterministic sensing, ISRs, compact tinyML
  - GPIO/INT handling
  - I2C scanning (1-10 Hz environment, 100-200 Hz IMU)
  - UART radar framing
  - CMSIS-NN/TFLM inference
    - Link protocol implementation: the Linux ↔ MCU link is a critical design surface. Implement compact, timestamped binary frames and a ring-buffer or shared RAM handshake to support low-latency, bounded-jitter sensor delivery.
      - Prefer SPI or UART with DMA for control/feature frames; use shared RAM + sequence numbers if the carrier exposes it for lockless transfer.
      - Consider two link classes: (1) compact feature frames (10–200 bytes) at high cadence for gestures, (2) low‑rate environmental frames (2–20 bytes) for terroir. Audio streams may be streamed as fixed blocks over shared memory or left to the Linux side depending on the algorithm.
      - Add a small benchmark suite in `mcu-stm32/` and `engine-ui/` to measure jitter, frame drops, and round-trip latency and tune buffer sizes and cadences.

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
- See `docs-site/defensive-publication.md` for the published summary and citation guidance

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
  - Mapping note: provide configurable smoothing and hysteresis kernels (exponentials, step-with-hysteresis) and record ER files for tuning; a reproducible dataset of ER recordings makes tuning simpler and safer.
  - Bounds & defaults: target long-slew windows in the 30–120 second range for global tonal drift, clamp per-parameter impact (e.g., ±2–3 cents pitch, ±1–3 dB spectral tilt), and make Terroir Depth a single hardware control whose default center is the calibrated baseline.
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
