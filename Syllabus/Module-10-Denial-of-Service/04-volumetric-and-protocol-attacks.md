# 04 — Volumetric and Protocol Attacks

> Exam objective: *Demonstrate different DoS/DDoS attack techniques*

## 4.1 The Three Basic Categories of DoS/DDoS Attack Vectors

DDoS attacks mainly aim to diminish network, application, or service resources, restricting
legitimate users from access. All named attack techniques fall into one of three categories:

| Category | What it exhausts | Measured in | Covered in |
|---|---|---|---|
| **Volumetric Attacks** | Bandwidth — within the target network/service, or between it and the rest of the Internet | bits per second (**bps**) | This file (§4.2) |
| **Protocol Attacks** | Connection-state tables in infrastructure like load balancers, firewalls, application servers | packets per second (**pps**) | This file (§4.3) |
| **Application-Layer Attacks** | The resources/services of the application itself | requests per second (**rps**) | [`05-application-layer-and-advanced-attacks.md`](05-application-layer-and-advanced-attacks.md) |

Volumetric attacks in particular tend to target inherently stateless protocols without built-in
congestion avoidance — NTP, DNS, and SSDP are classic targets, because a flood of packets against
them can consume an entire network's bandwidth almost by accident. A single machine usually can't
generate enough traffic to overwhelm real network equipment, which is exactly why attackers
recruit botnets: many geographically distributed machines combine their processing power to
generate huge traffic volumes — hence "distributed" in DDoS.

---

## 4.2 Volumetric Attacks

### Two Types of Bandwidth Depletion

| Type | Mechanism |
|---|---|
| **Flood attack** | Zombies send large volumes of traffic directly to the victim to exhaust its bandwidth |
| **Amplification attack** | The attacker/zombies send messages to a broadcast IP address; every host on that broadcast network replies, *amplifying* the traffic that lands on the victim |

### UDP Flood Attack

The attacker sends **spoofed UDP packets** at a very high rate to random ports on the target,
using a large, spoofed source-IP range. Because UDP is connectionless, the target has no choice
but to check each port for a listening application. Since most of the targeted ports have
nothing listening, the target replies with an **ICMP "Destination Unreachable"** packet for each
one — consuming CPU and bandwidth generating all those error replies, until the network goes
offline. Legitimate applications on the box become unreachable in the process.

```
Attacker ──UDP packets (spoofed IP, random dest. ports)──▶ Target Server
Target Server ──ICMP "Destination Unreachable" (per packet)──▶ (nowhere useful — the source was spoofed)
```

### ICMP Flood Attack

Network admins normally use ICMP for IP operations, troubleshooting, and error messaging on
undeliverable packets. In an ICMP flood, attackers send large volumes of **ICMP ECHO request**
packets to a victim — directly, or through reflection networks — each one signalling the victim
to reply. The combined inbound request traffic plus outbound reply traffic saturates the victim's
network connection, eventually causing it to stop responding to legitimate TCP/IP traffic
altogether.

**Countermeasure:** configure a **threshold limit** that triggers ICMP flood protection once
exceeded — by default, many platforms use 1000 packets/second. Once the threshold is hit, the
router rejects further ICMP echo requests from *all* addresses in that security zone for the
remainder of the current second and the next second.

### Ping of Death (PoD) Attack

The attacker tries to crash, destabilize, or freeze the target by sending **malformed or
oversized packets** using a simple ping command. RFC 791 caps a valid IP packet at **65,535
bytes**; a PoD attack sends a packet just over that limit (e.g., 65,538 bytes — 20-byte IP
header + 8-byte ICMP header + 65,510 bytes of ICMP data), and the reassembly process on the
receiving system can crash trying to handle it. The attacker's identity can easily be spoofed,
and no special knowledge of the target beyond its IP address is required.

### Smurf Attack

The attacker spoofs the source IP with the **victim's** IP address, then sends a large number of
**ICMP ECHO request** packets to an **IP broadcast network**. Every host on that broadcast
network replies — but because the source address was spoofed, all of those replies land on the
victim instead of the attacker, generating a flood of traffic that can crash the victim's machine.

### Pulse Wave DDoS Attack

Unlike a continuous flood, pulse wave attacks use a **periodic** attack pattern: a highly
repetitive burst ("pulse") of packets is sent every ~10 minutes, with the overall attack session
lasting anywhere from about an hour to several days. A single pulse can exceed **300 Gbps** — more
than enough to saturate most network pipes. Because the attack repeatedly ramps up and backs off,
recovery is very difficult, and sometimes effectively impossible while the campaign is ongoing.

### Zero-Day DDoS Attack

A **zero-day DDoS attack** exploits a DDoS-related vulnerability for which no patch or effective
defense yet exists. Until the victim identifies the threat actor's strategy and a patch is
developed, the attacker can freely block resources and even steal data. There is currently no
universally reliable way to protect a network against an attack of this class in advance — by
definition, nobody knew about it yet.

### NTP Amplification Attack

The **Network Time Protocol (NTP)** synchronizes time across hosts, processes, and devices on a
network. In an NTP amplification attack:

1. The attacker (via a botnet) sends large UDP packets to an NTP server, **spoofing the source IP**
   to be the victim's real IP address.
2. This is typically done against NTP servers that have the **`monlist`** command enabled — a
   legacy diagnostic command that returns a list of the last several hundred clients that talked
   to the server.
3. Each spoofed UDP packet triggers a `monlist` request, which produces a **disproportionately
   large response packet**.
4. The NTP server sends that large response immediately to the spoofed (victim) address.
5. The victim's IP is flooded with large responses from potentially many NTP servers at once,
   exhausting bandwidth, memory, and processing power — a full denial of service.

**Detecting exposed `monlist`-enabled NTP servers (authorized/lab use only):**
```bash
nmap -sU -pU:123 -Pn -n --script=ntp-monlist <target>
```
Example output on a vulnerable server:
```
PORT    STATE SERVICE
123/udp open  ntp
| ntp-monlist:
|   ... list of recent clients that talked to this NTP server ...
```
If this script returns a client list, the target NTP server is running with `monlist` enabled and
could be abused as an amplifier.

**Countermeasures for NTP amplification:**
- Secure and harden NTP server configurations to disable/restrict `monlist`.
- Limit flow control on the NTP server.
- Frequently monitor the network for abnormal traffic.
- Implement a zero-trust network model.
- Use firewalls to filter/rate-limit NTP server requests.

---

## 4.3 Protocol Attacks

Protocol attacks exhaust resources *other* than raw bandwidth — specifically the connection-state
tables in devices like load balancers, firewalls, and application servers. Because the device
waits for existing connections to close or expire, no new connections can be accepted once the
table fills, even though bandwidth usage might look perfectly normal. Magnitude is measured in
packets per second (pps) or connections per second (cps), and these attacks can overwhelm even
high-capacity devices tracking millions of simultaneous connections.

### SYN Flood Attack

Recall the normal TCP three-way handshake:
```
Client                                   Server
  │────────────── SYN ────────────────────▶│
  │◀───────────── SYN/ACK ─────────────────│
  │────────────── ACK ─────────────────────▶│
  (connection established)
```

In a SYN flood, the attacker sends a large number of SYN requests with **fake/spoofed source IP
addresses**. The target replies with SYN/ACK as normal and waits for the final ACK — which never
arrives, because the source address was fake. Each half-open connection sits in the server's
**"SYN RECEIVED" listen queue for at least ~75 seconds** by default on many hosts. Since the
queue has limited size, flooding it with fake SYNs quickly exhausts the queue, and the server
stops accepting new — including legitimate — connections until stale entries time out.

```
Host A (Attacker)                       Host B (Victim)
  │── SYN ──────────────────────────────▶│   (normal handshake, once)
  │◀─ SYN/ACK ────────────────────────────│
  │── ACK ───────────────────────────────▶│
  │
  │── SYN (spoofed src #1) ──────────────▶│  ┐
  │── SYN (spoofed src #2) ──────────────▶│  │  SYN flood — no ACKs ever arrive
  │── SYN (spoofed src #3) ──────────────▶│  │  listen queue fills up
  │── SYN (spoofed src #4) ──────────────▶│  ┘
```

An attacker can fill a connection table even *without* spoofing, simply by never sending the
final ACK — but spoofing makes the attack far harder to trace and block by source IP.

**Countermeasures:**
- Proper packet filtering is a viable first line of defense.
- Tune the TCP/IP stack to reduce SYN-flood impact while still allowing legitimate traffic
  through.
- Deploy **SYN cookies** and **SynAttackProtect** — both let the server avoid committing real
  resources to a connection until the handshake is confirmed legitimate.
- Decrease the SYN-RECEIVED timeout period so half-open connections expire faster.
- Decrease the number of, or entirely disable, SYN/ACK retransmissions.

```bash
# Linux — enable SYN cookies (kernel-level SYN-flood mitigation)
sudo sysctl -w net.ipv4.tcp_syncookies=1
# Make persistent:
echo "net.ipv4.tcp_syncookies = 1" | sudo tee -a /etc/sysctl.conf

# Linux — reduce the SYN backlog timeout / retransmits to fail faster under flood
sudo sysctl -w net.ipv4.tcp_synack_retries=2
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# iptables — basic SYN flood rate-limit rule (lab/edge-router use)
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP
```

### SYN-ACK Flood Attack

A close cousin of the SYN flood: instead of exploiting the *first* stage of the handshake, the
attacker sends a large number of spoofed **SYN-ACK** packets directly to the target, exhausting
its resources as it tries to match each one to a session that was never actually opened.

### ACK and PUSH ACK Flood Attack

During an active TCP session, **ACK** and **PUSH ACK** flags carry ordinary data to and from
client and server until the session ends. In this attack, the attacker sends a large volume of
spoofed ACK/PUSH ACK packets to the target — since these appear to belong to existing sessions,
the target wastes resources trying to match them against its connection table, becoming
non-functional under the load.

### Fragmentation Attack

These attacks stop a victim from being able to **reassemble fragmented packets**, by flooding the
target with a large number of fragmented TCP or UDP packets (typically 1500+ bytes) sent at a
relatively modest packet rate. Because network protocols are *designed* to allow fragmentation,
these fragments usually pass uninspected through routers, firewalls, and IDS/IPS — but
reassembling and inspecting the large fragments at the destination consumes excessive CPU and
memory. Attackers make this worse by randomizing the actual content of each fragment, forcing the
reassembly/inspection process to work even harder — ultimately crashing the target.

```
 Original Packet:  [IP Header][Data seg 1][Data seg 2][Data seg 3][Data seg 4]
                          │         │           │           │           │
                          ▼         ▼           ▼           ▼           ▼
                     Fragment 1  Fragment 2  Fragment 3  Fragment 4
                    (each with its own IP header prepended)
```

### Spoofed Session Flood Attack

Attackers create **fake/spoofed TCP sessions** carrying combinations of SYN, ACK, and RST/FIN
packets specifically to slip past firewalls that key their detection on SYN-packet volume alone,
while still exhausting network resources.

| Variant | Mechanism |
|---|---|
| **Multiple SYN-ACK Spoofed Session Flood** | Fake session built from multiple SYN *and* multiple ACK packets, plus one or more RST/FIN packets |
| **Multiple ACK Spoofed Session Flood** | Fake session that **skips SYN packets entirely**, using only multiple ACK packets plus one or more RST/FIN packets — because most firewalls key DDoS detection on SYN volume, this variant frequently sails through undetected |

---

**Next:** [`05-application-layer-and-advanced-attacks.md`](05-application-layer-and-advanced-attacks.md) →