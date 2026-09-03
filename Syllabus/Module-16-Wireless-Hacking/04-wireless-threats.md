# 04 — Wireless Threats

> Objective 3 of the module: *Explain Different Wireless Threats*

## Table of Contents
- [The Five Threat Categories](#the-five-threat-categories)
- [1. Access Control Attacks](#1-access-control-attacks)
- [2. Integrity Attacks](#2-integrity-attacks)
- [3. Confidentiality Attacks](#3-confidentiality-attacks)
- [4. Availability Attacks](#4-availability-attacks)
- [5. Authentication Attacks](#5-authentication-attacks)
- [Special-Case Threats](#special-case-threats)

---

## The Five Threat Categories

To secure wireless networks, a network administrator needs to understand the various possible weaknesses that may lure attackers. Wireless networks are at risk to five broad categories of attack *(Figure — Wireless Threats overview slide)*:

```
                              WIRELESS THREATS
        ┌───────────┬──────────────┬───────────────┬────────────┬───────────────┐
        │  Access   │  Integrity   │Confidentiality│Availability│Authentication │
        │  Control  │   Attacks    │    Attacks     │  Attacks   │    Attacks    │
        └───────────┴──────────────┴───────────────┴────────────┴───────────────┘
```

This module gives each category a reference table of `Type of Attack | Description | Method and Tools`. Those tables are reproduced verbatim below, followed by narrative detail on the attacks that received a full write-up in the source material.

## 1. Access Control Attacks

Wireless access-control attacks aim to **penetrate a network by evading WLAN access-control measures**, such as AP MAC filters and Wi-Fi port access controls.

| Type of Attack | Description |
|---|---|
| **MAC Spoofing** | Reconfiguring a MAC address to appear as an authorized AP to a host on a trusted network, using tools such as SMAC. |
| **AP Misconfiguration** | If a user improperly configures critical security settings, the entire network can be exposed. Misconfigured APs cannot trigger alerts in most intrusion-detection systems because they're recognized as legitimate devices. |
| **Ad Hoc Associations** | Wi-Fi clients communicate directly via ad-hoc mode, with no AP relaying packets. Ad-hoc mode is inherently insecure — no strong authentication or encryption — so an attacker can easily connect to and compromise a client operating in it, then pivot into the wired LAN. |
| **Promiscuous Client** | Exploits the fact that 802.11 wireless cards always try to find the strongest signal. The attacker places an AP near the target with a common SSID and an irresistibly stronger/faster signal, luring clients to connect to the attacker's AP instead of the legitimate one — very similar to the evil-twin threat. |
| **Client Mis-association** | A client connects/associates with an AP outside the legitimate network — intentionally or accidentally — because WLAN signals pass through air, walls, and other obstructions. An attacker sets up a rogue AP outside the corporate perimeter, learns the target SSID, and beacons a spoofed SSID to lure clients; once connected, the attacker can launch MITM, EAP dictionary, or Metasploit-based attacks. |
| **Unauthorized Association** | Two forms: *accidental* association (connecting to a neighboring org's overlapping network without the victim's knowledge) and *malicious* association (attacker creates a **soft AP** on a laptop making its NIC appear as a legitimate AP, then gains network access, steals passwords, launches attacks on the wired network, or plants Trojans). |

### AP Misconfiguration — the key elements
- **SSID broadcast**: APs with default SSIDs are vulnerable to brute-force/dictionary attacks; even with WEP enabled, an unencrypted SSID broadcast can leak the password in plaintext.
- **Weak password**: some admins incorrectly use the SSID itself as a rudimentary password.
- **Configuration error**: mistakes made during installation, inconsistent security-change rollout across an architecture, and SSID broadcasting that helps attackers steal an SSID and impersonate a legitimate connection.

## 2. Integrity Attacks

Integrity attacks involve **changing or altering data during transmission**. Attackers send forged control, management, or data frames over a wireless network to misdirect wireless devices into performing another type of attack (e.g., a DoS attack).

*(Table 16.3 — Integrity Attacks, reproduced exactly)*

| Type of Attack | Description | Method and Tools |
|---|---|---|
| **Data-Frame Injection** | Constructing and sending forged 802.11 frames. | Airpwn-ng, Wperf |
| **WEP Injection** | Constructing and sending forged WEP encryption keys. | WEP cracking + injection tools |
| **Bit-Flipping Attacks** | Capturing the frame, flipping random bits in the data payload, modifying the ICV, and sending it to the user. | — |
| **Extensible AP Replay** | Capturing 802.1X Extensible Authentication Protocols (e.g., EAP Identity, Success, Failure) for later replay. | Wireless capture + injection tools between client and AP |
| **Data Replay** | Capturing 802.11 data frames for later (modified) replay. | Capture + injection tools |
| **Initialization Vector Replay Attacks** | Deriving the keystream by sending a plaintext message. | — |
| **RADIUS Replay** | Capturing RADIUS Access-Accept or Access-Reject messages for later replay. | Ethernet capture + injection tools between AP and authentication server |
| **Wireless Network Viruses** | Viruses have a great impact on wireless networks and can provide an attacker with a simple method to compromise APs. | — |

## 3. Confidentiality Attacks

These attacks attempt to **intercept confidential information** sent over wireless associations, regardless of whether it was sent in clear text or encrypted by Wi-Fi protocols.

*(Table 16.4 — Confidentiality Attacks, reproduced exactly)*

| Type of Attack | Description | Method and Tools |
|---|---|---|
| **Eavesdropping** | Capturing and decoding unprotected application traffic to obtain potentially sensitive information. | Wireshark, Ettercap, Kismet, commercial analyzers |
| **Traffic Analysis** | Inferring information from the observation of external traffic characteristics. | Wireshark, Ettercap, Snort |
| **Cracking WEP Key** | Capturing data to recover a WEP key using brute force or Fluhrer-Mantin-Shamir (FMS) cryptanalysis. | Aircrack-ng, WEPCrack |
| **Evil Twin AP** | Posing as an authorized AP by beaconing the WLAN's SSID to lure users. | Hostapd, EvilTwinFramework, Wifiphisher |
| **Honeypot AP** | Setting an AP's SSID to be the same as that of a legitimate AP. | Manipulating SSID |
| **Session Hijacking** | Manipulating the network such that the attacker's host appears to be the desired destination. | Manipulating |
| **Masquerading** | Pretending to be an authorized user to gain access to a system. | Stealing login IDs and passwords, bypassing authentication mechanisms |
| **MITM Attack** | Running conventional MITM attack tools on an evil-twin AP to intercept TCP sessions or SSL/SSH tunnels. | dsniff, Ettercap, aLTEr attack |

### Honeypot AP Attack — expanded
If multiple WLANs coexist in the same area, a user can connect to any available network — a scenario ripe for abuse. Normally, when a wireless client powers on, it probes nearby networks for a specific SSID. An attacker exploits this by setting up an unauthorized wireless network using a **rogue AP** with **high-power (high-gain) antennas**, using the **same SSID as the target network**. Users who regularly connect to multiple WLANs may connect to the rogue AP without realizing it. Such attacker-mounted APs are called **"honeypot" APs** — they transmit a stronger beacon signal than legitimate APs, so NICs searching for the strongest available signal connect to the rogue AP instead. If an authorized user connects to a honeypot AP, sensitive user information (identity, username, password) may be revealed to the attacker. This same "fake hotspot" trick is illustrated in the module with attackers spoofing familiar brand SSIDs — `Verizon`, `Vodafone`, `McDonald's`, `Starbucks Coffee`, `AT&T` — to trap victims who auto-connect to remembered network names.

## 4. Availability Attacks

Availability attacks aim at **obstructing the delivery of wireless services to legitimate users**, either by crippling WLAN resources or by denying access to them.

*(Table 16.5 — Availability Attacks, reproduced exactly)*

| Type of Attack | Description | Method and Tools |
|---|---|---|
| **Access Point Theft** | Physically removing an AP from its installed location. | Stealth and/or speed |
| **Disassociation Attacks** | Destroying the connectivity between an AP and client to make the target unavailable to other wireless devices. | Destruction of connectivity |
| **EAP-Failure** | Observing a valid 802.1X EAP exchange and then sending the client a forged EAP-Failure message. | Airtool Pi |
| **Beacon Flood** | Generating thousands of counterfeit 802.11 beacons to make it difficult for clients to find a legitimate AP. | — |
| **Denial-of-Service** | Exploiting the carrier-sense multiple access with collision avoidance (CSMA/CA) clear-channel-assessment (CCA) mechanism to make a channel appear busy. | An adapter that supports CW Tx mode, with a low-level utility to invoke continuous transmissions |
| **De-authenticate Flood** | Flooding client(s) with forged de-authenticates or disassociates to disconnect users from an AP. | AirJack |
| **Routing Attacks** | Distributing routing information within the network. | RIP protocol, exploiting Ad-Hoc On-Demand Distance Vector (AODV) and Dynamic Source Routing (DSR) protocols using wormhole and sinkhole attacks |
| **Authenticate Flood** | Sending forged authenticates or associates from random MACs to fill a target AP's association table. | AirJack |
| **Address Resolution Protocol (ARP) Cache Poisoning Attacks** | Creating many attack vectors. | — |
| **Power Saving Attacks** | Transmitting a spoofed traffic indication map (TIM) or delivery TIM (DTIM) to a client in power-saving mode, making the client vulnerable to a DoS attack. | — |
| **TKIP MIC Exploit** | Generating invalid TKIP data to exceed the target AP's MIC error threshold, suspending WLAN service. | — |

## 5. Authentication Attacks

The objective of authentication attacks is to **steal the identity of Wi-Fi clients** — their personal information, login credentials, etc. — to gain unauthorized access to network resources.

*(Table 16.6 — Authentication Attacks, reproduced exactly)*

| Type of Attack | Description | Method and Tools |
|---|---|---|
| **PSK Cracking** | Recovering a WPA PSK from captured key handshake frames using a dictionary attack tool. | Cowpatty, Fern Wifi Cracker |
| **LEAP Cracking** | Recovering user credentials from captured 802.1X Lightweight EAP (LEAP) packets using a dictionary attack tool to crack the NT password hash. | Asleap, THC-LEAPcracker |
| **VPN Login Cracking** | Gaining user credentials (e.g., PPTP password or IPsec pre-shared secret key) using brute-force attacks on VPN authentication protocols. | ike_scan and IKECrack (IPsec), Anger and THC-pptp-bruter (PPTP) |
| **Domain Login Cracking** | Recovering user credentials (e.g., Windows login and password) by cracking NetBIOS password hashes with brute-force or dictionary tools. | John the Ripper, L0phtCrack, THC-Hydra |
| **Key Reinstallation Attack** | Exploiting the four-way handshake of the WPA2 protocol. | Nonce reuse technique |
| **Identity Theft** | Capturing user identities from cleartext 802.1X Identity Response packets. | Packet capturing tools |
| **Shared Key Guessing** | Attempting 802.11 shared-key authentication with the vendor default or cracked WEP keys. | WEP cracking tools, Wifite |
| **Password Speculation** | Repeatedly attempting 802.1X authentication using a captured identity to guess the user's password. | Password dictionary |
| **Application Login Theft** | Capturing user credentials (e.g., email address and password) from cleartext application protocols. | Ace Password Sniffer, dsniff, Wi-Jacking Attack |

## Special-Case Threats

Three attacks get individual deep-dives in the source material because they don't fit neatly into a single row of the tables above.

### Wormhole Attack
Exploits dynamic routing protocols such as **Dynamic Source Routing (DSR)** and **Ad-Hoc On-Demand Distance Vector (AODV)**. The attacker positions themselves strategically in the target network to sniff and record ongoing wireless transmissions, then advertises that a malicious node has the shortest route for transmitting data to other nodes. To sniff and record ongoing communication, the attacker creates a **tunnel** to forward data between the source and destination nodes.

In wireless sensor networks, AODV/DSR use **Route Request (RREQ)** and **Route Reply (RREP)** messages to discover dynamic routes: a source node (S) broadcasts an RREQ to the destination node (D), and D unicasts an RREP back containing the route to reach D; S stores this in its route cache and forwards all application data to D via that route.

In a wormhole attack, the attacker builds a tunnel between S and D via a malicious node (M) within transmission range of both. The attacker listens for RREQ messages; when S tries to send data to D, it first sends an RREQ to discover the route. The attacker sniffs this RREQ and forwards it directly to D **before** the original reaches D by the legitimate path. Similarly, it sniffs D's RREP and forwards it to S before the original arrives — creating a fake direct link between S and D via M. Once the tunnel is established, the attacker controls the data flow between the two nodes and may launch further attacks. Wormhole attacks pose a severe threat to wireless sensor networks because attackers may manipulate routing and application data in real time, impacting confidentiality, integrity, and availability all at once.

### Sinkhole Attack
A variant of the selective-forwarding attack in which the attacker advertises a compromised/malicious node as the **shortest possible route to the base station**. The attacker places the malicious node near the base station to attract all neighboring nodes with fake routing-path information, then performs a data-forging attack — using the compromised node to sniff and manipulate all ongoing network transmissions.

A sinkhole attack can be combined with a wormhole attack, where the malicious node occupies all network traffic and uses tunneling to reach the base station faster than legitimate nodes. Sinkhole attacks are complex to detect and can adversely affect higher-layer applications in the OSI model.

### Inter-Chip Privilege Escalation / Wireless Co-Existence Attack
Exploits underlying vulnerabilities in **combo chips** that handle multiple wireless protocols (e.g., a single chip handling both Bluetooth and Wi-Fi, which manufacturers increasingly ship instead of separate chips). Attackers leverage the combo chip to compromise one radio (say, Bluetooth) and use shared resources to steal data from, or manipulate traffic passing through, the other radio (Wi-Fi) — a lateral move across chip boundaries. This can cause a **wireless co-existence attack**, leading to privilege escalation at the chip-to-chip trust boundary.

---
**Previous:** [`03-wireless-encryption-wep-wpa-wpa2-wpa3.md`](03-wireless-encryption-wep-wpa-wpa2-wpa3.md)
**Next:** [`05-wifi-discovery-and-footprinting.md`](05-wifi-discovery-and-footprinting.md) — start of the practical wireless hacking methodology.
