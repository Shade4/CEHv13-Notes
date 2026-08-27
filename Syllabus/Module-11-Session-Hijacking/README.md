# CEH v13 - Module 11: Session Hijacking

Comprehensive, expanded study notes and technical reference built from the **EC-Council CEH v13 official Curricula, Module 11: Session Hijacking** (Exam 312-50), with substantial additional research, real command syntax, comparison tables, and defensive playbooks layered on top of the official material.

This repo is part of a running personal security reference library that also covers **Module 6(System Hacking)**, **Module 8 (Sniffing)**, **Module 9 (Social Engineering)**, **Module 10 (Denial-of-Service)**, Session hijacking sits directly downstream of sniffing (Module 8) - you generally need to see traffic before you can hijack a session - and upstream of Module 12 (Evading IDS, Firewalls, and Honeypots), which covers how attackers avoid detection while doing this kind of thing.

> ⚠️ **Ethical & legal use only.** Every technique, tool, and command in this repository is documented for **authorized security testing, CTFs, lab environments, and CEH/OSCP-style exam preparation**. Do not run any of this against systems, networks, or accounts you do not own or do not have explicit written authorization to test. Unauthorized session hijacking is a criminal offense in most jurisdictions (e.g., under the U.S. Computer Fraud and Abuse Act, UK Computer Misuse Act, and India's IT Act Section 66/66C).

---

## Learning Objectives

By the end of this module you should be able to:

1. **Summarize session hijacking concepts** - what it is, why it works, the attack process, and how it differs from spoofing.
2. **Explain application-level session hijacking** - compromising the HTTP session token itself.
3. **Explain network-level session hijacking** - compromising the underlysing TCP/UDP session.
4. **Apply session hijacking countermeasures** - detection, prevention, and secure development practices.