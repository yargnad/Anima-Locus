# Contributing to Anima Locus

Thank you for your interest in contributing to **Anima Locus**! This document provides guidelines for contributing to the project.

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How to Contribute

### 1. Find or Create an Issue

- Check existing issues before creating a new one
- Use issue templates when available
- Clearly describe the problem or feature request
- Add relevant labels (bug, enhancement, documentation, etc.)

### 2. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

# Add upstream remote
git remote add upstream https://github.com/[org]/REPO_NAME.git
```

### 3. Create a Branch

Use descriptive branch names:

```bash
git checkout -b feature/add-sensor-calibration
git checkout -b fix/i2c-timeout-issue
git checkout -b docs/update-api-examples
```

### 4. Make Changes

Follow the repository-specific guidelines (see below for each repo).

### 5. Test Your Changes

- Run all tests: `make test` or `npm test` or `pytest`
- Verify no regressions
- Add new tests for new features

### 6. Commit with DCO

All commits **must** include a Developer Certificate of Origin (DCO) sign-off:

```bash
git commit -s -m "Add sensor calibration routine

This commit adds automatic calibration for the MGC3130
E-field sensor at startup.

Fixes #42"
```

The `-s` flag adds:
```
Signed-off-by: Your Name <your.email@example.com>
```

**Why DCO?** It certifies you have the right to submit your contribution under the project's license (AGPLv3/CERN-OHL-S).

### 7. Push and Create Pull Request

```bash
git push origin feature/add-sensor-calibration
```

Create a PR on GitHub with:
- Clear title and description
- Reference related issues (`Fixes #42`, `Relates to #37`)
- Screenshots/videos for UI changes
- Test results if applicable

---

## Repository-Specific Guidelines

### Hardware (`hw/`)

**License:** CERN-OHL-S v2 (strongly reciprocal)

**Requirements:**
- KiCad 8.0+ project files
- Gerber files for each PCB revision
- BOM with part numbers (Digikey/Mouser preferred)
- Assembly drawings
- Test procedures for new circuits

**Review Process:**
- Electrical review (circuit correctness, EMC considerations)
- DRC/ERC clean (no unresolved errors)
- PCB layout review (trace width, clearances, thermal)
- Documentation review (schematics readable, BOM complete)

### MCU Firmware (`mcu-stm32/`)

**License:** AGPLv3

**Code Style:**
- C11 standard
- MISRA-C compliance (where practical)
- 80-character line limit
- 4-space indentation (no tabs)

**Safety Rules:**
- ISRs must be < 10 µs execution time
- No blocking calls in ISRs (no printf, no delays)
- Use DMA for bulk transfers
- Atomic operations for shared state

**Testing:**
- Unit tests for non-ISR functions
- On-device integration tests
- CI must pass (cppcheck, clang-tidy, build)

**Commit Message Format:**
```
[mcu] Brief description (50 chars max)

Detailed explanation (wrap at 72 chars).

- Bullet points for multiple changes
- Reference issue numbers: Fixes #42

Signed-off-by: Your Name <your.email@example.com>
```

### Audio Engine + UI (`engine-ui/`)

**License:** AGPLv3

**Code Style:**
- Python 3.11+ with type hints
- Black formatter (line length 100)
- isort for import ordering
- mypy strict mode

**Testing:**
- pytest for unit tests
- API contract tests (OpenAPI validation)
- Audio pipeline tests (latency, CPU usage)

**Performance Requirements:**
- Audio latency < 10 ms
- CPU usage < 40% (on target hardware)
- No blocking I/O in audio callback

**Commit Message Format:**
```
[engine] Brief description

Detailed explanation.

Signed-off-by: Your Name <your.email@example.com>
```

### Python SDK (`sdk-py/`)

**License:** AGPLv3

**Code Style:**
- PEP 8 compliance
- Type hints for all public APIs
- Docstrings (Google style)

**Testing:**
- pytest with > 80% coverage
- mypy strict mode
- Integration tests against live API

**Versioning:**
- Semantic versioning (SemVer)
- Changelog updated for each release

### TypeScript SDK (`sdk-ts/`)

**License:** AGPLv3

**Code Style:**
- TypeScript strict mode
- ESLint (Airbnb config)
- Prettier formatting

**Testing:**
- Jest for unit tests
- > 80% coverage
- Integration tests against live API

**Browser Compatibility:**
- Modern browsers (ES2020+)
- Node.js 18+

### Documentation (`docs-site/`)

**License:** Creative Commons BY-SA 4.0 (content), AGPLv3 (code examples)

**Content Guidelines:**
- Clear, concise writing
- Use H2 for main sections, H3 for subsections
- Code blocks with language tags
- Images < 500 KB, WebP preferred
- Alt text for all images (accessibility)

**Review Process:**
- Technical accuracy
- Grammar and spelling
- Clarity and completeness
- Link validity

---

## Pull Request Review Process

### Checklist

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated (if needed)
- [ ] DCO sign-off on all commits
- [ ] No merge conflicts
- [ ] Descriptive PR title and description

### Review Criteria

1. **Correctness:** Does it work as intended?
2. **Safety:** No undefined behavior, race conditions, or security issues
3. **Performance:** No unnecessary overhead
4. **Maintainability:** Readable, well-documented, idiomatic
5. **Testing:** Adequate test coverage

### Approval

- **1 reviewer** required for documentation
- **2 reviewers** required for code changes
- **3 reviewers** required for hardware changes (electrical, layout, assembly)

---

## Reporting Bugs

Use the issue tracker with:

- Clear title describing the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, hardware, firmware version)
- Logs or error messages

**Security vulnerabilities:** See [SECURITY.md](./SECURITY.md) for responsible disclosure.

---

## Feature Requests

Use the issue tracker with:

- Clear title describing the feature
- Use case or motivation
- Proposed solution (optional)
- Alternative approaches (optional)

---

## Communication

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** Questions, ideas, general discussion
- **Pull Requests:** Code review, technical discussion

---

## License

By contributing, you agree that your contributions will be licensed under:

- **Hardware:** CERN-OHL-S v2 (hw/ repository)
- **Software:** AGPLv3 (all other repositories)
- **Documentation:** Creative Commons BY-SA 4.0 (docs content)

---

## Recognition

Contributors are recognized in:

- Repository `CONTRIBUTORS.md` file
- Release notes
- Documentation credits

---

## Questions?

Open a GitHub Discussion or contact the maintainers.

---

*Part of [The Authentic Rebellion Framework](https://rebellion.musubiaccord.org) ecosystem.*
