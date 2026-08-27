# CEH v13 — Module 10: Denial-of-Service

A comprehensive, hands-on reference library covering **Denial-of-Service (DoS)** and
**Distributed Denial-of-Service (DDoS)** attacks as taught in CEH v13 (Exam 312-50), rewritten
and expanded into original study notes with real commands, tool references, detection techniques,
and defensive configurations.

This repo is part of a growing security reference library. Companion modules:
- `CEHv13-Module06-System-Hacking`
- `CEHv13-Module08-Sniffing`
- `CEHv13-Module09-Social-Engineering`

> ⚠️ **Legal & Ethical Use Notice**
> Everything in this repository — attack mechanics, tool names, and commands — is provided
> strictly for **authorized security education, certification study (CEH/OSCP/PenTest+), and
> sanctioned load/resilience testing or red-team engagements with signed authorization**.
> Launching a DoS/DDoS attack against any system you do not own or do not have **explicit,
> documented, written permission** to test is a serious crime in virtually every jurisdiction
> (in the U.S., it falls under the Computer Fraud and Abuse Act; most countries have equivalent
> computer-misuse statutes) and carries severe penalties, since these attacks cause real financial
> and operational harm to real organizations. Any command in this repo involving traffic
> generation is meant for an isolated lab environment (e.g., your own local VMs) or an engagement
> with a signed statement of work — never a production system you don't control.

---

## 📚 Table of Contents

| # | File | Topic |
|---|------|-------|
| 01 | [`01-dos-ddos-concepts.md`](01-dos-ddos-concepts.md) | What DoS/DDoS are, impact, the DDoS attack lifecycle, primary vs. secondary victims |
| 02 | [`02-botnets-and-cybercrime-ecosystem.md`](02-botnets-and-cybercrime-ecosystem.md) | Botnets, organized cybercrime hierarchy, scanning methods, malicious-code propagation, mobile botnets |
| 03 | [`03-real-world-case-studies.md`](03-real-world-case-studies.md) | The Anonymous/HOIC scenario + the real 2023 Google Cloud HTTP/2 "Rapid Reset" attack (CVE-2023-44487) |
| 04 | [`04-volumetric-and-protocol-attacks.md`](04-volumetric-and-protocol-attacks.md) | UDP/ICMP/NTP floods, Ping of Death, Smurf, Pulse Wave, SYN flood family, fragmentation, spoofed session floods |
| 05 | [`05-application-layer-and-advanced-attacks.md`](05-application-layer-and-advanced-attacks.md) | HTTP GET/POST, Slowloris, UDP app-layer floods, multi-vector, P2P, PDoS, TCP SACK Panic, DRDoS, RDDoS extortion |
| 06 | [`06-dos-ddos-attack-tools.md`](06-dos-ddos-attack-tools.md) | ISB, UltraDDOS-v2, HOIC, LOIC, HULK, Slowloris, UFONet, and how to recognize their traffic |
| 07 | [`07-detection-techniques.md`](07-detection-techniques.md) | Activity profiling, sequential change-point detection, wavelet-based signal analysis |
| 08 | [`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) | Full defense playbook: filtering, TCP intercept (real Cisco IOS commands), honeypots, rate limiting, forensics |
| 09 | [`09-protection-tools-and-services.md`](09-protection-tools-and-services.md) | Enterprise appliances (FortiDDoS, A10, Huawei, Check Point) & cloud services (Cloudflare, Akamai, etc.) |
| 10 | [`10-dos-ddos-resilience-testing.md`](10-dos-ddos-resilience-testing.md) | **[Bonus]** Authorized load/resilience-testing methodology — scoping, tooling, and reporting |
| — | [`cheatsheets/attack-quick-reference.md`](cheatsheets/attack-quick-reference.md) | One-page lookup of every named attack technique |
| — | [`cheatsheets/tools-and-commands.md`](cheatsheets/tools-and-commands.md) | Every tool + real commands (nmap, Cisco IOS, iptables, hping3) in one place |

---

## 🎯 Learning Objectives

By the end of this module, you should be able to:

- [ ] Describe DoS/DDoS concepts, including botnets and the DDoS attack lifecycle
- [ ] Understand and recognize the major categories of DoS/DDoS attack vectors
- [ ] Explain volumetric, protocol, and application-layer attack techniques in detail
- [ ] Identify common DoS/DDoS attack tools and toolkits
- [ ] Walk through a real-world DDoS case study (Google Cloud, HTTP/2 Rapid Reset)
- [ ] Apply detection techniques and best practices to mitigate DoS/DDoS attacks
- [ ] Evaluate and select DoS/DDoS protection tools, appliances, and services

---

## 🧠 What Is a DoS/DDoS Attack? (30-Second Version)

A **Denial-of-Service (DoS)** attack floods a machine or network with illegitimate traffic or
requests until it can no longer serve legitimate users — the goal is *availability* sabotage, not
data theft. A **Distributed Denial-of-Service (DDoS)** attack is the same goal achieved at scale,
using many compromised machines (a **botnet**) spread across the Internet so the attack traffic
is too large and too distributed to block at any single point.

```
        PRIMARY VICTIM                          SECONDARY VICTIMS (the botnet)
   ┌───────────────────────┐            ┌──────────────────────────────────┐
   │ The actual target —   │◀───flood───│ Thousands of compromised "zombie" │
   │ website, server, or   │   traffic  │ machines the attacker controls    │
   │ network resource      │            │ via a Command & Control (C&C)     │
   └───────────────────────┘            └──────────────────────────────────┘
```

The use of secondary victims lets an attacker mount a large, disruptive attack while making it
very difficult to trace the attack back to themselves.

## 🌳 Taxonomy of DoS/DDoS Attack Vectors (this module's structure)

```
DoS/DDoS Attack Vectors
├── Volumetric Attacks        (exhaust bandwidth — measured in bps)
│   ├── UDP Flood · ICMP Flood · Ping of Death · Smurf
│   └── Pulse Wave · Zero-Day · NTP/other amplification
│
├── Protocol Attacks          (exhaust connection-state tables — measured in pps)
│   ├── SYN Flood · SYN-ACK Flood · ACK/PUSH ACK Flood
│   └── Fragmentation Attack · Spoofed Session Flood (SYN-ACK / ACK variants)
│
└── Application-Layer Attacks (exhaust app resources — measured in rps)
    ├── HTTP GET/POST Attack (+ recursive/random-recursive GET floods)
    ├── Slowloris · UDP Application-Layer Flood (CHARGEN, NTP, SNMP, RPC...)
    └── DDoS Extortion (RDDoS)

Cross-cutting / advanced patterns:
  Multi-Vector Attack · Peer-to-Peer Attack · Permanent DoS (PDoS/"phlashing")
  TCP SACK Panic Attack · Distributed Reflection DoS (DRDoS)
```

## 📦 Repository Structure

```
CEHv13-Module10-Denial-of-Service/
├── README.md                                        ← you are here
├── 01-dos-ddos-concepts.md
├── 02-botnets-and-cybercrime-ecosystem.md
├── 03-real-world-case-studies.md
├── 04-volumetric-and-protocol-attacks.md
├── 05-application-layer-and-advanced-attacks.md
├── 06-dos-ddos-attack-tools.md
├── 07-detection-techniques.md
├── 08-countermeasures-and-mitigation.md
├── 09-protection-tools-and-services.md
├── 10-dos-ddos-resilience-testing.md
└── cheatsheets/
    ├── attack-quick-reference.md
    └── tools-and-commands.md
```

## 🗺️ Exam Mapping (CEH 312-50, Module 10)

| Exam Objective | Covered In |
|---|---|
| Summarize DoS/DDoS concepts | `01`, `02` |
| Demonstrate different DoS/DDoS attack techniques | `04`, `05`, `06` |
| Explain DoS/DDoS attack countermeasures | `07`, `08`, `09` |
| (Bonus, not on exam) Resilience-testing methodology | `10` |

## 🔗 How to Use This Repo

1. Read `01` → `02` for the conceptual foundation (botnets, lifecycle, cybercrime economics).
2. `03` walks through a real, publicly documented case (Google's 2023 HTTP/2 Rapid Reset
   defense) — useful for understanding how attack theory maps to a real incident timeline.
3. `04`–`06` are the attack-technique deep dive — this is where most CEH exam scenario
   questions live ("attacker sends SYN packets with fake source IPs" → SYN flood, etc.).
4. `07`–`09` are the defensive core — detection techniques, the full mitigation playbook
   (including real Cisco IOS TCP-intercept commands), and a buyer's-guide-style tour of
   commercial protection tools/services.
5. `10` is supplementary — useful if you're planning an authorized load/resilience test against
   your own infrastructure.

## 📖 Module Summary

This module covers DoS/DDoS concepts and botnets (including the botnet ecosystem and organized
cybercrime hierarchy behind many attacks); the three major attack-vector categories — volumetric,
protocol, and application-layer — and roughly twenty named attack techniques within them; common
attack tools; a real DDoS case study (the September 2023 Google Cloud HTTP/2 "Rapid Reset"
attack, CVE-2023-44487); and a full countermeasure playbook covering detection techniques,
mitigation strategies, botnet defenses, forensics, and both hardware/software and cloud-based
protection products.

---

*Compiled as personal certification study notes. Original wording and structure — not a
reproduction of any vendor's copyrighted courseware. Tool names, defensive frameworks, and
publicly documented techniques/incidents are referenced for educational purposes with links to
official sources.*