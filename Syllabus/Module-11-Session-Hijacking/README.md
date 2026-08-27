# CEH v13 — Module 11: Session Hijacking

Comprehensive, expanded study notes and technical reference built from the **EC-Council CEH v13 Official Curricula, Module 11: Session Hijacking** (Exam 312-50), with substantial additional research, real command syntax, comparison tables, and defensive playbooks layered on top of the official material.

This repo is part of a running personal security reference library that also covers **Module 6 (System Hacking)**, **Module 8 (Sniffing)**, **Module 9 (Social Engineering)**, and **Module 10 (Denial-of-Service)**. Session hijacking sits directly downstream of sniffing (Module 8) — you generally need to see traffic before you can hijack a session — and upstream of Module 12 (Evading IDS, Firewalls, and Honeypots), which covers how attackers avoid detection while doing this kind of thing.

> ⚠️ **Ethical & legal use only.** Every technique, tool, and command in this repository is documented for **authorized security testing, CTFs, lab environments, and CEH/OSCP-style exam preparation**. Do not run any of this against systems, networks, or accounts you do not own or do not have explicit written authorization to test. Unauthorized session hijacking is a criminal offense in most jurisdictions (e.g., under the U.S. Computer Fraud and Abuse Act, UK Computer Misuse Act, and India's IT Act Section 66/66C).

---

## Learning Objectives

By the end of this module you should be able to:

1. **Summarize session hijacking concepts** — what it is, why it works, the attack process, and how it differs from spoofing.
2. **Explain application-level session hijacking** — compromising the HTTP session token itself.
3. **Explain network-level session hijacking** — compromising the underlying TCP/UDP session.
4. **Apply session hijacking countermeasures** — detection, prevention, and secure development practices.

## Repository Structure

| # | File | Covers |
|---|------|--------|
| 01 | [`01-session-hijacking-concepts.md`](01-session-hijacking-concepts.md) | Definition, why it succeeds, the 3-phase attack process, packet analysis of a local hijack, active vs. passive hijacking, OSI-model view, spoofing vs. hijacking |
| 02 | [`02-application-level-session-hijacking.md`](02-application-level-session-hijacking.md) | Session sniffing, token prediction, MITM/MITB, XSS, CSRF, session replay, session fixation, session donation, CRIME, Forbidden Attack, proxy-based hijacking |
| 03 | [`03-network-level-session-hijacking.md`](03-network-level-session-hijacking.md) | TCP 3-way handshake internals, TCP/IP hijacking, source-routed IP spoofing, RST hijacking, blind hijacking, UDP hijacking, ARP/ICMP-based MITM, PetitPotam |
| 04 | [`04-session-hijacking-tools.md`](04-session-hijacking-tools.md) | Hetty, Caido, bettercap, Burp Suite, OWASP ZAP, WebSploit, sslstrip, JHijack, plus classic/legacy tools (Ettercap, Hunt, T-Sight, Hamster & Ferret, Firesheep) |
| 05 | [`05-detection-methods-and-tools.md`](05-detection-methods-and-tools.md) | Manual vs. automatic detection, forced ARP entry, IDS/IPS signatures, Wireshark filters, USM Anywhere, a blue-team investigation playbook |
| 06 | [`06-countermeasures-and-best-practices.md`](06-countermeasures-and-best-practices.md) | The full countermeasure list organized by category, secure cookie flags, developer guidelines, end-user guidelines |
| 07 | [`07-ipsec-and-advanced-protections.md`](07-ipsec-and-advanced-protections.md) | HSTS, Token Binding (and its deprecation), IPsec (AH/ESP, transport/tunnel mode, architecture), DoH, WPA3, VPNs, Zero Trust, PKI, network segmentation |
| 08 | [`08-prevention-tools.md`](08-prevention-tools.md) | Checkmarx One SAST, Fiddler, Nessus, Invicti, Wapiti, OWASP ZAP baseline scanning |
| — | [`cheatsheets/commands-cheatsheet.md`](cheatsheets/commands-cheatsheet.md) | Every real, runnable command in this repo, grouped by task |
| — | [`cheatsheets/quick-reference-cheatsheet.md`](cheatsheets/quick-reference-cheatsheet.md) | One-page matrix: attack → level → tool → detection signal → countermeasure |

## Quick Concept Map

```
                         SESSION HIJACKING
                                │
                ┌───────────────┴────────────────┐
                │                                 │
        NETWORK-LEVEL                     APPLICATION-LEVEL
   (attacks the TCP/UDP session)         (attacks the HTTP session token)
                │                                 │
   ┌────┬────┬────┬────┬────┬────┐   ┌─────┬─────┬─────┬─────┬─────┬─────┐
  Blind  UDP TCP/IP RST  MITM  IP-   Sniff Predict MITM/ XSS/ Fixation/ CRIME/
  Hijack Hij Hijack Hij (ARP/ Spoof  -ing  Token   MITB  CSRF Donation/ Forbidden/
                     ICMP) (src-                          Replay    Proxy
                          routed)
```

Network-level hijacking generally requires **less effort per target** (protocol-level, works against any app) but often **more network positioning** (same LAN, or the ability to route/sniff traffic). Application-level hijacking requires **no special network position** in many cases (e.g., XSS or CSRF just need the victim to click a link) but is **specific to the target web application**.

## How to Use This Repo

- **Studying for CEH/OSCP**: read files 01 → 08 in order; each builds on the last.
- **Doing a pentest engagement**: jump straight to `cheatsheets/commands-cheatsheet.md` for copy-paste-ready syntax, then back-reference the relevant numbered file for the "why."
- **Building defenses**: start at `06-countermeasures-and-best-practices.md` and `05-detection-methods-and-tools.md`.

## Related Modules in This Library

- Module 6 — System Hacking
- Module 8 — Sniffing *(prerequisite skill for most network-level hijacking here)*
- Module 9 — Social Engineering *(delivery mechanism for fixation/donation/CSRF links)*
- Module 10 — Denial-of-Service *(RST/FIN-based desync overlaps with DoS techniques)*
- Module 12 — Evading IDS, Firewalls, and Honeypots *(next module — how attackers stay undetected while doing this)*

## Source & Attribution

Primary source: *EC-Council Certified Ethical Hacker v13, Module 11 — Session Hijacking* (Exam 312-50), 78-page official courseware. All explanations below have been substantially rewritten, reorganized, and expanded with additional context, comparison tables, real-world CVE references, current tool status research, and runnable command examples. Diagrams are original recreations (ASCII/Mermaid) for clarity, not reproductions of the source slides.

## License

Personal educational/reference use. No warranty. See [`LICENSE`](LICENSE).
