# 07 — Web Server Attack Tools

> Supporting toolset referenced throughout the **Web Server Attack Methodology** objective.

Beyond the phase-specific tools already covered (footprinting, scanning, password cracking), the courseware highlights a set of **general-purpose web server attack/exploitation frameworks**.

## Immunity's CANVAS

- **Source:** https://www.immunityinc.com
- CANVAS provides penetration testers and security professionals with hundreds of exploits, an automated exploitation system, and a comprehensive, reliable exploit development framework.
- Provides features such as:
  - Client-side exploitation
  - Privilege escalation
  - HTTP-tunneled privilege escalation
  - Remote kernel exploitation
  - Advanced backdoor technology
  - Advanced web attack technology

```
                              Immunity CANVAS — typical workflow
   ┌──────────────┐    ┌──────────────────┐    ┌────────────────┐    ┌────────────────┐
   │ Select Target│───>│ Choose Exploit    │───>│ Configure &     │───>│ Execute + Get   │
   │ / Import Scan│    │ from Module List  │    │ Set Payload     │    │ Interactive Shell│
   └──────────────┘    └──────────────────┘    └────────────────┘    └────────────────┘
```

## Additional Web Server Attack Tools

| Tool | Source | Notes |
|---|---|---|
| **OpenVAS** | https://www.openvas.org | Full-featured open-source vulnerability scanner and manager; commonly used to find and validate exploitable web server vulnerabilities before weaponizing them. |
| **THC-Hydra** | https://github.com | Parallelized network login cracker (see [06](06-session-hijacking-and-password-cracking.md) for full protocol list and usage). |
| **HULK DoS** | https://github.com | HTTP Unbearable Load King — generates unique, obfuscated HTTP GET requests to bypass caching layers and overload a web server, causing a denial of service. |
| **MPack** | https://sourceforge.net | A PHP-based malicious web exploitation toolkit historically used to compromise visitors of infected websites (drive-by download style attacks) by chaining browser/plugin exploits. |

```bash
# Example: HULK-style basic DoS test (a minimal Python re-implementation concept — for AUTHORIZED lab testing only)
# Real HULK is run as: python hulk.py <target-URL>
python hulk.py http://10.10.1.19/
```

> ⚠️ **Authorized testing only.** DoS/DDoS tooling (HULK, and similar load-generation tools) must **never** be run against a system without explicit written authorization — even a brief test can cause outages, financial loss, and legal liability. See **Module 10: Denial-of-Service** for the full attack/defense picture, and [08 — Countermeasures & Hardening](08-countermeasures-and-hardening.md) for defensive controls.

---

**Previous:** [← 06 — Session Hijacking & Password Cracking](06-session-hijacking-and-password-cracking.md) · **Next:** [08 — Countermeasures & Hardening →](08-countermeasures-and-hardening.md)
