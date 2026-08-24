# Module 03 — Scanning Networks

Personal study notes for **CEH v13 – Module 03: Scanning Networks**, rewritten and expanded from the official courseware slide deck (`Module 3 - Scanning Networks`, pgs. 281–422) into a self-contained, repo-ready reference. Part of an ongoing CEH v13 study-notes collection.

> **Scope note:** These are original study notes — concepts, commands, and explanations rewritten in my own words for revision and lab reference. They are not a copy of the EC-Council courseware; screenshots/figures referenced from the source slides are described rather than reproduced.

---

## Why Scanning Matters

Footprinting (Module 02) tells an attacker *who* the target is. Scanning tells them *what's actually reachable*. It's the bridge between passive recon and active exploitation — the point where you go from "I know this company exists" to "I know this specific host has port 445 open running an unpatched SMB service."

Scanning is **not** the intrusion itself — it's an aggressive, active extension of reconnaissance. The output of a good scan is a working map: which hosts are alive, which ports are open on them, what services and versions sit behind those ports, what OS they're running, and where the soft spots in the perimeter (IDS/firewall) are.

## Module Learning Objectives

1. Explain network scanning concepts
2. Perform host discovery to check for live systems
3. Perform port and service discovery using various scanning techniques
4. Perform OS discovery (banner grabbing / OS fingerprinting)
5. Scan beyond intrusion detection systems (IDS) and firewalls
6. Explain network scanning countermeasures

---

## Table of Contents

| # | File | Covers |
|---|------|--------|
| 01 | [`01-network-scanning-concepts.md`](01-network-scanning-concepts.md) | What scanning is, types of scanning, TCP flags & the 3-way handshake, TCP/IP communication basics |
| 02 | [`02-scanning-tools.md`](02-scanning-tools.md) | Nmap, Hping3 (full command reference), Metasploit, NetScanTools Pro, AI-assisted scanning |
| 03 | [`03-host-discovery.md`](03-host-discovery.md) | ARP/ICMP/TCP/UDP/IP-protocol ping scans, ping sweeps, ping sweep tools |
| 04 | [`04-port-and-service-discovery.md`](04-port-and-service-discovery.md) | Full port-scanning taxonomy (TCP Connect, Stealth, Inverse-flag, ACK-probe, IDLE, UDP, SCTP, SSDP, IPv6), service/version detection, Nmap performance tuning |
| 05 | [`05-os-discovery-banner-grabbing.md`](05-os-discovery-(banner-grabbing-os-fingerprinting).md) | Active vs. passive banner grabbing, Nmap OS fingerprint tests, TTL/window-size signatures, OS discovery tooling |
| 06 | [`06-scanning-beyond-ids-firewall.md`](06-scanning-beyond-ids-and-firewall.md) | Packet fragmentation, source routing, source port manipulation, decoys, IP/MAC spoofing, custom packets, proxies & anonymizers |
| 07 | [`07-network-scanning-countermeasures.md`](07-network-scanning-countermeasures.md) | Defensive controls: ping-sweep/port-scan/banner-grab countermeasures, IP-spoofing detection & defense, detection tooling |
| — | [`cheatsheet.md`](cheatsheet.md) | One-page quick reference: every scan type + its exact Nmap/Hping3 syntax |

---

## Quick Mental Model

```
        FOOTPRINTING              SCANNING                    ENUMERATION
        (passive recon)     →    (this module)         →      (next module)
        "who/where"              "what's alive,               "what's exposed
                                   what's open,                 in detail —
                                   what OS/service"              users, shares,
                                                                  SNMP, etc."
```

Scanning itself breaks into three layers, each answering a different question:

| Layer | Question it answers | Covered in |
|---|---|---|
| **Host discovery** | Which IPs in this range are actually alive? | `03-host-discovery.md` |
| **Port & service discovery** | On a live host, which ports are open, and what's listening? | `04-port-and-service-discovery.md` |
| **OS discovery** | What operating system is the host running? | `05-os-discovery-banner-grabbing.md` |

Once you have all three, you know enough to pick an attack strategy — which is exactly why defenders spend so much effort on the countermeasures in file `07`.

## Lab Environment Referenced in Source Material

The original slides use a consistent lab topology, referenced throughout these notes:

- Attacker host: Parrot Security OS (terminal examples use `root@parrot`)
- Primary target: `10.10.1.11` (Windows machine, `WINDOWS11`)
- Secondary targets: `10.10.1.22` (Windows Server), `10.10.1.9` (Linux/Ubuntu)
- Tooling: Nmap / Zenmap (GUI front-end for Nmap), Hping3, Metasploit, Wireshark, Colasoft Packet Builder, Unicornscan

## Tools Index (all tools mentioned across this module)

| Category | Tools |
|---|---|
| Core scanners | Nmap (+ Zenmap GUI), Hping3, Unicornscan, Masscan-class tools (sx, RustScan) |
| Framework | Metasploit (`auxiliary/scanner/*` modules) |
| GUI/enterprise scanners | NetScanTools Pro, MegaPing, SolarWinds Engineer's Toolset, PRTG Network Monitor |
| Ping sweep | Angry IP Scanner, Colasoft Ping Tool, Advanced IP Scanner, OpUtils |
| Packet crafting | Colasoft Packet Builder, NetScanTools Pro |
| Packet analysis | Wireshark |
| Proxy / anonymity | Proxy Switcher, CyberGhost VPN, AstrillVPN, Tor, Whonix, Tails, I2P, Psiphon, TunnelBear |
| Detection / defense | Snort (IDS/IPS), ExtraHop, Splunk Enterprise Security, Scanlogd, Vectra Detect, IBM QRadar XDR, Cynet 360 |

---

## How to Use This Repo

Each file is self-contained and can be read independently, but the recommended order is `01 → 07` since later files assume you already know the terminology from earlier ones (e.g., `04` assumes you know the TCP flags from `01`). The `cheatsheet.md` is meant to be pinned open in a second tab during labs/CTFs.

**Ethical/legal note:** All techniques described here are for use in authorized penetration testing, CTFs, and personal lab environments only. Scanning networks you don't own or have written permission to test is illegal in most jurisdictions.
