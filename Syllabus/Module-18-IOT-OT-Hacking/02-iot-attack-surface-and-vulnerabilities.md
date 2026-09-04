# 02 — IoT Attack Surface and Vulnerabilities

> Continuation of Learning Objective 1: *Explain IoT Concepts and Attacks.*

## Table of Contents

- [OWASP Top 10 IoT Threats](#owasp-top-10-iot-threats)
- [OWASP IoT Attack Surface Areas (all 18)](#owasp-iot-attack-surface-areas-all-18)
- [IoT Vulnerabilities Reference Table](#iot-vulnerabilities-reference-table)

---

## OWASP Top 10 IoT Threats

Source: [owasp.org](https://owasp.org) — OWASP Internet of Things Project

This is the standard "top of mind" checklist used when assessing *any* IoT product, from a smart plug to an industrial sensor gateway.

| # | Threat | What it means in practice |
|---|--------|---------------------------|
| **I1** | **Weak, Guessable, or Hardcoded Passwords** | Devices ship with publicly known, unchangeable, or trivially brute-forceable default credentials baked into firmware or a client app. |
| **I2** | **Insecure Network Services** | Unnecessary or exploitable services (Telnet, unauthenticated HTTP admin panels, debug shells) running on the network stack, reachable from the LAN or internet. |
| **I3** | **Insecure Ecosystem Interfaces** | Weaknesses in the web UI, backend API, cloud service, or mobile app that talk to the device — commonly missing authentication, weak encryption, or no input/output filtering. |
| **I4** | **Lack of Secure Update Mechanisms** | No signed-firmware validation, no anti-rollback protection, no encrypted transmission of updates, or no notification when an update happens. |
| **I5** | **Use of Insecure or Outdated Components** | Devices ship with unmaintained OS/SDK components, or third-party libraries that already have public CVEs, because supply chains rarely re-vet dependencies. |
| **I6** | **Insufficient Privacy Protection** | User PII stored on-device or in the cloud without adequate access control or minimization. |
| **I7** | **Insecure Data Transfer and Storage** | Sensitive data handled without encryption at rest or in transit, anywhere across the device/cloud/component chain. |
| **I8** | **Lack of Device Management** | No production fleet management: no ability to patch, no asset inventory, no ability to decommission or revoke a device's cloud credentials. |
| **I9** | **Insecure Default Settings** | Devices ship configured for convenience, not security, with no way (or no easy way) for operators to lock the configuration down. |
| **I10** | **Lack of Physical Hardening** | Physical access to the device grants disproportionate control — exposed debug headers, unsecured storage media, no tamper-detection. |

---

## OWASP IoT Attack Surface Areas (all 18)

Source: [owasp.org](https://owasp.org) — this is the master checklist a penetration tester walks through when scoping an IoT assessment. Each numbered area below maps to a distinct category of exposure; the "vulnerabilities" column lists what a tester actually looks for inside that surface.

| # | Attack Surface Area | Vulnerabilities to check for |
|---|----------------------|-------------------------------|
| **1** | **Ecosystem (General)** | Interoperability standards gaps; poor data governance; system-wide failure modes; individual stakeholder risk; implicit trust between components; weak enrollment security; no decommissioning process; no "lost access" recovery procedure. |
| **2** | **Device Memory** | Sensitive data in memory: cleartext usernames, cleartext passwords, third-party credentials, encryption keys. |
| **3** | **Device Physical Interfaces** | Firmware extraction points; exposed user/admin CLI; privilege escalation via physical access; reset-to-insecure-state; removable storage media; tamper resistance; exposed debug ports (UART/JTAG/SWD); device ID/serial number exposure. |
| **4** | **Device Web Interface** | Standard web-app weaknesses (OWASP Web Top 10, ASVS, Testing Guide apply directly); credential-management flaws — username enumeration, weak lockout policy, weak/default credentials, insecure password-recovery mechanism. |
| **5** | **Device Firmware** | Sensitive data exposure (backdoor accounts, hardcoded creds, encryption keys, sensitive URLs); no signature verification for updates or firmware version disclosure; firmware downgrade possible. |
| **6** | **Device Network Services** | Information disclosure; unauthenticated/administrative CLI over the network; injection flaws; unencrypted or poorly encrypted services; test/dev services left enabled; buffer overflow; UPnP; vulnerable UDP services; unsigned/unencrypted OTA update payloads; replay attacks; weak/no payload verification or message integrity checks; default credentials; weak password-recovery mechanism. |
| **7** | **Administrative Interface** | Same OWASP Web Top 10/ASVS/Testing Guide classes as #4; credential-management flaws mirror #4; missing security/logging options; SSH exposure; two-factor authentication absence; inability to wipe device remotely. |
| **8** | **Local Data Storage** | Unencrypted data at rest; encrypted-but-discoverable-key data; lack of data integrity checks; use of static/shared encryption/decryption keys. |
| **9** | **Cloud Web Interface** | Same OWASP Web Top 10/ASVS/Testing Guide classes; credential-management flaws (enumeration, weak passwords, lockout, default creds); transport encryption; two-factor authentication absence. |
| **10** | **Third-Party Backend APIs** | Unencrypted PII in transit; encrypted PII that still leaks metadata; device-location leakage. |
| **11** | **Update Mechanism** | Updates sent without encryption; updates not signed; update location writable/predictable; malicious update possible; missing manual/automatic update capability. |
| **12** | **Mobile Application** | Implicitly trusted by device/cloud; username enumeration; account lockout absent; known default credentials; weak passwords allowed; insecure data storage; transport encryption weaknesses; insecure password recovery; two-factor authentication absence. |
| **13** | **Vendor Backend APIs** | Inherent over-trust of the cloud or mobile app; weak authentication; weak access controls; injection flaws; hidden/undocumented services. |
| **14** | **Ecosystem Communication** | Health-check abuse; heartbeat spoofing; command-injection via ecosystem-wide commands; unnecessary deprovisioning triggers; pushing unnecessary/malicious updates. |
| **15** | **Network Traffic** | LAN traffic exposure; LAN-to-internet exposure; short-range protocol exposure; non-standard protocols in use; protocol fuzzing weaknesses; wireless (Wi-Fi/Z-Wave/Zigbee/Bluetooth/LoRa) exposure. |
| **16** | **Authentication/Authorization** | Session-token handling flaws (leak, reuse, disclosure); reuse of session/login tokens; weak device-to-device or device-to-mobile-app authentication; weak device-to-cloud or mobile-app-to-cloud authentication; web-app-to-cloud authentication weaknesses; lack of dynamic authentication. |
| **17** | **Privacy** | User data disclosed without consent; device/user location tracked and disclosed; differential-privacy failures. |
| **18** | **Hardware (Sensors)** | Sensing-environment manipulation; physical tampering; physical damage. |

*(Table 18.2 in the source courseware.)*

### Why this list matters for scoping

Notice how many of the 18 areas are **not** the device's firmware at all — Vendor Backend APIs (#13), Third-Party Backend APIs (#10), Mobile Application (#12), and Ecosystem Communication (#14) are frequently the *weakest* link in a real assessment, because vendors harden the device itself but leave the surrounding cloud/app ecosystem loosely secured. A thorough IoT pentest engagement scope should explicitly call out which of these 18 areas are in-bounds.

---

## IoT Vulnerabilities Reference Table

Source: [owasp.org](https://owasp.org)

This table lists 17 specific, named vulnerability patterns and which attack surface area(s) they typically show up in — useful as a findings checklist during reporting.

| # | Vulnerability | Attack Surface | Description |
|---|---|---|---|
| 1 | **Username Enumeration** | Admin Interface, Device Web Interface, Cloud Interface, Mobile Application | Ability to collect a set of valid usernames by interacting with the authentication mechanism. |
| 2 | **Weak Passwords** | Admin Interface, Device Web Interface, Cloud Interface, Mobile Application | Ability to set account passwords to "1234" or "123456", or use of pre-programmed/default passwords. |
| 3 | **Account Lockout** | Admin Interface, Device Web Interface, Cloud Interface, Mobile Application | Ability to continue sending authentication attempts without any lockout after 3–5 failed login attempts. |
| 4 | **Unencrypted Services** | Device Network Services | Network services not properly encrypted to prevent eavesdropping or tampering by attackers. |
| 5 | **Two-Factor Authentication** | Admin Interface, Cloud Interface, Mobile Application | Lack of two-factor authentication mechanisms such as hardware tokens or a fingerprint scan. |
| 6 | **Poorly Implemented Encryption** | Device Network Services | Encryption implemented, but incorrectly configured or not being kept properly updated (e.g., stuck on SSL/TLS 1.x). |
| 7 | **Update Sent Without Encryption** | Update Mechanism | Updates transmitted over the network without TLS, allowing tampering in transit. |
| 8 | **Update Location Writable** | Update Mechanism | Update storage location is world-writable, meaning any local process/user can modify the firmware slated for install. |
| 9 | **Denial of Service** | Device Network Services | A service can be attacked to deny service to the entire device or a specific service on it. |
| 10 | **Removal of Storage Media** | Device Physical Interfaces | Ability to physically remove the storage media from the device (e.g., pulling an SD card or SPI flash chip). |
| 11 | **No Manual Update Mechanism** | Update Mechanism | No ability to manually force a check for updates. |
| 12 | **Missing Update Mechanism** | Update Mechanism | No ability to update the device at all. |
| 13 | **Firmware Version Display and/or Last Update Date** | Device Firmware | Current firmware version and/or last update date is not displayed, complicating patch-status verification. |
| 14 | **Firmware and Storage Extraction** | Device Physical Interfaces | Firmware pulled off the device via JTAG/SWD in-situ dumping, intercepted OTA download, download from the manufacturer's website, eMMC tapping, unsoldering the SPI/NAND/eMMC flash chip, or reading it in an adapter. |
| 15 | **Manipulating the Code Execution Flow of the Device** | JTAG/SWD Interface, Side-Channel Attacks like Glitching | With the help of a JTAG adapter and a GNU debugger, the execution flow of firmware can be modified to bypass all software-based security controls. |
| 16 | **Obtaining Console Access** | Serial Interfaces (SPI/UART) | Console access (a root or debug shell) can be obtained by connecting to a serial interface — often the single most useful hardware attack primitive there is. |
| 17 | **Insecure Third-Party Components** | Software | Out-of-date versions of BusyBox, OpenSSL, SSH, web servers, etc., bundled into the firmware image, carrying their own known CVEs. |

*(Table 18.3 in the source courseware.)*

> 💡 **Practical tip:** Vulnerabilities #14–16 (Firmware extraction, manipulating code-execution flow, console access) form a natural attack chain — see [05 — IoT Hacking Methodology and Tools](05-iot-hacking-methodology-and-tools.md#maintain-access-by-exploiting-firmware) for the exact tools (JTAGulator, Attify Badge, GDB+OpenOCD, binwalk) used to exploit them.

---

**Previous:** [01 — IoT Concepts and Architecture](01-iot-concepts-and-architecture.md)
**Next:** [03 — IoT Attacks and Threats](03-iot-attacks-and-threats.md)
