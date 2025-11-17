# Security Policy

## Reporting a Vulnerability

The Anima Locus project takes security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead:

1. **GitHub Security Advisories** (preferred):
   - Go to the relevant repository
   - Click "Security" tab
   - Click "Report a vulnerability"
   - Fill out the private advisory form

2. **Email** (alternative):
   - Send to: [security contact - TBD]
   - Subject: `[SECURITY] Anima Locus: Brief Description`
   - Include:
     - Repository affected (hw, mcu-stm32, engine-ui, sdk-py, sdk-ts, docs-site)
     - Description of the vulnerability
     - Steps to reproduce
     - Potential impact
     - Suggested fix (if available)

3. **Encrypted Email** (for highly sensitive issues):
   - PGP key: [TBD]

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 7 days
- **Status updates:** Every 7 days until resolved
- **Fix timeline:** Varies by severity (see below)

### Severity Levels

| Severity | Response Time | Examples |
|----------|---------------|----------|
| **Critical** | 24-48 hours | Remote code execution, authentication bypass |
| **High** | 7 days | Privilege escalation, data leakage |
| **Medium** | 30 days | Denial of service, information disclosure |
| **Low** | 90 days | Minor issues with limited impact |

### Disclosure Policy

We follow **coordinated disclosure**:

1. You report the vulnerability privately
2. We confirm and develop a fix
3. We release a patched version
4. We publish a security advisory (with credit to you, if desired)
5. You may publish your findings 30 days after the advisory

### Scope

**In scope:**
- All Anima Locus repositories (hw, mcu-stm32, engine-ui, sdk-py, sdk-ts, docs-site)
- Authentication/authorization issues
- Code execution vulnerabilities
- Data leakage or privacy violations
- Denial of service attacks
- Hardware security issues (e.g., EMC, power injection)

**Out of scope:**
- Social engineering attacks
- Physical attacks requiring device access
- Denial of service via rate limiting (by design)
- Issues in third-party dependencies (report to upstream)
- Self-XSS or self-inflicted vulnerabilities

### Security Best Practices

**For Hardware (`hw/`):**
- **EMC:** Design is not certified - use in non-critical environments only
- **High voltage:** Nutube stage operates at 90V - handle with care
- **Power injection:** Use regulated 5V supply only

**For MCU Firmware (`mcu-stm32/`):**
- **Buffer overflows:** Report immediately
- **ISR safety:** Race conditions or deadlocks
- **DMA misuse:** Memory corruption risks

**For Engine/API (`engine-ui/`):**
- **WebSocket authentication:** Currently none - do not expose to public networks
- **Input validation:** Malformed presets or sensor data
- **File system access:** Arbitrary file read/write

**For SDKs (`sdk-py/`, `sdk-ts/`):**
- **Input validation:** Improper handling of server responses
- **WebSocket injection:** Malicious server attacks

### Known Security Limitations

**Current version has no authentication:**
- WebSocket API is unauthenticated
- REST API is unauthenticated
- **DO NOT expose to untrusted networks**
- Use only on local/trusted networks

**Hardware is not EMC certified:**
- May emit RF interference
- May be susceptible to RF interference
- Use in controlled environments only

**Nutube high voltage:**
- 90V DC for analog stage
- Risk of electric shock if mishandled

### Future Security Enhancements

Planned for future releases:

- [ ] API authentication (JWT tokens)
- [ ] TLS/SSL for WebSocket and REST
- [ ] Rate limiting
- [ ] Input validation hardening
- [ ] Firmware signing
- [ ] Secure boot (if supported by STM32U585)

### Security Advisories

Published advisories will be listed here and in GitHub Security Advisories.

(None yet)

---

## Credit

We appreciate responsible disclosure and will credit security researchers in:

- Security advisories
- Release notes
- `SECURITY.md` (this file)

You may choose to be credited anonymously or publicly.

---

## Contact

For security issues: [TBD - security email or GitHub Security Advisories]

For general questions: Open a GitHub Discussion (do not discuss security vulnerabilities publicly)

---

*This Security Policy applies to all [Anima Locus](./README.md) repositories.*

---

## Appendix: CVSS Scoring

We use CVSS 3.1 for severity assessment:

- **Critical:** CVSS 9.0-10.0
- **High:** CVSS 7.0-8.9
- **Medium:** CVSS 4.0-6.9
- **Low:** CVSS 0.1-3.9

Use the [CVSS 3.1 Calculator](https://www.first.org/cvss/calculator/3.1) for self-assessment.

---

*Last updated: 2025-11-17*
