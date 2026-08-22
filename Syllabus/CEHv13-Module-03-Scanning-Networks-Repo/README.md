# CEHv13 Module 03 — Scanning Networks

> **Study repository based on the uploaded CEH v13 Module 03: Scanning Networks curriculum PDF.**
>
> This repository converts the module into structured, exam-oriented and lab-oriented notes. The wording is intentionally rewritten rather than copied verbatim from the course material.

## What this repository covers

This module builds the transition from reconnaissance into active network scanning. The source module is organized around six learning objectives:

1. Explain network scanning concepts.
2. Demonstrate host-discovery scanning techniques.
3. Demonstrate port and service-discovery techniques.
4. Demonstrate OS-discovery techniques.
5. Demonstrate scanning techniques intended to get around IDS/firewall controls.
6. Explain network-scanning countermeasures.

The source frames scanning as the phase where a tester gathers more actionable information about reachable systems, ports, services, configurations and possible weaknesses after initial reconnaissance.

> **Authorization rule:** perform the commands in this repository only against systems you own or have explicit permission to test. For practice, prefer a local VM lab, CTF target, or isolated virtual network.

---

## Repository structure

```text
CEHv13-Module-03-Scanning-Networks/
├── README.md
├── docs/
│   ├── CHEATSHEET.md
│   ├── LAB-GUIDE.md
│   └── TOOL-MATRIX.md
└── .gitignore
```

---

# 1. Network Scanning Fundamentals

## 1.1 What is network scanning?

Network scanning is the deliberate examination of a network or host to discover information that is useful for security assessment. Typical results include:

- Which hosts appear to be alive.
- Which IP addresses are in use.
- Which TCP or UDP ports are reachable.
- Which services appear behind those ports.
- Which application/service versions are exposed.
- Which operating system characteristics can be inferred.
- What filtering or firewall behavior is visible.
- Which weaknesses may deserve later validation.
- How hosts, routers, switches and other devices may be connected.

The module describes scanning as a systematic process rather than a single command. A practical workflow is:

```text
Reconnaissance
      ↓
Identify target range
      ↓
Host discovery
      ↓
Port discovery
      ↓
Service/version discovery
      ↓
OS discovery
      ↓
Vulnerability/configuration review
      ↓
Map findings and plan next validation
```

Scanning therefore answers a different question from passive reconnaissance. Recon tells you **what might exist**; scanning attempts to determine **what is actually responding and exposing network behavior**.

## 1.2 Why scan a network?

The curriculum highlights several reasons:

- Locate live hosts before spending resources on deeper scans.
- Identify open ports and potential entry points.
- Learn which services are exposed.
- Associate services with versions.
- Infer operating systems and network stacks.
- Identify possible misconfigurations or vulnerable services.
- Understand topology and communication paths.
- Give defenders a way to verify whether security controls are behaving as intended.

## 1.3 Types of scanning in the module

The module groups scanning into three broad purposes early on:

### Port scanning
Checks ports to determine whether services may be listening. TCP flag behavior is central to many port-scanning techniques.

### Network/host scanning
Discovers active hosts and IP addresses before detailed service analysis.

### Vulnerability scanning
Looks for known weaknesses or indicators of exploitable configurations. The source emphasizes that vulnerability scanning can involve checking for common files, known vulnerabilities, weak configurations and exposed services.

---

# 2. TCP Communication and Flags

Understanding TCP is essential because many scanning techniques are really experiments with TCP state transitions.

## 2.1 Important TCP flags

The module highlights these six flags:

| Flag | Meaning | High-level use in scanning |
|---|---|---|
| SYN | Synchronize | Starts a TCP connection and is central to SYN scans |
| ACK | Acknowledgment | Confirms receipt/sequence expectations; used by ACK scans |
| PSH | Push | Requests that buffered data be delivered promptly |
| URG | Urgent | Marks urgent data handling |
| FIN | Finish | Signals the sender wants to end a TCP stream |
| RST | Reset | Aborts/rejects a connection or reports certain invalid states |

## 2.2 TCP three-way handshake

A normal TCP connection is established with:

```text
Client                      Server
  |                           |
  | -------- SYN -----------> |
  | <------ SYN + ACK ------- |
  | -------- ACK -----------> |
  |                           |
  |      connection ready     |
```

The module explains that a full TCP connection uses this handshake before normal data transfer.

### Why this matters to scanning

A scanner can intentionally stop after one or two packets instead of completing the session. That is the basic idea behind a half-open/stealth SYN scan.

## 2.3 TCP connection termination

A normal close generally involves FIN/ACK exchange. A RST is different: it abruptly resets the state rather than gracefully closing a session.

This distinction becomes important when interpreting scanner responses.

---

# 3. Scanning Tools

The module introduces several tools and tool families.

## 3.1 Nmap

Nmap is the central scanner throughout this module. The source presents it as a network exploration and security-auditing tool that can identify hosts, services, ports and operating-system characteristics.

Typical syntax:

```bash
nmap [options] <target>
```

Useful study examples using a placeholder lab target:

```bash
# Host discovery
nmap -sn 192.0.2.10

# Common ports + basic service information
nmap 192.0.2.10

# Scan selected ports
nmap -p 22,80,443 192.0.2.10

# Service/version detection
nmap -sV 192.0.2.10

# OS detection (lab/authorized targets)
sudo nmap -O 192.0.2.10
```

### Concepts to remember

- `-sn` — host discovery / ping scan.
- `-p` — choose ports.
- `-sV` — service/version detection.
- `-O` — OS detection.
- `-A` — aggressive combined detection profile; use cautiously in a lab because it can be noisy.
- `-oN`, `-oX`, `-oG` — save results in normal, XML or grep-friendly formats.
- `-T<0-5>` — timing template.

## 3.2 Hping3

Hping3 is presented as a packet-crafting and network-testing utility that can send custom TCP/IP packets and support different probe types.

The module demonstrates it for:

- ICMP probing.
- ACK probing.
- UDP probing.
- SYN scanning.
- FIN/PSH/URG-style probing.
- Timestamp-related behavior.
- Sequence-number collection.
- Packet crafting.

Safe lab examples:

```bash
# Basic ICMP test
hping3 -1 -c 3 192.0.2.10

# TCP ACK probe to port 80
sudo hping3 -A -p 80 -c 3 192.0.2.10

# UDP probe to port 53
sudo hping3 -2 -p 53 -c 3 192.0.2.10
```

Some Hping3 combinations can generate substantial traffic; use them only in an isolated lab.

## 3.3 Metasploit

The module introduces Metasploit as a broader penetration-testing platform containing scanners and auxiliary modules in addition to exploitation capabilities.

Example of a scanner-oriented workflow in an authorized lab:

```text
msfconsole
search type:auxiliary scanner
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.0.2.10
run
```

The important learning point is not the framework itself; it is that scanning can be integrated into a larger assessment workflow.

## 3.4 NetScanTools Pro

The source describes it as a commercial Windows network troubleshooting/monitoring toolkit able to gather network information through active and passive techniques.

## 3.5 Other tools mentioned

The module also names tools including:

- Angry IP Scanner
- RustScan
- MegaPing
- SolarWinds Engineer's Toolset
- PRTG Network Monitor
- Wireshark
- Unicornscan
- Nmap NSE
- ProxySwitcher
- CyberGhost VPN
- Whonix
- Tails
- Colasoft Packet Builder
- ExtraHop
- Splunk Enterprise Security
- other scanning/monitoring products referenced in the source tables

Not every named tool has the same role. Some discover hosts, some inspect packets, some craft traffic, some provide network monitoring and some are anonymity/privacy tools.

---

# 4. Host Discovery

Host discovery is the process of finding which addresses appear to represent live systems before deeper scanning.

The module lists several techniques:

- ARP ping scan.
- UDP ping scan.
- ICMP echo ping.
- ICMP echo ping sweep.
- ICMP timestamp ping.
- ICMP address-mask ping.
- TCP SYN ping.
- TCP ACK ping.
- IP protocol ping.
- Ping sweep utilities.

## 4.1 ARP ping scan

ARP operates at the local-link level and is particularly useful inside an IPv4 LAN. Instead of asking the target to respond through an upper-layer protocol, a scanner uses ARP request/reply behavior to determine whether an address is active on the local network.

The module shows Nmap's `-PR` behavior for ARP ping on local Ethernet-style networks.

Example:

```bash
sudo nmap -PR 192.0.2.0/24
```

### Why ARP discovery is strong on local networks

An ARP response gives both reachability information and a link-layer identity (MAC address). This makes ARP-based discovery very effective within the same broadcast domain.

## 4.2 UDP ping

UDP probing can be useful when traditional ICMP echo requests are filtered.

Example:

```bash
sudo nmap -PU 192.0.2.10
```

Interpretation is context-dependent. Some systems may answer with an ICMP error for a closed UDP port; a response indicates that traffic reached the stack, but silence does not always prove a host is absent because filtering and rate limiting can suppress responses.

## 4.3 ICMP Echo ping

Classic ping uses ICMP Echo Request and Echo Reply.

```bash
ping -c 4 192.0.2.10
```

Nmap equivalent:

```bash
nmap -PE 192.0.2.10
```

## 4.4 ICMP echo ping sweep

A ping sweep applies host discovery across a range.

```bash
sudo nmap -sn 192.0.2.0/24
```

Useful result interpretation:

```text
Host is up → address is responding to at least one selected discovery method
No response → may be down, filtered, rate-limited, or otherwise not answering
```

Do not equate **no reply** with **definitely offline**.

## 4.5 ICMP timestamp ping

The source covers ICMP Timestamp Requests as an alternate probing method. The goal is not merely reachability but examining whether the target answers this ICMP message type.

Nmap syntax shown conceptually in the module:

```bash
sudo nmap -PP 192.0.2.10
```

## 4.6 ICMP address-mask ping

The module also describes ICMP Address Mask Requests as another legacy discovery method.

Nmap syntax:

```bash
sudo nmap -PM 192.0.2.10
```

## 4.7 TCP SYN ping

A SYN ping sends a TCP SYN probe to a selected port. Receiving SYN/ACK suggests that a service or TCP stack is reachable. A reset can also prove the host is active even if the requested port is closed.

Example:

```bash
sudo nmap -PS80,443 192.0.2.10
```

## 4.8 TCP ACK ping

ACK ping uses a TCP ACK packet rather than SYN. The key idea is that a returned RST can demonstrate that the TCP/IP stack is reachable.

```bash
sudo nmap -PA80,443 192.0.2.10
```

## 4.9 IP protocol ping

This technique sends probes using different IP protocols rather than relying on only one transport protocol.

Example:

```bash
sudo nmap -PO1,6,17 192.0.2.10
```

Here the protocol numbers correspond to examples such as ICMP (1), TCP (6) and UDP (17).

## 4.10 Ping sweep tools

The module describes tools such as Angry IP Scanner and lists several other utilities that can identify live hosts in a range.

The core advantage of a dedicated ping-sweep utility is convenience and speed when the immediate question is simply **which addresses are alive?**

---

# 5. Port and Service Discovery

After host discovery, the next question is: **which ports are reachable, and what may be listening there?**

## 5.1 Common ports

The source includes a reserved-port reference table. High-value ports to memorize for CEH study include:

| Port | Protocol | Typical service |
|---:|---|---|
| 20 | TCP | FTP data |
| 21 | TCP | FTP control |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67/68 | UDP | DHCP |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 111 | TCP/UDP | RPCbind / portmapper |
| 119 | TCP | NNTP |
| 123 | UDP | NTP |
| 135 | TCP/UDP | Microsoft RPC-related service |
| 137–139 | UDP/TCP | NetBIOS family |
| 143 | TCP | IMAP |
| 161/162 | UDP | SNMP / SNMP traps |
| 389 | TCP/UDP | LDAP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB |
| 500 | UDP | IKE / ISAKMP |
| 514 | UDP | Syslog |
| 515 | TCP | Line printer / LPD |
| 631 | TCP/UDP | IPP |
| 636 | TCP/UDP | LDAPS |
| 1433 | TCP | Microsoft SQL Server |
| 1521 | TCP | Oracle listener |
| 1723 | TCP | PPTP |
| 2049 | TCP/UDP | NFS |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP |
| 5432 | TCP | PostgreSQL |
| 5900 | TCP | VNC |
| 6000–6063 | TCP | X11 |
| 6667 | TCP | IRC |

> The table above is a study aid derived from the source's reserved-port tables. Service assignments can vary in real environments.

## 5.2 Port states

Nmap and similar scanners commonly classify a port as:

- **open** — an application appears to be listening.
- **closed** — the host is reachable but nothing is listening on that port.
- **filtered** — filtering prevents the scanner from determining the state directly.
- **unfiltered** — the port is reachable but the chosen probe does not establish whether it is open or closed.
- **open|filtered** — the response pattern is compatible with either open or filtered.

Understanding the state is more important than memorizing an isolated command.

---

# 6. TCP Port-Scanning Techniques

The module divides TCP scans into multiple families.

## 6.1 TCP Connect / full-open scan

A full TCP connection follows the normal three-way handshake.

Conceptual exchange when the port is open:

```text
SYN  →
     ← SYN/ACK
ACK  →
```

If the port is closed, a scanner normally receives an RST instead of completing the connection.

Nmap:

```bash
nmap -sT -p 22,80,443 192.0.2.10
```

### Strengths

- Reliable when raw-packet privileges are unavailable.
- Uses normal TCP behavior.
- Easy to understand.

### Weaknesses

- Creates a completed connection.
- More likely to appear in ordinary connection logs.
- Potentially noisier than a half-open SYN scan.

## 6.2 SYN / half-open scan

The scanner sends SYN and interprets the reply without completing the connection.

Open-port pattern:

```text
SYN      →
         ← SYN/ACK
RST      →
```

Closed-port pattern:

```text
SYN      →
         ← RST
```

Nmap:

```bash
sudo nmap -sS -p 1-1000 192.0.2.10
```

This is one of the most important CEH scanning techniques.

## 6.3 NULL scan

A NULL scan sends a TCP packet with no flags set.

```bash
sudo nmap -sN 192.0.2.10
```

The technique depends heavily on operating-system TCP/IP behavior. The source notes that it is not universally reliable, especially across platforms that do not follow the same RFC-derived behavior.

## 6.4 FIN scan

FIN scan sends FIN without completing a normal session.

```bash
sudo nmap -sF 192.0.2.10
```

It is historically associated with interpreting different responses from open versus closed ports, with important OS-specific caveats.

## 6.5 XMAS scan

XMAS sets multiple flags at once, typically FIN, PSH and URG.

```bash
sudo nmap -sX 192.0.2.10
```

The unusual flag combination is the reason for the name.

## 6.6 Maimon scan

The Maimon technique uses a FIN/ACK-style probe and depends on implementation behavior to infer the state of ports.

Nmap:

```bash
sudo nmap -sM 192.0.2.10
```

## 6.7 ACK flag probe scan

ACK scanning is primarily useful for mapping filtering behavior rather than directly proving a port is listening.

```bash
sudo nmap -sA 192.0.2.10
```

The source discusses two related variants:

- **TTL-based analysis**.
- **Window-size-based analysis**.

The important conceptual result is often **filtered vs unfiltered**, not simply open vs closed.

### TTL-based reasoning

If RST responses show different TTL characteristics, a scanner may infer useful information about filtering behavior or stack behavior.

### Window-based reasoning

Some legacy stacks returned distinct TCP window values in RST responses. Historically, a non-zero window could provide a clue that a port was open under specific circumstances. Modern systems and network devices can make this heuristic unreliable.

## 6.8 Idle / IPID-header scan

The module explains the idea of using a third host (a "zombie") whose IP identification counter behavior can be observed to infer activity at another target.

High-level workflow:

```text
1. Probe zombie and observe IPID behavior.
2. Send spoofed-looking probe toward target using zombie's identity.
3. Probe zombie again.
4. Compare IPID change.
5. Infer whether target caused a response through the zombie.
```

Nmap syntax has historically used `-sI <zombie>[:probeport] <target>` for idle scanning. This is an advanced and environment-sensitive technique; use it only in a closed lab.

## 6.9 UDP scan

UDP scanning is fundamentally different because UDP has no three-way handshake.

```bash
sudo nmap -sU -p 53,69,123,161 192.0.2.10
```

A closed UDP port may respond with ICMP Port Unreachable. Silence can mean open, filtered, rate-limited, or otherwise unanswered.

### Practical issue: slowness

UDP scanning is often slower because:

- Many ports do not reply.
- ICMP errors can be rate-limited.
- Scanners wait longer before declaring a port unanswered.

## 6.10 UDP response logic

The module discusses two important interpretations:

- Closed UDP → ICMP unreachable response can indicate the port is closed.
- No response → does not prove the port is open; it can also be filtered.

This is a recurring exam trap: **silence is not automatically proof of openness**.

## 6.11 UDP RECVFROM / WRITE scanning concept

The source discusses a more specialized method that can use a UDP socket's received-error behavior to infer port state under certain local conditions. It is primarily relevant to Unix/Linux semantics and may require elevated privileges.

## 6.12 SCTP INIT scan

SCTP is a transport protocol with multi-streaming and message-oriented behavior. An INIT probe can resemble a half-open discovery approach.

Nmap:

```bash
sudo nmap -sY -p 2905 192.0.2.10
```

The module explains:

- INIT ACK → open/listening behavior.
- ABORT → port is not listening.
- No response or ICMP unreachable after retransmissions → may indicate filtering.

## 6.13 SCTP COOKIE-ECHO scan

This is a more advanced SCTP technique. The source explains that a COOKIE-ECHO probe can help distinguish states under certain implementations but may not always separate open and filtered as cleanly as desired.

Nmap:

```bash
sudo nmap -sZ 192.0.2.10
```

## 6.14 SSDP and LIST scan

### SSDP scan

Simple Service Discovery Protocol (SSDP) is associated with UPnP discovery. The module discusses checking UDP-based UPnP/SSDP behavior and using M-SEARCH-style discovery.

### LIST scan

A list scan resolves hosts without actively probing them for liveness. In Nmap the concept is:

```bash
nmap -sL 192.0.2.0/24
```

This is useful for checking what names/addresses Nmap would enumerate before performing active host discovery.

## 6.15 IPv6 scanning

IPv6 expands the address space enormously, which changes scanning assumptions.

The module presents Nmap IPv6 support and the `-6` option.

```bash
sudo nmap -6 -sS <IPv6-target>
```

IPv6 discovery frequently relies on different mechanisms and local knowledge because brute-forcing the entire IPv6 space is impractical.

---

# 7. Service and Version Discovery

Port state alone is not enough. A tester wants to know **what is behind the port**.

## 7.1 Why service/version detection matters

A service may be:

- old or unsupported,
- misconfigured,
- exposing unnecessary functionality,
- running with known vulnerabilities,
- using a weak protocol,
- or revealing excessive identification information.

Nmap:

```bash
nmap -sV 192.0.2.10
```

Aggressive service probes can be combined with other checks, but always keep scope and traffic volume in mind.

## 7.2 Version detection vs port scanning

Think of them as two layers:

```text
Port scan → Is something reachable/listening?
Version detection → What application/service appears to be there?
```

Example:

```text
22/tcp open  ssh
80/tcp open  http
443/tcp open https
```

With version detection:

```text
22/tcp open  ssh   <version hint>
80/tcp open  http  <server/version hint>
```

Version detection helps bridge scanning and later vulnerability analysis.

## 7.3 Nmap service detection mechanics

The source explains that Nmap uses service/version probes rather than simply relying on a single port number. It sends application/protocol probes, observes responses and matches them against known service fingerprints.

That distinction matters because:

> **Port 8080 does not automatically mean a single specific application.**

The port number is only a hint; protocol behavior and service responses are stronger evidence.

---

# 8. Reducing Nmap Scan Time

The module gives several optimization ideas.

## 8.1 Omit non-critical tests

Do not run a massive scan when only a small question needs answering.

Prefer:

```bash
nmap -sn 192.0.2.0/24
```

over an expensive all-in-one scan when the only goal is to find live hosts.

Similarly, scan a focused port set when appropriate:

```bash
nmap -sS -p 22,53,80,443,445,3389 192.0.2.10
```

## 8.2 Optimize timing

Nmap provides timing templates:

```bash
nmap -T3 192.0.2.10
nmap -T4 192.0.2.10
```

The source discusses balancing speed with reliability and the risk of higher aggressiveness on filtered or fragile networks.

## 8.3 Separate UDP from other scans

UDP scans can be slower and can distort the time budget of a broad scan. Consider running them separately when the assessment objective requires UDP.

## 8.4 Keep Nmap current

Version improvements can add probes, fingerprints, bug fixes and performance improvements.

## 8.5 Run scans concurrently when appropriate

Parallel execution can reduce total elapsed time, but too much concurrency may increase packet loss or burden the network. Use small, controlled groups in production-like environments.

## 8.6 Scan from a favorable network location

Distance, filtering, packet loss and routing can affect scan speed. A scanner placed near the target can sometimes obtain more stable results than one crossing several routed networks.

## 8.7 Increase available CPU/bandwidth carefully

Resource constraints can become a bottleneck. Faster hardware does not compensate for bad timing, aggressive packet loss or remote rate-limiting, so always validate the quality of results, not only elapsed time.

---

# 9. OS Discovery / Banner Grabbing / Fingerprinting

OS discovery attempts to infer the operating system from network-stack behavior.

## 9.1 Banner grabbing

A banner can disclose:

- server type,
- operating-system family,
- application version,
- protocol details,
- technology choices.

Two broad categories are presented:

### Active banner grabbing
The tester connects or sends crafted probes and analyzes the direct response.

### Passive banner grabbing
The tester observes existing traffic rather than directly probing the target.

## 9.2 Active fingerprinting

The module explains that TCP/IP stacks can behave differently depending on implementation details. Nmap can send multiple carefully chosen probes and compare responses to a fingerprint database.

The source describes a series of tests that vary TCP flags, window behavior and other characteristics. The overall principle is:

```text
Known probe → target response → fingerprint features → compare against database → OS guess
```

## 9.3 Passive fingerprinting

Passive methods analyze packets already seen on the network.

Potential clues include:

- TTL.
- TCP window size.
- DF (Don't Fragment) behavior.
- TOS/DSCP-related fields.
- IPID patterns.
- TCP option ordering.
- initial sequence behavior.

The source emphasizes that passive techniques avoid generating new probes, but accuracy depends on traffic quality and fingerprint database coverage.

## 9.4 TTL as an OS clue

Different operating-system families often choose different default initial TTL values. A packet observed with a TTL of 64 may be compatible with one family, while 128 is commonly associated with another.

However, the observed TTL decreases as the packet crosses routers. Therefore, the observed value is not necessarily the original value.

A simplistic model is:

```text
Estimated original TTL ≥ observed TTL
```

Do not treat TTL alone as definitive OS identification.

## 9.5 TCP window size

TCP window sizes and related behavior can provide additional fingerprint clues. The module includes a table of example TTL/window characteristics for several OS families.

Use these as **fingerprinting clues**, not absolute truth.

## 9.6 Wireshark for OS clues

The source shows Wireshark being used to inspect packet fields such as TTL and TCP window size.

A practical lab workflow:

```text
1. Capture traffic from your own test VM.
2. Locate an ICMP or TCP packet.
3. Inspect the IP TTL.
4. Inspect TCP window/option fields where present.
5. Compare several packets rather than one packet.
6. Form a tentative OS hypothesis.
```

## 9.7 Unicornscan

The source demonstrates OS discovery by observing TTL-related values with Unicornscan.

The study takeaway is that OS fingerprinting can be performed by multiple tools and multiple evidence sources.

## 9.8 Nmap Script Engine (NSE)

NSE automates tasks using scripts.

The source shows NSE being used for OS discovery and examples involving SMB-related discovery on Windows-like systems.

General syntax:

```bash
nmap --script <script-name> 192.0.2.10
```

Always verify the exact script available in your installed Nmap version with:

```bash
nmap --script-help "*"
```

## 9.9 IPv6 fingerprinting

The source describes IPv6-specific probing such as:

- sequence-generation probes,
- ICMPv6 echo probes,
- ICMPv6 node-information queries,
- neighbor solicitation,
- UDP behavior,
- TCP congestion-notification behavior.

Nmap example:

```bash
sudo nmap -6 -O <IPv6-target>
```

---

# 10. Automated Network Scanning with Shell Scripts and AI

The module includes several pages demonstrating AI-assisted use of scanning commands. The key educational idea is **automation and command orchestration**, not blind trust in AI output.

## 10.1 Example automation pattern

A controlled host-discovery → port scan → service/version pipeline can look like:

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_RANGE="192.0.2.0/24"

nmap -sn "$TARGET_RANGE" -oG live_hosts.gnmap
awk '/Up$/{print $2}' live_hosts.gnmap > live_hosts.txt

while read -r host; do
  [ -n "$host" ] || continue
  nmap -sS -sV --top-ports 100 "$host" -oN "scan_${host}.txt"
done < live_hosts.txt
```

The source contains a similar pattern: discover live hosts, extract their IPs, then feed that list into a second Nmap phase for ports, services and versions.

## 10.2 AI-assisted command generation

The module shows prompts such as asking an AI assistant to:

- find open ports,
- perform a stealth scan,
- perform XMAS scanning,
- process a list of targets,
- perform version discovery,
- run NSE scripts,
- build a shell script.

### Best practice

Treat AI as a **command-generation assistant**, not as an authorization layer or a source of truth. Review:

- target scope,
- scan intensity,
- port selection,
- output handling,
- legality/authorization,
- potential side effects.

---

# 11. Scanning Beyond IDS and Firewalls

The source dedicates a full objective to techniques intended to make scanning harder for security controls to identify or interpret.

The topics include:

- packet fragmentation,
- source routing,
- source-port manipulation,
- IP address decoys,
- IP address spoofing,
- MAC address spoofing,
- custom packets,
- randomized host order,
- malformed/bad checksums,
- proxy servers,
- anonymizers.

These are important to understand for defensive testing even when a real assessment should use a controlled and approved methodology.

---

# 12. Packet Fragmentation

Packet fragmentation splits one logical packet into smaller IP fragments.

The module describes how fragmented probes can complicate simplistic IDS/firewall inspection because a control may need to reconstruct fragments before it can reliably apply a rule.

Nmap has historically supported fragmentation with an option such as:

```bash
sudo nmap -f 192.0.2.10
```

Use only in a lab when studying parser/filter behavior.

### Defensive idea

Modern security devices should normalize/reassemble traffic when appropriate rather than assume that each fragment can be inspected independently.

---

# 13. Source Routing

Source routing allows the sender to influence the route a packet takes.

The module explains that source-routing information can be embedded in IP options and that intermediate devices inspect those options to determine the next hop.

Historically, attackers could try to use source routing to steer traffic around security controls.

### Defensive lesson

Disable or tightly control source routing unless it is explicitly required. Network infrastructure should not blindly trust attacker-selected paths.

---

# 14. Source Port Manipulation

Some filters historically allowed traffic from certain source ports, assuming that a packet from a trusted service port was legitimate.

A scanner can deliberately choose a source port to test whether filtering rules are based on the source port rather than the actual protocol/session context.

Nmap syntax:

```bash
sudo nmap --source-port 53 192.0.2.10
```

The defensive lesson is straightforward:

> **Firewall decisions should not rely on easily forged source-port values.**

---

# 15. IP Address Decoys

Decoys cause a target to see traffic associated with several source addresses so that the real scanner is harder to isolate from the packet stream.

Nmap conceptually supports decoys with `-D`.

Lab example:

```bash
sudo nmap -sS -D 192.0.2.20,192.0.2.21,ME 192.0.2.10
```

Use only inside an isolated environment because decoy traffic can affect other hosts and security logs.

---

# 16. IP Address Spoofing

IP spoofing changes the apparent source address of a packet.

The source uses spoofing to illustrate how an IDS/firewall that trusts IP identity can be deceived.

Important TCP limitation:

> Spoofing a source address does not magically give the attacker a working two-way TCP session.

The reason is simple: replies are sent toward the spoofed source, not the scanner.

The module also demonstrates Hping3-style spoofing syntax, but this should be reproduced only in a closed lab.

---

# 17. MAC Address Spoofing

A MAC address is the link-layer identity used within local Ethernet-style networks.

The source discusses modifying a scanner's MAC identity to resemble a trusted vendor/device.

Nmap supports `--spoof-mac` conceptually:

```bash
sudo nmap --spoof-mac 00:11:22:33:44:55 192.0.2.10
```

In practice, applicability is limited to scenarios where the traffic is actually being transmitted on a compatible local link and the network controls inspect source MAC information.

---

# 18. Creating Custom Packets

The module introduces packet-crafting tools such as Colasoft Packet Builder.

The goal is to demonstrate that a tester can construct packets by controlling fields at multiple layers, including:

- Ethernet fields,
- IP fields,
- TCP/UDP fields,
- payload bytes,
- checksums,
- flags and options.

A packet-building application can expose multiple representations such as a structured field view and hexadecimal payload view.

The defensive takeaway is that security controls must validate packet structure, not merely assume that a packet is trustworthy because a single field looks normal.

---

# 19. Randomizing Host Order

Large scans may normally visit hosts in predictable order. Randomizing host order can make scanning patterns less obvious to simple monitors.

The source demonstrates Nmap's random-host-order behavior.

Example:

```bash
nmap --randomize-hosts 192.0.2.0/24
```

The defensive implication is to detect **behavior and volume over time**, rather than relying only on sequential address order.

---

# 20. Bad / Invalid Checksums

The source discusses deliberately sending packets with invalid TCP/UDP checksums.

Why would this matter?

- Some systems or intermediate devices may treat malformed packets differently.
- Certain filtering controls may drop them early.
- Comparing responses can reveal how traffic is handled.

Nmap support is exposed through an option such as:

```bash
sudo nmap --badsum 192.0.2.10
```

Use this strictly as a lab experiment.

---

# 21. Proxy Servers

A proxy can act as an intermediary between the scanner and the target.

Conceptual flow:

```text
Scanner → Proxy → Target
```

The target sees the proxy's connection rather than the original client in many ordinary proxy designs.

The source discusses proxy use for:

- routing traffic through an intermediary,
- masking the original source from the target,
- accessing content through another network path,
- chaining multiple proxy servers.

## 21.1 Proxy chaining

```text
Scanner → Proxy 1 → Proxy 2 → Proxy 3 → Target
```

Each hop adds another layer between the scanner and the target, but also increases complexity, latency and potential points of failure.

## 21.2 Proxy tools mentioned

The module discusses tools such as:

- Proxy Switcher.
- Proxy-related anonymization services.
- Burp Suite.
- Tor.
- Privoxy/related proxy tools.

---

# 22. Anonymizers and Privacy Networks

The module covers anonymizers as intermediary systems intended to conceal the origin of web/network requests.

## 22.1 Why anonymizers are used

The curriculum discusses motivations such as:

- privacy,
- reducing direct exposure of the client address,
- bypassing some network restrictions,
- intermediary routing.

These tools can be abused, but they also have legitimate privacy and research use.

## 22.2 Networked vs single-point anonymizers

### Networked anonymizer
Traffic crosses multiple intermediary nodes.

**Advantage:** traffic analysis can be more difficult.

**Disadvantage:** every additional node introduces trust and performance considerations.

### Single-point anonymizer
Traffic is routed through one intermediary.

**Advantage:** simpler architecture.

**Disadvantage:** the intermediary becomes a major trust and correlation point.

## 22.3 Examples in the source

The module names or illustrates:

- Whonix.
- Tails.
- AstillVPN/AstrillVPN.
- CyberGhost VPN.
- Tor.
- ProxySwitcher.
- additional anonymizer/proxy products.

The important exam concept is not memorizing every product but understanding **intermediary routing, identity masking and the tradeoff between privacy and trust**.

---

# 23. Network Scanning Countermeasures

The final objective shifts perspective from attacker methodology to defense.

The correct mindset is:

```text
What information does a scanner need?
            ↓
Which packets reveal it?
            ↓
Can we reduce unnecessary exposure?
            ↓
Can we detect abnormal probing?
            ↓
Can we stop or rate-limit it safely?
```

---

# 24. Ping Sweep Countermeasures

The module recommends defensive measures including:

- Filtering unwanted ICMP echo requests.
- Using IDS/IPS to detect unusual discovery activity.
- Reviewing the type and volume of ICMP traffic.
- Limiting ICMP behavior when it is not operationally necessary.
- Using access-control lists to constrain reachability.
- Segmenting networks.
- Using private addressing where appropriate.
- Monitoring for sweep-like traffic patterns.

### Important nuance

Completely blocking ICMP everywhere can break legitimate operations such as diagnostics, path-MTU discovery and troubleshooting. Filtering should be deliberate rather than indiscriminate.

---

# 25. Port-Scanning Countermeasures

The source recommends a layered approach:

## 25.1 Minimize exposed ports

Keep only genuinely required ports reachable.

```text
Better:
Internet → firewall → only required service(s)

Worse:
Internet → dozens of unnecessary listening services
```

## 25.2 Firewall + IDS/IPS

Use perimeter and host-level controls to detect scan patterns and block clearly unwanted sources.

## 25.3 Maintain current rules and software

Security controls themselves must be patched and their rules reviewed.

## 25.4 Detect scan behavior

Look for:

- many destination ports in a short window,
- sequential port access,
- repeated SYN probes,
- unusual UDP probing,
- source-address anomalies,
- fragmented or malformed probes.

## 25.5 Block or rate-limit obvious scanner behavior

Rate limiting can reduce the effectiveness of noisy scanning, but must be balanced against legitimate distributed clients.

## 25.6 Use decoy/empty hosts carefully

The source mentions making scanning more time-consuming by presenting ports that do not correspond to real services, such as carefully controlled honeypots/honeynets.

## 25.7 Network segmentation

Separate sensitive assets so that a scan against one segment does not automatically reveal every system in the environment.

## 25.8 Keep service exposure narrow

The module also emphasizes avoiding unnecessary open ports, limiting access to administrative services and blocking unnecessary protocol responses.

---

# 26. Banner-Grabbing Countermeasures

Banner grabbing becomes dangerous when it reveals too much technology detail.

The source recommends approaches such as:

- disable or change verbose banners,
- remove unnecessary product/version information,
- use server masking where appropriate,
- avoid revealing implementation-specific headers,
- reduce information leakage from HTTP responses,
- avoid unnecessary file-extension clues.

## 26.1 HTTP/server-header hardening

The source includes examples such as changing web-server signatures and hiding implementation information.

Generic example of the principle:

```text
Do not expose:
Server: ExampleProduct/12.3.4

Prefer a minimal, policy-approved response header.
```

Exact hardening syntax depends on the web server and version.

## 26.2 Hide application/file-extension clues

The source notes that extensions such as `.asp`, `.php` and similar mappings can disclose implementation technologies.

A defensive strategy is to:

- avoid unnecessary technology-revealing URLs,
- use routing/rewriting where justified,
- limit directory and server metadata disclosure,
- use HTTPS and secure headers.

---

# 27. Detecting IP Spoofing

The source covers three major detection ideas.

## 27.1 Direct TTL probes

Send a probe that is likely to trigger a reply and compare the response TTL with the expected behavior.

Conceptual method:

```text
Known/expected traffic pattern
        ↓
Observe response TTL
        ↓
Compare with suspected source behavior
        ↓
Flag inconsistency
```

## 27.2 IP Identification Number (IPID)

Some systems historically incremented IPID values in predictable patterns. Monitoring those values can sometimes reveal that traffic is not originating from the claimed host.

The source emphasizes that the technique is more useful when the suspected and observing systems are in the same or compatible network context.

## 27.3 TCP flow-control method

The module describes comparing TCP flow-control behavior, especially changes in the advertised receive window. Unexpected continuation patterns can provide clues about forged versus genuine traffic under certain conditions.

These fingerprinting methods are heuristics, not universal proof.

---

# 28. IP Spoofing Countermeasures

The source presents a broad defense stack.

## 28.1 Avoid trusting source addresses alone

Do not assume that an IP address proves identity.

Use stronger authentication where practical.

## 28.2 Firewalls and filtering

Apply ingress filtering so packets claiming impossible or unauthorized source ranges are discarded near the edge.

## 28.3 Egress filtering

Prevent internal hosts from sending packets with source addresses that should not belong to them.

This helps reduce spoofing from inside and limits abuse of compromised systems.

## 28.4 Random initial TCP sequence numbers

Predictable TCP sequence values historically enabled certain spoofing attacks. Modern TCP stacks should use robust sequence-number generation.

## 28.5 Encryption and authentication

Use protocols that provide cryptographic integrity/authentication instead of trusting only source IP metadata.

Examples:

- TLS-based application protocols.
- SSH.
- VPN technologies.
- authenticated services.

## 28.6 SYN-flood protections

The module associates spoofing resilience with SYN-flood defenses because spoofed TCP handshakes can be used to exhaust connection state.

## 28.7 Additional controls

The source also mentions:

- IPv6 migration in some security designs.
- digital certificate authentication.
- secure VPNs.
- application-specific packet inspection.
- DHCP snooping-related controls.
- network address translation.

---

# 29. Scanning Detection and Prevention Tools

The module closes with examples of monitoring/detection platforms.

## ExtraHop

The source presents ExtraHop as a platform for real-time network visibility and detection, including service discovery, anomaly detection and traffic analysis.

## Other tools named

- Splunk Enterprise Security.
- Scanlogd.
- Vectra Detect.
- IBM Security QRadar XDR.
- Cynet 360 AutoXDR.

The category to remember is more important than the vendor list:

```text
Visibility → Detection → Correlation → Alerting → Response
```

---

# 30. High-Value CEH Exam Comparisons

## TCP Connect vs SYN scan

| Feature | TCP Connect (`-sT`) | SYN (`-sS`) |
|---|---|---|
| Completes TCP handshake | Yes | No |
| Requires raw-packet privileges | Usually no | Often yes |
| Noise/logging | Higher | Usually lower |
| Reliability | High | High |
| Core idea | Full connection | Half-open probe |

## SYN vs ACK scan

| Feature | SYN scan | ACK scan |
|---|---|---|
| Primary question | Is port likely open? | Is port filtered/unfiltered? |
| Flag | SYN | ACK |
| Typical result | open/closed/filtered | filtered/unfiltered |

## ICMP echo vs TCP SYN ping

| Feature | ICMP echo | TCP SYN ping |
|---|---|---|
| Protocol | ICMP | TCP |
| Useful when | ICMP allowed | ICMP blocked but TCP reachable |
| Common command | `ping`, `nmap -PE` | `nmap -PS` |

## Active vs passive fingerprinting

| Feature | Active | Passive |
|---|---|---|
| Sends probes | Yes | No |
| Detectability | Higher | Lower |
| Data source | Target replies | Existing traffic |
| Main challenge | Noise | Need enough traffic |

## Port scan vs service/version scan

```text
Port scan       = Which ports are reachable?
Service scan    = What service/application is there?
Version scan    = Which version does it appear to be?
OS scan         = Which OS/network stack is likely?
```

---

# 31. A Practical Authorized-Lab Workflow

This workflow turns the module into a repeatable exercise.

## Phase A — Scope

```text
Target: 192.0.2.10
Network: isolated VM/CTF lab
Authorization: explicit
```

## Phase B — Host discovery

```bash
nmap -sn 192.0.2.10
sudo nmap -PS22,80,443 192.0.2.10
sudo nmap -PA80,443 192.0.2.10
```

## Phase C — Port discovery

```bash
sudo nmap -sS -p 1-1000 192.0.2.10
sudo nmap -sU --top-ports 50 192.0.2.10
```

## Phase D — Service/version discovery

```bash
nmap -sV 192.0.2.10
```

## Phase E — OS discovery

```bash
sudo nmap -O 192.0.2.10
```

## Phase F — Focused NSE validation

```bash
nmap --script default 192.0.2.10
```

Use targeted scripts in real assessments instead of blindly running every script.

## Phase G — Packet analysis

Capture your own lab traffic with Wireshark and compare:

- SYN/SYN-ACK/RST behavior.
- TTL.
- TCP window.
- TCP flags.
- ICMP responses.
- Retransmission behavior.

## Phase H — Document

Record:

```text
Host
↓
Reachability
↓
Open ports
↓
Detected services
↓
Versions
↓
OS hypothesis
↓
Filtering behavior
↓
Potential weaknesses
↓
Next validation step
```

---

# 32. Suggested Practice Matrix

| Topic | Tool | Practice target | Expected learning |
|---|---|---|---|
| ICMP discovery | ping/Nmap | own VM | reachability |
| ARP discovery | Nmap | local subnet | local-host discovery |
| SYN scan | Nmap | lab VM | TCP state inference |
| Connect scan | Nmap | lab VM | full handshake |
| UDP scan | Nmap | DNS/SNMP lab | UDP response interpretation |
| ACK scan | Nmap | lab VM/firewall lab | filtering behavior |
| XMAS/FIN/NULL | Nmap | vulnerable lab VM | flag-based scanning |
| SCTP scan | Nmap | SCTP-enabled lab | non-TCP/non-UDP discovery |
| Version detection | Nmap | local services | service identification |
| OS discovery | Nmap/Wireshark | two VMs | fingerprinting |
| NSE | Nmap | Windows/Samba lab | scripted discovery |
| Packet inspection | Wireshark | your own traffic | field-level analysis |
| IDS detection | Snort/Suricata lab | isolated network | defensive visibility |
| Proxy routing | Burp/Tor/HTTP proxy | local test service | intermediary routing |

---

# 33. Common Mistakes

## Mistake 1 — "No response means host is down."

False. Filtering, rate limiting, asymmetric routing and protocol behavior can all produce silence.

## Mistake 2 — "Port number equals application."

False. A service can run on a non-default port.

## Mistake 3 — "ACK scan finds open ports directly."

Not primarily. ACK scanning is mainly about understanding filtering state.

## Mistake 4 — "UDP scanning is identical to TCP scanning."

False. UDP has no TCP-like handshake.

## Mistake 5 — "TTL proves the operating system."

False. TTL is one clue among several and changes during routing.

## Mistake 6 — "A stealth scan is invisible."

False. "Stealth" is relative. Network telemetry, IDS/IPS, endpoint logs and packet capture can still expose it.

## Mistake 7 — "Spoofing gives you a normal TCP connection."

Usually not. Two-way return traffic goes to the spoofed source unless the attacker can observe or influence that path.

## Mistake 8 — "AI-generated scan commands are automatically safe."

False. AI can generate commands that are overly broad, noisy or inappropriate. Human scope review is mandatory.

---

# 34. CEH Memory Map

```text
SCANNING NETWORKS
│
├── Fundamentals
│   ├── Why scan?
│   ├── Types of scans
│   └── TCP flags / handshake
│
├── Host Discovery
│   ├── ARP
│   ├── UDP
│   ├── ICMP Echo
│   ├── ICMP Timestamp
│   ├── ICMP Address Mask
│   ├── TCP SYN
│   ├── TCP ACK
│   └── IP protocol
│
├── Port / Service Discovery
│   ├── Connect
│   ├── SYN
│   ├── NULL
│   ├── FIN
│   ├── XMAS
│   ├── Maimon
│   ├── ACK
│   ├── Idle/IPID
│   ├── UDP
│   ├── SCTP INIT
│   ├── SCTP COOKIE-ECHO
│   ├── SSDP
│   ├── LIST
│   └── IPv6
│
├── Service / OS Discovery
│   ├── Service versions
│   ├── Active fingerprinting
│   ├── Passive fingerprinting
│   ├── TTL
│   ├── TCP windows
│   ├── Wireshark
│   ├── Unicornscan
│   ├── Nmap NSE
│   └── IPv6 fingerprinting
│
├── IDS / Firewall Evasion Concepts
│   ├── Fragmentation
│   ├── Source routing
│   ├── Source port manipulation
│   ├── Decoys
│   ├── IP spoofing
│   ├── MAC spoofing
│   ├── Custom packets
│   ├── Random host order
│   ├── Bad checksums
│   ├── Proxies
│   └── Anonymizers
│
└── Countermeasures
    ├── Ping sweep defense
    ├── Port-scan defense
    ├── Banner hardening
    ├── IP spoofing detection
    ├── Ingress / egress filtering
    ├── Strong authentication
    ├── Encryption
    ├── SYN-flood protections
    ├── Segmentation / ACLs
    └── IDS / IPS / SIEM / NDR
```

---

# 35. Exam-Oriented Command Sheet

> Commands below are examples for authorized lab targets. Replace the placeholder target with your own isolated VM/IP.

```bash
# Basic host discovery
nmap -sn 192.0.2.10

# ARP discovery on local network
sudo nmap -PR 192.0.2.0/24

# ICMP Echo
sudo nmap -PE 192.0.2.10

# ICMP timestamp
sudo nmap -PP 192.0.2.10

# ICMP address mask
sudo nmap -PM 192.0.2.10

# TCP SYN ping
sudo nmap -PS80,443 192.0.2.10

# TCP ACK ping
sudo nmap -PA80,443 192.0.2.10

# IP protocol ping
sudo nmap -PO1,6,17 192.0.2.10

# TCP connect scan
nmap -sT 192.0.2.10

# SYN scan
sudo nmap -sS 192.0.2.10

# FIN scan
sudo nmap -sF 192.0.2.10

# NULL scan
sudo nmap -sN 192.0.2.10

# XMAS scan
sudo nmap -sX 192.0.2.10

# Maimon scan
sudo nmap -sM 192.0.2.10

# ACK scan
sudo nmap -sA 192.0.2.10

# UDP scan
sudo nmap -sU 192.0.2.10

# SCTP INIT
sudo nmap -sY 192.0.2.10

# SCTP COOKIE-ECHO
sudo nmap -sZ 192.0.2.10

# Service/version detection
nmap -sV 192.0.2.10

# OS detection
sudo nmap -O 192.0.2.10

# Aggressive profile for a lab
sudo nmap -A 192.0.2.10

# List scan
nmap -sL 192.0.2.0/24

# IPv6 scan
sudo nmap -6 -sS <IPv6-target>

# Randomize host order
nmap --randomize-hosts 192.0.2.0/24

# Source-port test (lab)
sudo nmap --source-port 53 192.0.2.10

# Fragmentation test (lab)
sudo nmap -f 192.0.2.10

# Bad checksum test (lab)
sudo nmap --badsum 192.0.2.10

# Decoy test (isolated lab)
sudo nmap -D 192.0.2.20,192.0.2.21,ME 192.0.2.10

# MAC spoofing test (local lab only)
sudo nmap --spoof-mac 00:11:22:33:44:55 192.0.2.10
```

---

# 36. What to Memorize vs What to Understand

## Memorize

- TCP flag meanings.
- Three-way handshake.
- Major Nmap scan flags.
- Core host-discovery options.
- Common ports/services.
- Differences among SYN, Connect, ACK, FIN, NULL and XMAS scans.
- UDP scan response logic.
- Main OS-fingerprint clues.
- Main IDS/firewall evasion concepts.
- Main countermeasures.

## Understand

- Why a scanner receives RST vs SYN/ACK.
- Why UDP is slower and ambiguous.
- Why ACK scans identify filtering behavior.
- Why TTL is only a clue.
- Why spoofed TCP traffic is difficult to complete as a normal session.
- Why fragmented traffic can challenge poorly designed filters.
- Why randomizing scan order can affect basic detection.
- Why defense needs both prevention and visibility.

---

# 37. Source Traceability

The notes are organized from the uploaded 144-page module. Major section ranges in the source include:

| Source pages | Topic represented |
|---|---|
| 3–21 | Learning objectives, scanning concepts, TCP flags, Nmap/Hping3/Metasploit/tools |
| 22–39 | Host discovery techniques |
| 40–78 | Port/service discovery and Nmap scan types |
| 79–99 | OS discovery, fingerprinting, service/version detection and automation |
| 100–129 | Scanning beyond IDS/firewalls, proxies and anonymizers |
| 130–143 | Countermeasures, spoofing detection/defense and monitoring tools |
| 144 | Closing page |

The original module explicitly presents the six objectives above and uses diagrams/screenshots throughout to illustrate packet flows, scan outputs, fingerprinting and countermeasures.

---

# 38. Final Takeaway

The whole module can be reduced to one mental model:

```text
Discover the host
      ↓
Understand how it responds
      ↓
Find reachable ports
      ↓
Identify services and versions
      ↓
Infer the OS and filtering behavior
      ↓
Assess exposure
      ↓
Understand how controls may detect/block scanning
      ↓
Design countermeasures and monitor for scanning
```

Scanning is not just "run Nmap." The real skill is learning how to interpret packet behavior, choose the right probe for the question, minimize unnecessary traffic, correlate results, and turn raw network responses into a defensible assessment.

---

## Disclaimer

This repository is an independent study aid created from the user-provided CEH v13 Module 03 source. It is **not an official EC-Council publication** and does not replace the official courseware, labs or exam objectives. Commands are included for authorized educational testing only.
