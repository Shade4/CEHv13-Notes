# 03 — IoT Attacks and Threats

> Learning Objective 1 (continued): *Explain IoT Concepts and Attacks.*

## Table of Contents

- [The 21 IoT Threat Categories](#the-21-iot-threat-categories)
- [Deep-Dive: DDoS Attacks on IoT](#deep-dive-ddos-attacks-on-iot)
- [Deep-Dive: Exploiting HVAC Systems](#deep-dive-exploiting-hvac-systems)
- [Deep-Dive: Rolling Code Attack](#deep-dive-rolling-code-attack)
- [Deep-Dive: BlueBorne Attack](#deep-dive-blueborne-attack)
- [Deep-Dive: Jamming Attack](#deep-dive-jamming-attack)
- [Deep-Dive: SDR-Based Attacks](#deep-dive-sdr-based-attacks)
- [Deep-Dive: Fault Injection Attacks](#deep-dive-fault-injection-attacks)
- [Hacking Smart Grid / Industrial Devices via Backdoor](#hacking-smart-grid--industrial-devices-via-backdoor)
- [Identifying and Accessing Local IoT Devices (DNS Rebinding)](#identifying-and-accessing-local-iot-devices-dns-rebinding)
- [Attacks by Sector](#attacks-by-sector)

---

## The 21 IoT Threat Categories

IoT devices generally have very few built-in security controls, and because they're internet-connected 24/7, attackers exploit them at scale to cause physical damage, wiretap communications, or launch disruptive attacks like DDoS. Below is the complete list of 21 named IoT attack/threat categories from the module, each with a working definition:

| # | Threat | Definition |
|---|--------|-----------|
| 01 | **DDoS Attack** | An attacker converts compromised devices into an army of bots to flood a target system/server, making it unavailable to legitimate users. |
| 02 | **Attack on HVAC Systems** | Attackers exploit HVAC (heating, ventilation, air conditioning) system vulnerabilities to steal confidential information such as user credentials, then pivot to further attacks. |
| 03 | **Rolling Code Attack** | An attacker jams and sniffs the RF signal used to unlock a vehicle/garage, capturing the rolling code to later unlock and steal the vehicle. |
| 04 | **BlueBorne Attack** | Attackers connect to nearby Bluetooth-enabled devices and exploit Bluetooth-stack vulnerabilities to compromise the device without pairing. |
| 05 | **Jamming Attack** | An attacker floods the RF channel between a sender and receiver with noise/traffic, preventing the two endpoints from communicating. |
| 06 | **Remote Access using Backdoor** | Attackers exploit an IoT device vulnerability to plant a backdoor and use it as a foothold into the organization's network. |
| 07 | **Remote Access using Telnet** | Attackers exploit an open, unauthenticated Telnet port to pull information shared between connected devices, including hardware/software details. |
| 08 | **Sybil Attack** | An attacker creates multiple forged identities to fabricate an illusion of legitimate traffic/consensus, disrupting communication between neighboring nodes. |
| 09 | **Exploit Kits** | Pre-packaged malicious scripts used to automatically exploit poorly patched vulnerabilities in an IoT device. |
| 10 | **Man-in-the-Middle (MITM) Attack** | An attacker positions between sender and receiver, intercepting and potentially hijacking the entire communication session. |
| 11 | **Replay Attack** | Attackers intercept a legitimate message and repeatedly resend it to the target device to cause a DoS condition or crash. |
| 12 | **Forged Malicious Device** | With physical access to the network, an attacker swaps a legitimate IoT device with a malicious look-alike. |
| 13 | **Side-Channel Attack** | Attackers extract encryption-key material by observing physical emissions ("side channels") — power draw, timing, EM radiation — rather than attacking the cryptography directly. |
| 14 | **Ransomware Attack** | Malware that encrypts a device or locks its screen/files, demanding payment to restore access. |
| 15 | **Client Impersonation** | An attacker masquerades as a legitimate smart-device client using a malicious device, performing unauthorized actions or accessing sensitive information on the real client's behalf. |
| 16 | **SQL Injection Attack** | Attackers exploit injection flaws in the mobile/web application controlling the IoT device to gain unauthorized data access. |
| 17 | **SDR-Based Attack** | Using a software-defined radio, an attacker examines and injects into the RF communication signals used by an IoT network. |
| 18 | **Fault Injection Attack** | An attacker deliberately introduces faulty behavior (electrical, thermal, or optical) into a device to exploit the resulting undefined state. |
| 19 | **Network Pivoting** | An attacker uses a compromised smart device as a stepping stone to reach otherwise-closed servers/network segments. |
| 20 | **DNS Rebinding Attack** | An attacker obtains access to a victim's router/LAN devices by getting a victim's browser to run malicious JavaScript that "rebinds" a DNS name to an internal IP. |
| 21 | **Firmware Update (FOTA) Attack** | An attacker intercepts and manipulates the firmware-over-the-air update process to inject malicious code into the update payload. |

---

## Deep-Dive: DDoS Attacks on IoT

IoT devices make ideal DDoS bot recruits: they're numerous, rarely monitored, frequently exposed directly to the internet, and rarely patched. The general workflow:

1. **Attacker gains remote access** to vulnerable devices at scale — usually via default credentials, exposed Telnet/SSH, or an unpatched RCE — turning them into a botnet.
2. The attacker sends phishing emails or exploits compromised devices to spread further and instructs the botnet via a **Command-and-Control (C2) server**.
3. The C2 server issues **flooding instructions** to every bot, which simultaneously send massive volumes of traffic (or malformed requests) at a chosen target.
4. The **target server** goes offline or becomes too overwhelmed to answer legitimate requests.

*(Illustrated in the module as Figure 18.8 — "DDoS attack on IoT devices".)*

---

## Deep-Dive: Exploiting HVAC Systems

Many organizations run internet-connected HVAC systems without adequate security, giving attackers a path into the corporate network.

**Attack steps:**

1. The attacker uses **Shodan** (`https://www.shodan.io`) to search for internet-exposed, vulnerable HVAC/ICS control systems.
2. Once a vulnerable system is found, the attacker checks default-credential databases and online resources for that make/model's factory login.
3. Default credentials are used to log into the HVAC system.
4. Once inside, the attacker can move laterally from the HVAC network into the broader corporate network, or directly manipulate temperature/climate controls from anywhere on the internet.

---

## Deep-Dive: Rolling Code Attack

Modern key fobs use a "rolling code" so a captured code can't simply be replayed — each unlock request uses a new, one-time code. Attackers defeat this with a **jam-and-replay** technique using SDR tools such as **HackRF One** and **RFCrack**:

1. Victim presses the remote button to unlock the car.
2. Attacker's jamming device blocks the car from receiving the signal, **while simultaneously sniffing and recording the first code**.
3. The car doesn't unlock; the victim, assuming a missed signal, presses the button again — sending a second code.
4. The attacker again jams reception but sniffs the **second code** too.
5. The attacker now releases the first (already-captured) code to the vehicle, unlocking it — while the victim's fob thinks the second (unused) code is still valid.
6. The **still-valid recorded second code** is used later by the attacker to unlock and steal the vehicle at will.

*(Illustrated in the module as Figure 18.20 — "Illustration of rolling code attack".)*

---

## Deep-Dive: BlueBorne Attack

**BlueBorne** is a collection of vulnerabilities in Bluetooth stack implementations that let an attacker take control of a device *without* pairing or even having the device set to discoverable mode. It's cross-platform — Android, iOS, Windows, and Linux devices have all had exploitable BlueBorne-class bugs.

**Attack steps (using HackRF One):**

1. The attacker discovers nearby Bluetooth-enabled devices.
2. Once a target is located, the attacker obtains its MAC address.
3. The attacker sends continuous probes to fingerprint the device's OS.
4. After identifying the OS, the attacker locates and exploits the specific Bluetooth-stack vulnerability for that platform.
5. The attacker can now perform **remote code execution** or a **man-in-the-middle** attack, gaining full control over the device.

---

## Deep-Dive: Jamming Attack

A jamming attack floods the wireless spectrum with noise at the same frequency legitimate devices use, drowning out real signals so the network's devices can no longer send/receive data — a physical-layer DoS. Attackers commonly use purpose-built RF jamming hardware or SDR gear tuned to the target frequency and simply transmit continuous noise, denying service to every device sharing that channel.

---

## Deep-Dive: SDR-Based Attacks

Software-Defined Radio (SDR) lets an attacker generate, receive, and process almost any radio waveform in software rather than needing purpose-built hardware for each protocol — making it the single most versatile tool category in the IoT attacker's kit. Three sub-types:

### Replay Attack
1. Attacker targets the specific frequency the target IoT device communicates on.
2. Attacker captures the original data being transmitted between two connected devices.
3. Once the frequency is confirmed, a tool like **URH (Universal Radio Hacker)** captures the command sequence.
4. The attacker replays the captured/segregated command sequence back into the IoT network at will.

### Cryptanalysis Attack
The attacker reverse-engineers the device's RF specifications, then uses that knowledge combined with cryptography/signal-processing techniques to decrypt captured RF messages without ever needing the original key.

### Reconnaissance Attack
Attackers passively fingerprint the make/model of a device by examining its unique RF chipset signature and comparing it against public specification/report databases, aiding target identification even before touching the device directly.

---

## Deep-Dive: Fault Injection Attacks

Also called **perturbation attacks** — the attacker deliberately induces abnormal, out-of-spec behavior in a chip or device (invasive or non-invasive) so it fails in an exploitable way:

| Technique | How it works |
|---|---|
| **Optical, Electromagnetic Fault Injection (EMFI), Body Bias Injection (BBI)** | Projects targeted light pulses or electromagnetic fields at a chip to induce bit-flips in memory/logic without physical contact. |
| **Power/Clock/Reset Glitching** | A precisely-timed glitch in the power rail, clock signal, or reset line skips or corrupts an instruction cycle — often used to bypass a bootloader's security check. |
| **Frequency/Voltage Tampering** | Attackers over/under-clock or over/under-volt the chip, changing the timing of internal operations in ways the design never accounted for. |
| **Temperature Attacks** | Operating the chip well outside its rated thermal range induces faults in otherwise-correct logic. |

Fault injection is often paired with **NAND glitching** during firmware extraction — see [05 — IoT Hacking Methodology and Tools](05-iot-hacking-methodology-and-tools.md#nand-glitching) for the exact hardware procedure.

---

## Hacking Smart Grid / Industrial Devices via Backdoor

A social-engineering-led attack chain aimed at compromising SCADA-connected industrial equipment:

1. The attacker researches employees of the target utility/organization using OSINT and social engineering.
2. A phishing email with a malicious attachment is sent to an employee.
3. The employee opens the attachment, installing a RAT (Remote Access Trojan) that gives the attacker a foothold on that workstation.
4. The attacker pivots from the workstation into the SCADA network the compromised system had access to.
5. Once inside SCADA, the attacker uploads malicious firmware to a substation control system, potentially disabling the substation entirely.

*(Illustrated in the module as Figure 18.13 — "Hacking a smart grid to gain remote access".)*

---

## Identifying and Accessing Local IoT Devices (DNS Rebinding)

**DNS rebinding** lets an attacker on the *public* internet reach devices on a victim's *private* LAN, bypassing same-origin-policy protections, by abusing the fact that DNS answers can change between lookups.

1. The victim visits a malicious website; the malicious JavaScript embedded in that page begins port-scanning the victim's own local network from inside the victim's browser.
2. If DNS rebinding tooling (e.g., **Singularity of Origin**) is used, the attacker further extracts private information and gains remote command-and-control over locally reachable IoT devices.
3. Once local devices are enumerated, the attacker can extract private information, map the geolocation of local access points, and pull SSIDs/BSSIDs of nearby wireless networks.

*(Illustrated in the module as Figures 18.14 "Discovering the local IoT devices" and 18.15 "DNS rebinding attack on local IoT devices".)*

---

## Attacks by Sector

The module maps common attack types to the industries where they show up most, along with the primary consequence of each. This is a useful table for tailoring a risk narrative to a specific client vertical:

| Sector | Representative Attacks | Typical Consequence |
|---|---|---|
| **Buildings** | Access Control abuse, MITM, DoS (resource flooding), Eavesdropping, Control-Hijacking (malicious firmware reflash) | Loss of confidentiality, data availability |
| **Energy / Industrial** | Reverse Engineering firmware, Rube Goldberg (chained) attacks, Access Control abuse, Reconnaissance, DoS, Eavesdropping, Spear Phishing, Bluejacking | Loss of privacy, confidentiality, availability |
| **Consumer & Home** | Access Control abuse, MITM, Skill-Squatting (voice-assistant command hijacking), Fernjacking (payment-terminal data theft) | Loss of privacy, data confidentiality |
| **Healthcare & Life Science** | Signal Jamming, Access Control abuse, DoS | Loss of data availability |
| **Critical Water Infrastructure** | Access Control abuse, Jamming, Fragmentation (header-guessing via XOR), DoS, Misconfiguration exploitation | Loss of privacy, confidentiality, availability |
| **Agriculture** | Path-based DoS (malicious packet injection/replay), Reprogramming attack, GPS Spoofing | Loss of privacy, data confidentiality |
| **Marine** | Signal Jamming, Access Control abuse, Communication Redirection/Eavesdropping | Loss of privacy, data confidentiality |
| **Transportation / Automotive / Public Safety** | Eavesdropping, Sinkhole attack, Sybil attack, Bluesnarfing, ZigBee End-Device (ZED) sabotage, MITM, Impersonation, GPS spoofing, DoS, Black-hole routing attack, Brute force | Loss of privacy, confidentiality, availability |
| **IT & Networks** | Access Control abuse, DoS | Loss of privacy, data availability |

*(Table 18.4 in the source courseware — condensed and paraphrased here.)*

---

**Previous:** [02 — IoT Attack Surface and Vulnerabilities](02-iot-attack-surface-and-vulnerabilities.md)
**Next:** [04 — IoT Malware and Botnets](04-iot-malware-and-botnets.md)
