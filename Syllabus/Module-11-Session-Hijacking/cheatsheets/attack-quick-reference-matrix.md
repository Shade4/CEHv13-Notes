# Cheatsheet — Attack Quick-Reference Matrix

One-page lookup: for each attack, what level it operates at, whether it needs an already-active victim session, the key tool(s), the clearest detection signal, and the single highest-leverage countermeasure.

| Attack | Level | Needs Existing Session? | Key Tool(s) | Detection Signal | Primary Countermeasure |
|---|---|---|---|---|---|
| **Blind Hijacking** | Network (TCP) | No (creates a spoofed one) | Custom scripting / seq. prediction | Unexpected packets with valid-looking but unverified sequence numbers | Randomized ISNs (modern OS default); encryption |
| **UDP Hijacking** | Network (UDP) | No | Scapy, hping3 | Duplicate/conflicting UDP replies to one request | Application-layer authentication (UDP has none natively) |
| **TCP/IP Hijacking** | Network (TCP) | Yes | Sniffer + packet crafting | `tcp.analysis.retransmission`, duplicate ACKs | Encrypted sessions (SSL/TLS, IPsec); switched networks |
| **RST Hijacking** | Network (TCP) | Yes | Colasoft Packet Builder, tcpdump, hping3 | `tcp.flags.reset==1` with unexpected source | Per-packet integrity checking; encrypted sessions |
| **MITM (ARP/ICMP)** | Network (Link) | N/A (enables other attacks) | bettercap, ettercap, arpspoof | ARP reply floods, duplicate MAC-to-IP mappings | ARPwatch/IDS; switched + segmented networks; DAI on switches |
| **IP Spoofing (Source-Routed)** | Network | No | Custom packet crafting | Packets carrying IP source-route options | Drop source-routed packets at routers/firewalls (default on most modern stacks) |
| **PetitPotam** | Application (RPC/NTLM) | No (coerces new auth) | Impacket (`PetitPotam.py`, `ntlmrelayx.py`), Rubeus | Inbound auth attempts *from* a Domain Controller | Disable NTLM/enable EPA on AD CS; patch per MS guidance |
| **Session Sniffing** | Application | Yes | Wireshark, Riverbed Packet Analyzer Plus | Cleartext session cookies on the wire | `Secure` + `HttpOnly` cookies; HTTPS everywhere |
| **Predictable Session Token** | Application | No | Custom scripting, JHijack | Sequential/short/short-lived IDs observed in testing | Long random tokens; framework-generated session IDs |
| **MITM / MITB (App-level)** | Application | Yes | Hetty, Caido, Burp Suite, banking Trojans | Unexpected proxy/certificate changes on client | Certificate pinning; endpoint protection; MFA |
| **XSS (session theft)** | Application | Yes | Manual/Burp/ZAP | Unusual outbound requests from client scripts | Output encoding, CSP, `HttpOnly` cookies |
| **CSRF** | Application | Yes | Manual PoC / Burp | State-changing requests with no matching user action | `SameSite` cookies, anti-CSRF tokens, re-auth on sensitive actions |
| **Session Replay** | Application | Yes | Sniffer + replay tooling (Burp Repeater) | Same token used twice in a way that violates expected flow | Nonces / one-time tokens; short token lifetimes |
| **Session Fixation** | Application | No (pre-login) | Phishing + crafted link | Login using an ID issued before authentication | Regenerate session ID after login |
| **Session Donation** | Application | No (attacker's own session) | Phishing + crafted link | Victim data appearing under an unrelated account | Regenerate session ID after login; user education |
| **Session Hijacking via Proxy** | Application | Yes | Malicious redirect server | Traffic routed through an unexpected intermediate host | HTTPS + certificate validation; link/URL scrutiny |
| **CRIME Attack** | Application (TLS) | Yes | ARP spoof + custom JS, CrimeCheck | Repeated near-identical HTTPS requests with varying length | Disable TLS/SPDY compression |
| **Forbidden Attack** | Application (TLS) | Yes | Custom tooling exploiting AES-GCM nonce reuse | TLS nonce reuse in captured handshakes | Correct, spec-compliant AES-GCM nonce generation |
| **CRIME's cousin: BREACH** | Application (HTTP) | Yes | Same compression-oracle technique, at the HTTP layer | Same as CRIME, on gzip'd HTTP bodies | Disable HTTP compression for pages reflecting secrets |

---
**See also:** [`commands-cheatsheet.md`](commands-cheatsheet.md) for the runnable syntax behind each row above.