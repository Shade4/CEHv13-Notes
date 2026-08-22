# 03 — Host Discovery

## 3.1 Why Host Discovery Comes First

Before spending time port-scanning every single address in a range, you want to know which of those addresses are actually attached to a live system. Host discovery answers exactly one question per IP: **"is anything home?"** It's the first practical step in scanning, and it exists purely to save time — there's no point running a full 65,535-port scan against an address nobody's using.

Nmap groups host discovery techniques into four families, each using a different protocol to provoke a response:

```
Host Discovery Techniques
│
├── ARP Ping Scan            nmap -sn -PR <Target IP>
├── UDP Ping Scan            nmap -sn -PU <Target IP>
├── ICMP Ping Scan
│   ├── ICMP ECHO Ping       nmap -sn -PE <Target IP>
│   ├── ICMP ECHO Ping Sweep nmap -sn -PE <IP Range>
│   ├── ICMP Timestamp Ping  nmap -sn -PP <Target IP>
│   └── ICMP Address Mask    nmap -sn -PM <Target IP>
├── TCP Ping Scan
│   ├── TCP SYN Ping         nmap -sn -PS <Target IP>
│   └── TCP ACK Ping         nmap -sn -PA <Target IP>
└── IP Protocol Scan         nmap -sn -PO <Target IP>
```

`-sn` tells Nmap "just tell me if the host is up — skip the port scan."

## 3.2 ARP Ping Scan

**Syntax:** `nmap -sn -PR <Target IP>`

ARP scanning discovers active devices on the local IPv4 subnet by sending ARP request probes and watching for ARP replies. Because the sender needs the destination's hardware (MAC) address to correctly address the Ethernet frame, the OS has to issue an ARP request regardless of any higher-layer firewall rule — **ARP typically isn't filtered by host-based or perimeter firewalls the way ICMP/TCP/UDP often is**, which makes this the most reliable discovery technique on a local LAN.

```
   Attacker  ---- ARP request probe -------->  Target
   Attacker  <--- ARP response ("Host is Active") --
```

If the target doesn't answer after a set number of attempts, the source records an "incomplete" entry in its local ARP table and moves on.

> **Note:** Nmap uses ARP ping as its *default* ping method whenever you're scanning a target on the same local network — you have to explicitly disable it with `--disable-arp-ping` if you want to force a different ping type.

**Advantages:**
- More efficient and accurate than the other discovery techniques (on-LAN)
- Handles retransmission/timeout automatically without extra flags
- Good for large local address-space sweeps
- Can report response latency per host

## 3.3 UDP Ping Scan

**Syntax:** `nmap -sn -PU <Target IP>`

Similar in spirit to a TCP ping, but sends UDP packets instead. Nmap's default UDP-ping destination port is the deliberately obscure **40,125** (configurable at compile-time via `DEFAULT_UDP_PROBE_PORT_SPEC`) — a port unlikely to be running any real service, so a response reliably indicates something about host state rather than an application quirk.

- **Host active:** target replies with a UDP response.
- **Host inactive/unreachable:** you get an ICMP error (host/network unreachable, TTL exceeded) or nothing at all.

**Advantage:** UDP ping can find hosts sitting behind firewalls with strict TCP filtering but looser UDP rules — many perimeter devices are configured with far more attention paid to TCP than UDP.

## 3.4 ICMP Ping Scan

The classic "ping," in several variants, each useful when a different one is blocked.

### ICMP ECHO Ping
**Syntax:** `nmap -sn -PE <Target IP>`

Sends an ICMP ECHO request; a live host answers with an ICMP ECHO reply.

```
Source (10.10.1.19) -- ICMP Echo Request -->  Destination (10.10.1.11)
Source (10.10.1.19) <-- ICMP Echo Reply  ----  Destination (10.10.1.11)
```

A ping also reports **round-trip time (RTT)** — how long the full request/reply cycle took — and can be used for basic hostname resolution sanity-checking (if a reply comes back when pinging by IP but not by name, something's off in DNS resolution for that host).

**Platform quirk:** UNIX/Linux/BSD TCP/IP stacks reply to ICMP echo requests sent to a *broadcast* address; Windows stacks generally do not. This asymmetry itself is a mini OS fingerprinting signal (see file `05`).

### ICMP ECHO Ping Sweep
**Syntax:** `nmap -sn -PE <IP Range>`

A ping sweep is just the ECHO ping technique run against an entire range instead of a single host — the oldest and slowest host-discovery method, but supported almost everywhere. Live hosts each answer with their own ICMP ECHO reply, and the attacker walks away with an inventory of active machines in the subnet.

```
                    ICMP Echo Request
        Attacker  ------------------->  10.10.1.9
        Attacker  ------------------->  10.10.1.11  <-- ICMP Echo Reply --
        Attacker  ------------------->  10.10.1.13  <-- ICMP Echo Reply --
        Attacker  ------------------->  10.10.1.22
```
(Only hosts that reply are "up" — silence just means no reply was seen, not conclusively that the host is down, since firewalls may simply be dropping the probe.)

Attackers often calculate the subnet mask first (subnet-mask calculators), then ping-sweep the resulting address range to build an inventory of live systems before moving to port scanning.

Nmap tuning options relevant to sweeps: `-PE` (which probe type to use), `-L` (increase parallel ping count), `-T` (tweak the ping timeout value).

### ICMP Timestamp Ping
**Syntax:** `nmap -sn -PP <Target IP>`

An alternate ICMP probe that queries the target for its current time. A response confirms the host is alive; whether the host actually *answers with* a time value is configuration-dependent on the target's side. This variant is specifically useful **when an administrator has blocked traditional ICMP ECHO requests** but left timestamp queries unfiltered.

### ICMP Address Mask Ping
**Syntax:** `nmap -sn -PM <Target IP>`

Same idea as timestamp ping, but queries the target for its subnet mask instead. Also conditional on target configuration, and also useful specifically as a workaround when standard ECHO pings are blocked.

## 3.5 TCP Ping Scan

### TCP SYN Ping
**Syntax:** `nmap -sn -PS <Target IP>` (or `-PS22-25,80,113,1050,35000` to probe a specific port list in parallel)

Probes a port (default **80**) by sending an empty TCP SYN packet — a partial three-way handshake:

```
   Attacker -- empty TCP SYN packet -->  Target Host
   Attacker <---------- ACK packet ----  Target Host   ("Host is Active")
   Attacker ---------- RST ------------> Target Host   (tear down; goal achieved)
```

Because the connection is deliberately never completed (RST instead of the final ACK), **this scan leaves no connection-level log trace** at the system/network level and can be run against many machines in parallel without waiting on individual timeouts.

**Advantages:**
- Parallel-friendly — no waiting on individual timeouts
- Confirms liveness without establishing an actual connection, so it's quieter than a full connect

### TCP ACK Ping
**Syntax:** `nmap -sn -PA <Target IP>`

Also targets port 80 by default, but sends an empty **ACK** packet directly (no prior SYN — there's no real connection to acknowledge). Since the target never asked for anything, it responds with **RST** — and receiving that RST is itself the "host is active" signal.

```
   Attacker -- empty TCP ACK packet -->  Target Host
   Attacker <---------- RST -----------  Target Host   ("Host is Active")
```

**Advantage:** Firewalls are commonly configured to block SYN pings (the most recognizable pattern) while overlooking ACK probes — using both SYN and ACK pings together maximizes the chance of slipping past whatever rule set is in place.

## 3.6 IP Protocol Scan

**Syntax:** `nmap -sn -PO <Target IP>`

The newest/most general host-discovery option — sends IP packets carrying different protocol headers and treats *any* response as proof of life.

```
   Attacker -- ICMP, IGMP, TCP, and UDP packets -->  Target Host
   Attacker <----------- Any response -------------  Target Host  ("Host is Active")
```

By default (no protocol specified) Nmap sends probes for ICMP (protocol 1), IGMP (protocol 2), and IP-in-IP (protocol 4). This default set is configurable at compile time via `DEFAULT_PROTO_PROBE_PORT_SPEC` in `nmap.h`. For ICMP, IGMP, TCP (protocol 6), and UDP (protocol 17) specifically, full protocol headers are sent; for everything else, only the bare IP header is sent.

## 3.7 Host Discovery with AI

The source material shows the same "prompt an AI shell-assistant" pattern used for host discovery:

**Prompt:** *"Scan the target network 10.10.1.0/24 for active hosts and place only the IP addresses into a file scan1.txt"*
```bash
nmap -sn 10.10.1.0/24 -oG - | awk '/Up$/{print $2}' > scan1.txt
```
- `-sn 10.10.1.0/24` — ping-sweep the whole /24
- `-oG -` — grepable output, printed to stdout
- `| awk '/Up$/{print $2}'` — filter lines ending "Up" and print field 2 (the IP)
- `> scan1.txt` — save the resulting IP list

That list can then be fed straight into a follow-on scan:
```bash
nmap -T4 -iL scan1.txt -oN scan2.txt -v0
```
`-iL` reads targets from a file, `-T4` sets aggressive timing, `-oN` writes normal-format output, `-v0` suppresses non-error output.

A more complete example chains discovery and enumeration into one script:
```bash
#!/bin/bash
nmap -sP 10.10.1.0/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt &&
nmap -iL live_hosts.txt -sV -oA scan_results &&
cat scan_results.nmap
```
Ping-sweep → extract live IPs → version-scan each live IP → dump the combined report. This is a good template for turning a one-off manual workflow into a repeatable script.

## 3.8 Ping Sweep Tools (beyond Nmap)

| Tool | Notes |
|---|---|
| **Angry IP Scanner** (https://angryip.org) | Pings each address in a range, optionally resolves hostname, grabs MAC address, port-scans; extensible via plugins (NetBIOS info, favorite ranges, web server detection); multithreaded (one thread per scanned IP); exports to CSV/TXT/XML/IP-port lists |
| SolarWinds Engineer's Toolset | https://www.solarwinds.com |
| NetScanTools Pro | https://www.netscantools.com |
| Colasoft Ping Tool | https://www.colasoft.com |
| Advanced IP Scanner | https://www.advanced-ip-scanner.com |
| OpUtils | https://www.manageengine.com |

---

**Next:** [`04-port-and-service-discovery.md`](04-port-and-service-discovery.md) — now that you know which hosts are alive, find out what's actually running on them.
