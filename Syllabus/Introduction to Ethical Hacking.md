# Module 1: Introduction to Ethical Hacking
## Part A — Information Security Fundamentals

> Reference notes compiled for personal cybersecurity study.

---

## Table of Contents

1. [Overview](#overview)
2. [Elements of Information Security](#elements-of-information-security)
3. [Information Security Attacks: Motives, Goals, and Objectives](#information-security-attacks-motives-goals-and-objectives)
4. [Tactics, Techniques, and Procedures (TTPs)](#tactics-techniques-and-procedures-ttps)
5. [Vulnerabilities](#vulnerabilities)
6. [Classification of Attacks](#classification-of-attacks)
7. [Information Warfare](#information-warfare)
8. [Quick-Reference Summary](#quick-reference-summary)

---

## Overview

Security professionals can't defend a system they don't understand — and that includes understanding the people trying to break into it. Sun Tzu's line from *The Art of War* applies directly here: knowing your own defenses without knowing the attacker's mindset still leaves you exposed. This is the core justification for ethical hacking as a discipline — defenders study offensive techniques so they can anticipate and close the gaps attackers would otherwise exploit.

This first part of Module 1 lays the conceptual groundwork: what information security actually protects, why attacks happen, how vulnerabilities arise, how attacks are categorized, and how information itself becomes a weapon at a geopolitical scale (information warfare).

---

## Elements of Information Security

Information security is best defined as the condition in which the risk of theft, tampering, or disruption to information and information systems is minimized to an acceptable level. That condition rests on five pillars:

### 1. Confidentiality
Only authorized parties should be able to access given information. Breaches typically trace back to either mishandling of data or a deliberate intrusion. Common safeguards:
- Data classification schemes
- Encryption at rest and in transit
- Secure disposal of decommissioned hardware/media

### 2. Integrity
Data must remain trustworthy — accurate, complete, and free of unauthorized modification. Controls that support integrity include:
- Checksums / hash verification (confirming a data block hasn't changed)
- Access control (restricting who can create, modify, or delete data)

### 3. Availability
Authorized users need reliable access to systems and data when they need it. Availability is protected through:
- Redundant infrastructure (RAID arrays, clustered servers)
- Antivirus/anti-malware tooling
- DDoS mitigation systems

### 4. Authenticity
Authenticity confirms that data, communications, or users are genuine and not forged or impersonated. Supporting controls:
- Biometric authentication
- Smart cards
- Digital certificates

### 5. Non-Repudiation
Non-repudiation prevents a sender from denying they sent a message, and a receiver from denying they received it. This is typically enforced through **digital signatures**.

---

## Information Security Attacks: Motives, Goals, and Objectives

An **attack** is any deliberate attempt to compromise a system's security by exploiting a weakness — whether the goal is to steal, alter, destroy, plant, or expose data without authorization. It can be expressed as a formula:

```
Attack = Motive (Goal) + Method (TTP) + Vulnerability
```

An attacker perceives value in a target (data, access, disruption potential), which creates the motive. They then pair that motive with a method and a vulnerability to exploit.

### Common Attacker Motives
- Disrupting business continuity
- Stealing information
- Manipulating or corrupting data
- Sowing fear/chaos via attacks on critical infrastructure
- Causing financial damage
- Advancing religious or political agendas
- Achieving military/state objectives
- Damaging a target's reputation
- Revenge
- Extortion (ransom)

The specific motive shapes which tools, techniques, and targets an attacker chooses — which is why motive profiling matters in threat intelligence.

---

## Tactics, Techniques, and Procedures (TTPs)

TTPs describe the recurring behavioral fingerprint of a threat actor or group, and are central to threat profiling and detection engineering.

| Term | Definition | Why it matters |
|---|---|---|
| **Tactics** | The attacker's overall strategy, start to finish | Helps predict/detect threats early |
| **Techniques** | The specific technical methods used to achieve intermediate goals | Helps identify exploitable vulnerabilities and build defenses in advance |
| **Procedures** | The step-by-step sequence an actor follows to execute the attack | Reveals what the attacker is actually after inside the environment |

Understanding TTPs is how defenders move from reactive incident response to proactive threat hunting.

---

## Vulnerabilities

A **vulnerability** is a design or implementation weakness that an attacker can exploit to undermine a system's security — often a gap that allows authentication to be bypassed entirely. Vulnerabilities generally stem from misconfiguration or poor development practices.

### Root Causes of Vulnerabilities

**Hardware/software misconfiguration**
Insecure defaults or unencrypted protocols create openings for intrusion and data leakage. Hardware misconfig tends to expose network/system access; software misconfig tends to expose application/data access.

**Insecure network or application design**
Poorly architected firewalls, IDS, or VPN deployments leave the network exposed to threats they were meant to prevent.

**Inherent technology weaknesses**
Some technologies are simply not built to resist certain attack classes (e.g., legacy browsers vulnerable to distributed attacks). Unpatched systems compound this — a minor trojan infection can cascade into full data loss if defenses weren't updated.

**End-user carelessness**
Humans remain one of the softest targets. Credential sharing, falling for social engineering, or connecting to insecure networks all create openings independent of any technical flaw.

**Intentional end-user acts**
Former employees who retain access to shared resources can deliberately leak or misuse sensitive data — a distinct risk category from accidental carelessness.

### Technological Vulnerabilities

| Category | Details |
|---|---|
| TCP/IP protocol flaws | HTTP, FTP, ICMP, SNMP, SMTP are inherently insecure by design |
| OS vulnerabilities | Either inherently insecure, or insecure due to missing patches |
| Network device flaws | Missing password protection, missing authentication, insecure routing protocols, firewall weaknesses |

### Configuration Vulnerabilities

| Category | Details |
|---|---|
| User account issues | Credentials transmitted insecurely over the network |
| System account issues | Weak passwords set on system-level accounts |
| Internet service misconfig | e.g., unnecessarily enabled JavaScript, misconfigured IIS/Apache/FTP/Terminal Services |
| Default passwords/settings | Devices left on factory defaults |
| Network device misconfig | Incorrect setup of routers, switches, etc. |

---

## Classification of Attacks

The IATF (Information Assurance Technical Framework) groups attacks into five categories:

### 1. Passive Attacks
No direct interaction with the target — the attacker observes and collects. Because there's no active footprint, these are hard to detect.
- Footprinting
- Sniffing / eavesdropping
- Network traffic analysis
- Cracking weakly encrypted traffic

### 2. Active Attacks
The attacker actively interacts with — and often disrupts — the target, which makes these attacks more detectable than passive ones.
- Denial-of-Service (DoS)
- Bypassing protection mechanisms
- Malware (viruses, worms, ransomware)
- Data modification
- Spoofing
- Replay attacks
- Password attacks
- Session hijacking
- Man-in-the-Middle (MITM)
- DNS/ARP poisoning
- Compromised-key attacks

### 3. Close-in Attacks
Requires physical proximity to the target — either through surreptitious entry or exploiting legitimate physical access.
- Social engineering: eavesdropping, shoulder surfing, dumpster diving, etc.

### 4. Insider Attacks
Carried out by someone with legitimate, trusted access who abuses that privilege. These are especially damaging because insiders can bypass many controls outright, and are notoriously difficult to detect.
- Eavesdropping / wiretapping
- Physical device theft
- Social engineering
- Data theft or destruction

### 5. Distribution Attacks
The attacker tampers with hardware or software before it ever reaches the target — during manufacturing or in transit (e.g., vendor-inserted backdoors).
- Tampering during production
- Tampering during distribution

---

## Information Warfare

**Information warfare (InfoWar)** is the use of information and communication technology (ICT) to gain a competitive edge over an adversary. Weapons in this domain include viruses, worms, trojans, logic bombs, trap doors, electronic jamming, and penetration tools.

Martin Libicki's taxonomy breaks information warfare into seven categories:

| Category | Description |
|---|---|
| **Command & Control (C2) Warfare** | The degree of control an attacker exerts over a compromised system or network |
| **Intelligence-Based Warfare** | Sensor-driven systems designed to gather sufficient knowledge to dominate the battlespace, and to protect/deny that same knowledge to an adversary |
| **Electronic Warfare** | Uses radio-electronic methods (attacking the physical transmission of information) and cryptographic methods (disrupting information via bits/bytes) |
| **Psychological Warfare** | Propaganda and terror tactics aimed at demoralizing an adversary |
| **Hacker Warfare** | Ranges from shutting down systems to data corruption, information/service theft, covert monitoring, false messaging, and unauthorized data access — typically via viruses, logic bombs, trojans, and sniffers |
| **Economic Warfare** | Disrupting the flow of information to damage a nation's or business's economy — especially damaging to digitally-dependent organizations |
| **Cyberwarfare** | The broadest category — targeting the virtual personas of individuals or groups. Includes information terrorism, semantic attacks (system is compromised but appears to function normally), and simula-warfare (simulated conflict, e.g., weapons acquired for demonstration rather than use) |

Every category above has both a **defensive** dimension (protecting one's own ICT assets) and an **offensive** dimension (attacking an opponent's ICT assets).

---

## Quick-Reference Summary

- **CIA + AN** — the five pillars: Confidentiality, Integrity, Availability, Authenticity, Non-repudiation
- **Attack formula** — Motive + Method (TTP) + Vulnerability
- **TTPs** — Tactics (strategy) → Techniques (methods) → Procedures (execution steps)
- **Vulnerability root causes** — misconfig, poor design, tech limitations, careless users, malicious insiders
- **5 attack classes (IATF)** — Passive, Active, Close-in, Insider, Distribution
- **7 InfoWar categories (Libicki)** — C2, Intelligence-based, Electronic, Psychological, Hacker, Economic, Cyberwarfare

---

