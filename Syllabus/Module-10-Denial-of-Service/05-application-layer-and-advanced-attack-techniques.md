# 05 — Application-Layer and Advanced Attack Techniques

> Exam objective: *Demonstrate different DoS/DDoS attack techniques*

## 5.1 Application-Layer Attacks — Overview

In application-layer (Layer-7) attacks, the attacker exploits vulnerabilities in the application
protocol or the application itself, rather than the network below it. Because these attacks target
unpatched or logically weak points in the application, they **don't require anywhere near as much
bandwidth** as volumetric or protocol attacks to succeed — a handful of attacking machines
producing a low, "boring-looking" traffic rate can be just as effective as a botnet, which also
makes them **very difficult to detect and mitigate**. The attack works by opening connections
and holding them open until the application can accept no new ones. Magnitude is measured in
requests per second (**rps**).

Several application-layer attacks exploit **software-level bugs directly**, such as buffer
overflows: sending excessive data to an application either crashes it outright, or forces the
oversized data to execute on the host system, occasionally letting the attacker run arbitrary
code by overwriting the data that controls program flow.

**What attackers accomplish with application-layer floods:**
- Flood web applications with what looks like legitimate user traffic
- Disrupt service to a specific system or person (e.g., locking an account via repeated invalid
  login attempts)
- Jam an application's database connection using maliciously crafted SQL queries

Because a connection genuinely gets established and the incoming traffic looks legitimate on the
surface, these attacks are hard to spot in real time — but for the same reason, once a victim
*does* identify the attack, it's often easier to trace back to its source than a volumetric flood.

## 5.2 HTTP GET/POST Attack

HTTP clients (browsers, scripts) connect to a web server and send **HTTP GET** or **HTTP POST**
requests. Attackers weaponize both:

| Variant | Mechanism |
|---|---|
| **HTTP GET attack** | The attacker uses a **time-delayed HTTP header** to hold a connection open indefinitely, exhausting the web server's available connection slots — the server just sits waiting for a header that never finishes arriving |
| **HTTP POST attack** | The attacker sends a request with **complete headers** but a deliberately **incomplete message body**, so the server keeps the connection open waiting for the rest of the body that never comes |

```
HTTP GET Attack:   Attacker ──"Request w/ time-delayed header"──▶ Server (waits forever for complete header)
HTTP POST Attack:  Attacker ──"Request w/ incomplete message body"──▶ Server (waits forever for the rest of the body)
```

This is a sophisticated Layer-7 attack that needs no malformed packets, IP spoofing, or
reflection — it forces the server to allocate as many resources as possible just to service the
"pending" request, denying legitimate users access.

### Additional HTTP Flood Variants
| Variant | Mechanism |
|---|---|
| **Single-Session HTTP Flood** | Exploits HTTP 1.1 keep-alive behavior to bombard a target with multiple requests inside a *single* HTTP session |
| **Single-Request HTTP Flood** | Conceals multiple HTTP requests within a *single* HTTP packet from a single session — lets the attacker stay anonymous and effectively invisible while flooding |
| **Recursive HTTP GET Flood** | The attacker (posing as a legitimate user browsing normally) requests a list of pages/images in sequence, appearing to "just browse" — while stealthily flooding the target; combined with a plain HTTP flood, this can cause extreme damage because it's very hard for a firewall to distinguish from genuine crawling behavior |
| **Random Recursive GET Flood** | A tweak of the recursive GET flood aimed at forums/blogs/paginated sites — the attacker requests random page numbers from within a valid range, again mimicking a real user paging through content, while bombarding the target with GET requests |

## 5.3 Slowloris Attack

**Slowloris** is a dedicated Layer-7 DDoS tool that takes down web infrastructure using
**perfectly legitimate HTTP traffic** — its defining characteristic versus most other tools. The
attacker sends **partial HTTP requests** to the target; the server dutifully opens a connection
and waits for each request to complete. Because the requests are never actually completed, the
server's maximum concurrent connection pool fills up, and it starts rejecting even legitimate
connection attempts.

```
Normal HTTP:      Client ──HTTP request────▶ Server ──HTTP response────▶ Client
Slowloris DDoS:    Client ──partial request──▶ Server (holds connection open, waiting... forever)
                   Client ──partial request──▶ Server (another open slot consumed)
                   Client ──partial request──▶ Server (and another...)
```

Because each individual connection uses very little bandwidth, Slowloris can take down a
surprisingly well-resourced server using only a single attacking machine — which is exactly what
makes it such a popular, low-cost tool (see [`06-dos-ddos-attack-tools.md`](06-dos-ddos-attack-tools.md)
for the tool itself).

## 5.4 UDP Application-Layer Flood Attack

Although classic UDP floods are a *volumetric* technique, several **application-layer protocols
that run over UDP** can themselves be abused for flooding, because a small request can trigger a
disproportionately large or resource-intensive response. Commonly abused UDP-based
application-layer protocols include:

| | |
|---|---|
| CHARGEN (Character Generator Protocol) | TFTP (Trivial File Transfer Protocol) |
| SNMPv2 (Simple Network Management Protocol v2) | NetBIOS (Network Basic Input/Output System) |
| QOTD (Quote of the Day) | NTP (Network Time Protocol) |
| RPC (Remote Procedure Call) | Quake Network Protocol |
| SSDP (Simple Service Discovery Protocol) | Steam Protocol |
| CLDAP (Connection-less LDAP) | VoIP (Voice over Internet Protocol) |

## 5.5 Multi-Vector Attack

A **multi-vector DDoS attack** combines volumetric, protocol, and application-layer techniques
against a single target — the attacker rapidly and repeatedly switches attack forms (e.g., a wave
of SYN packets, then a Layer-7 flood, then back again).

```
Multi-Vector in sequence:  Attacker ──Volumetric──▶ ──Protocol──▶ ──App-Layer──▶  Victim
Multi-Vector in parallel:  Attacker ──Volumetric──▶
                           Attacker ──Protocol────▶  (all hitting Victim at once)
                           Attacker ──App-Layer───▶
```

Attacks may be launched **one vector at a time** or **in parallel**, specifically to confuse an
organization's IT/security team and exhaust their resources by diverting their attention to the
wrong mitigation.

## 5.6 Peer-to-Peer (P2P) Attack

A P2P attack exploits bugs found in **peer-to-peer file-sharing servers/protocols**, most
commonly the **DC++ (Direct Connect)** protocol used for exchanging files between instant-message
clients. Unlike a botnet-based attack, a P2P attack requires **no direct attacker-to-agent
communication and no traditional botnet** — instead, the attacker instructs clients of a large P2P
file-sharing hub to disconnect from their normal P2P network and instead connect to the **victim's
fake website**. Because thousands of legitimate P2P users then aggressively try to connect to
that "website," the target's performance collapses. P2P attacks are relatively easy to identify
by signature, and can be minimized by disallowing P2P communication on specific ports (e.g., port
80).

## 5.7 Permanent Denial-of-Service (PDoS) Attack

Also called **"phlashing,"** PDoS attacks target **hardware** directly, causing *irreversible*
damage that requires the victim to repair or completely replace the affected device — unlike
every other attack in this repo, which is disruptive but temporary. PDoS exploits security flaws
in devices that allow remote administration of management interfaces (routers, printers, and
other networked hardware).

```
Attacker ──sends email/IRC/tweets/videos with fraudulent "hardware update" content──▶ Victim
Victim ──installs the fake "update," believing it's genuine──▶ (malicious code executes)
Attacker ◀──gains full control of the victim's system──────────────────────────────────
```

PDoS is the **"bricking"** technique: the attacker distributes a corrupted or vulnerability-laden
firmware update disguised as a legitimate one, via email, IRC, tweets, or videos. Once the victim
installs it (believing it to be genuine), the attacker gains complete control — and often the
hardware itself is left unusable ("bricked"). PDoS attacks are quicker and more destructive than
conventional DoS attacks, and — critically — they don't require the sustained resources a DDoS
does, since the damage is done once, permanently.

## 5.8 TCP SACK Panic Attack

**TCP Selective Acknowledgment (SACK) Panic** is a remote attack vector targeting **Linux**
machines specifically. Linux uses the SACK mechanism so a sender only needs to retransmit packets
the receiver hasn't already acknowledged; internally, Linux stores unacknowledged data in a
linked-list structure called the **socket buffer (SKB)**, which can hold a maximum of **17
segments** before acknowledged packets are purged from the list.

The attack exploits an **integer overflow vulnerability** in the socket buffer: the attacker sends
specially crafted SACK packets to the target, setting the **Maximum Segment Size (MSS)** to the
lowest possible value (**48 bytes**). A tiny MSS forces a huge number of small TCP segments to be
tracked for retransmission, pushing the socket buffer's 17-segment limit — triggering an integer
overflow that causes a **kernel panic**, i.e., a full denial of service. Because the vulnerability
sits in the kernel stack, this attack can also be launched against **containers and virtual
machines** running on an affected kernel.

```
Attacker ──SACK packet (MSS=48 bytes)──▶ Linux Server
Attacker ──SACK packet (MSS=48 bytes)──▶ Linux Server     Socket buffer exceeds 17-segment
                                                            limit → integer overflow → kernel panic
Legitimate Users ──requests──▶  ✗ (server has crashed)
```

**Countermeasures:**
- Implement vulnerability patching (this is a known, patched class of kernel vulnerability on
  maintained systems).
- Implement a firewall rule to block incoming packets that request the lowest MSS values.

## 5.9 Distributed Reflection Denial-of-Service (DRDoS) Attack

Also known as a **"spoofed" attack**, DRDoS exploits the TCP three-way handshake and involves
**multiple intermediary and secondary machines** that unwittingly contribute to the attack:

- **Attacker** → commands **intermediary victims** (zombies)
- **Intermediary victims** → send a stream of spoofed **TCP SYN** packets (spoofed to show the
  primary target's IP as the source) to **secondary victims** (reflectors) — machines that were
  never compromised
- **Secondary victims (reflectors)** → believing the primary target requested a connection, they
  reply with **SYN/ACK** traffic directly to the primary target
- **Primary target** → discards the unsolicited SYN/ACKs (it never sent the original SYN) —
  but the reflectors, having received no ACK back, keep **resending** SYN/ACK until a timeout
  occurs, generating sustained, heavy traffic at the target the whole time

```
Attacker ──▶ Intermediary Victims ──(spoofed SYN, src=Primary Target's IP)──▶ Secondary Victims
Secondary Victims ──(SYN/ACK flood)──────────────────────────────────────────▶ Primary Target
```

**Why it's especially dangerous:** the secondary victims (reflectors) *appear* to be directly
attacking the primary target, making the real attacker extremely difficult — sometimes
effectively impossible — to trace. Because many reflector machines each contribute bandwidth, the
combined attack bandwidth can dwarf a typical single-source DDoS.

**Countermeasures:**
- Turn off the **CHARGEN** service — a classic reflector/amplifier service — wherever it isn't
  needed.
- Keep servers patched with the latest security updates.

## 5.10 DDoS Extortion / Ransom DDoS (RDDoS) Attack

A **DDoS extortion attack**, also called **Ransom DDoS (RDDoS)**, is financially motivated
blackmail: the attacker threatens an organization with a DDoS attack and demands a ransom payment
to call it off.

```
1. Attacker uses a botnet/attack group to launch a small, "sample" DDoS attack
   against a subset of the target organization's assets
2. This proof-of-capability attack convinces the victim the threat is real
3. Attacker sends a ransom note/email demanding payment (with a deadline),
   warning that the "real," larger attack can be launched at any moment
```

The ransom note typically threatens further disruption, exposure of vulnerabilities/assets, or
data leakage, and demands payment via cryptocurrency. Many such threats are actually **bluffs**
from attackers who don't have real high-capacity DDoS capability — but organizations can't safely
assume that in the moment.

**Countermeasures:**
- Implement effective DDoS defense tooling *before* you're targeted (see
  [`09-protection-tools-and-services.md`](09-protection-tools-and-services.md)).
- Immediately report any ransom note to law enforcement and your security team — don't negotiate
  unilaterally.
- Frequently evaluate assets for risk tolerance (know what you can afford to lose/have down).
- Implement mitigation strategies such as **BGP/DNS swing** (rapidly rerouting traffic) and an
  **always-on protection service** so you're not scrambling to onboard a mitigation vendor during
  the actual attack.

---

**Next:** [`06-dos-ddos-attack-tools.md`](06-dos-ddos-attack-tools.md) →