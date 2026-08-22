# CEHv13 Module 03 — Quick Cheat Sheet

## Core scan flags

| Goal | Nmap | Remember |
|---|---|---|
| Host discovery | `-sn` | no port scan |
| ARP discovery | `-PR` | local IPv4 LAN |
| ICMP echo | `-PE` | ping |
| ICMP timestamp | `-PP` | timestamp probe |
| ICMP address mask | `-PM` | legacy discovery |
| TCP SYN ping | `-PS` | host discovery using SYN |
| TCP ACK ping | `-PA` | host discovery using ACK |
| IP protocol ping | `-PO` | protocol probes |
| TCP Connect | `-sT` | full TCP connection |
| SYN | `-sS` | half-open |
| FIN | `-sF` | FIN-only |
| NULL | `-sN` | no flags |
| XMAS | `-sX` | FIN+PSH+URG |
| Maimon | `-sM` | FIN/ACK behavior |
| ACK | `-sA` | filtering analysis |
| Idle | `-sI` | zombie/IPID technique |
| UDP | `-sU` | UDP behavior |
| SCTP INIT | `-sY` | SCTP INIT |
| SCTP COOKIE-ECHO | `-sZ` | SCTP cookie probe |
| Service/version | `-sV` | identify applications |
| OS detection | `-O` | fingerprint OS |
| NSE | `--script` | scripted checks |
| IPv6 | `-6` | IPv6 mode |

## TCP flag mnemonic

```text
SYN = Start
ACK = Acknowledge
FIN = Finish
RST = Reset
PSH = Push
URG = Urgent
```

## Port-state mnemonic

```text
OPEN             = listening
CLOSED           = reachable, no listener
FILTERED         = firewall/filter blocks certainty
UNFILTERED       = reachable, state unresolved by probe
OPEN|FILTERED    = both possibilities remain
```

## Host-discovery decision tree

```text
Local LAN?
 └─ Yes → ARP is a strong first choice

ICMP allowed?
 └─ Yes → ICMP Echo/other ICMP probes

ICMP blocked but TCP reachable?
 └─ Try SYN/ACK host discovery

Need protocol diversity?
 └─ IP protocol probing
```

## Scan interpretation

```text
SYN scan:
SYN/ACK → likely open
RST      → closed
No reply → filtered or otherwise inconclusive

UDP scan:
ICMP unreachable → closed
No reply         → open|filtered
```

## OS-fingerprint clues

- TTL
- TCP window size
- DF flag
- TCP options/order
- IPID behavior
- TCP sequence behavior
- ICMP responses

## Evasion concepts

```text
Fragmentation
Source routing
Source-port manipulation
Decoys
IP spoofing
MAC spoofing
Custom packets
Randomized host order
Bad checksums
Proxies
Anonymizers
```

## Defensive concepts

```text
Minimize exposed ports
Firewall + IDS/IPS
Ingress filtering
Egress filtering
Strong authentication
Encryption
Segmentation
Service/banner hardening
Rate limiting
Central logging/SIEM/NDR
```
