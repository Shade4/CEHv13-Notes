# Cheatsheet — DoS/DDoS Attack Quick Reference

One-line lookups for every named attack technique in this module. Built for rapid exam review —
if you can match a CEH scenario question to the right row here, you're set.

## Attack Vector Categories

| Category | Exhausts | Measured in |
|---|---|---|
| Volumetric | Bandwidth | bits/sec (bps) |
| Protocol | Connection-state tables | packets/sec (pps) |
| Application-Layer | App/service resources | requests/sec (rps) |

## Volumetric Attacks

| Attack | One-liner |
|---|---|
| UDP Flood | Spoofed UDP packets to random ports; target replies with ICMP "Destination Unreachable" per packet, exhausting resources |
| ICMP Flood | Mass ICMP ECHO requests saturate bandwidth via reply traffic; mitigated with a threshold limit (default ~1000 pps) |
| Ping of Death (PoD) | Single oversized/malformed ping packet (>65,535 bytes) crashes the target during reassembly |
| Smurf | ICMP ECHO requests spoofed with the victim's IP, sent to a broadcast network — every host replies to the victim |
| Pulse Wave | Periodic high-bandwidth bursts (300+ Gbps) every ~10 min instead of a continuous flood; very hard to recover from |
| Zero-Day DDoS | Exploits an unpatched, unknown DDoS vulnerability — no defense exists yet by definition |
| NTP Amplification | Spoofed request to an NTP server's `monlist` command produces a large reply sent to the victim |

## Protocol Attacks

| Attack | One-liner |
|---|---|
| SYN Flood | Fake-source SYN packets fill the half-open connection queue; server never gets the final ACK |
| SYN-ACK Flood | Spoofed SYN-ACK packets sent directly at the target to exhaust matching resources |
| ACK / PUSH ACK Flood | Spoofed ACK/PUSH ACK packets that look like existing-session traffic overload the target |
| Fragmentation Attack | Flood of 1500+ byte fragments with randomized content overloads packet reassembly |
| Multiple SYN-ACK Spoofed Session Flood | Fake session using multiple SYN + multiple ACK + RST/FIN packets |
| Multiple ACK Spoofed Session Flood | Fake session skipping SYN entirely — evades SYN-count-based firewall detection |

## Application-Layer Attacks

| Attack | One-liner |
|---|---|
| HTTP GET Attack | Time-delayed HTTP header holds the connection open indefinitely |
| HTTP POST Attack | Complete header, incomplete body — server waits forever for the rest |
| Single-Session HTTP Flood | Multiple requests bombarded within one HTTP 1.1 session |
| Single-Request HTTP Flood | Multiple requests hidden inside a single HTTP packet — stealthy |
| Recursive HTTP GET Flood | Mimics a user browsing sequential pages while stealthily flooding |
| Random Recursive GET Flood | Same as above but targets forums/blogs using random valid page numbers |
| Slowloris | Partial HTTP requests trickle just enough data to keep connections open forever, exhausting the connection pool |
| UDP Application-Layer Flood | Abuses UDP-based app protocols (CHARGEN, NTP, SNMPv2, QOTD, RPC, SSDP, CLDAP, TFTP, NetBIOS, Quake, Steam, VoIP) |

## Advanced / Cross-Cutting Attacks

| Attack | One-liner |
|---|---|
| Multi-Vector Attack | Combines volumetric + protocol + application-layer attacks, in sequence or in parallel, to confuse defenders |
| Peer-to-Peer (P2P) Attack | Exploits DC++ bugs to redirect P2P file-sharing clients toward a fake "victim" website — no botnet needed |
| Permanent DoS (PDoS) / "Phlashing" | Fake firmware/hardware update bricks the device permanently — irreversible, unlike other DoS types |
| TCP SACK Panic Attack | SACK packets with MSS=48 bytes overflow the Linux socket buffer's 17-segment limit → kernel panic |
| Distributed Reflection DoS (DRDoS) | Spoofed SYNs sent to uninvolved reflectors, who flood the real target with unsolicited SYN/ACKs |
| DDoS Extortion / Ransom DDoS (RDDoS) | Attacker demands payment after a "proof of capability" mini-attack, threatening a bigger one |

## Botnet Scanning Methods (finding new victims)

| Method | One-liner |
|---|---|
| Random Scanning | Probes random IPs across the target range |
| Hit-List Scanning | Pre-built target list, split in half and shared with each new bot — exponential growth |
| Topological Scanning | Uses info found on an already-infected machine (URLs, configs) to find new targets |
| Local Subnet Scanning | Infected machine scans its own local network behind the firewall |
| Permutation Scanning | Shared pseudorandom IP list walked from a point-of-infection offset |

## Malicious Code Propagation Techniques

| Technique | One-liner |
|---|---|
| Central Source Propagation | Central server pushes a toolkit copy to each newly infected host (HTTP/FTP/RPC) |
| Back-Chaining Propagation | Newly infected host pulls the toolkit back from the attacker's own system (often via TFTP) |
| Autonomous Propagation | The attacking host transfers the toolkit itself, at the exact moment of exploitation |

## Detection Techniques

| Technique | One-liner |
|---|---|
| Activity Profiling | Watches average packet rate & flow-cluster entropy for abnormal increases |
| Sequential Change-Point Detection | CUSUM algorithm flags sudden shifts in traffic flow rate over time |
| Wavelet-Based Signal Analysis | Frequency-domain analysis flags unusual high-frequency energy spikes |

## Countermeasure Categories

`Absorb the Attack` · `Degrade Services` · `Shut Down Services` — high-level response postures

`Egress Filtering` · `Ingress Filtering` · `TCP Intercept` · `Rate Limiting` — prevent potential
attacks

`Honeypots (low/high-interaction)` — deflect attacks

`Load Balancing` · `Throttling` · `Drop Requests` — mitigate attacks

`Traffic Pattern Analysis` · `Packet Traceback` · `Event Log Analysis` — post-attack forensics

`RFC 3704 Filtering` · `Cisco IPS Source IP Reputation Filtering` · `Black Hole Filtering` ·
`ISP DDoS Prevention Offerings` — botnet-specific defenses