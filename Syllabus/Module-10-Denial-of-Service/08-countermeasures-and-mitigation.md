# 08 — Countermeasures and Mitigation

> Exam objective: *Explain DoS/DDoS attack countermeasures*

DoS/DDoS is one of the foremost security threats on the Internet, so there's a real and constant
need for layered mitigation. **No single, complete solution protects against every known form of
DDoS attack** — and attackers continually invent new methods specifically to bypass whatever
defenses are currently deployed. This file is the full defensive playbook: high-level response
strategies, the detailed DDoS countermeasure catalog, botnet-specific defenses, and a big list of
general hardening steps.

---

## 8.1 High-Level Countermeasure Strategies

When an attack is actively underway, an organization generally chooses one of three broad
response postures:

| Strategy | Approach | Trade-off |
|---|---|---|
| **Absorbing the Attack** | Use additional capacity (bandwidth, compute) to soak up the extra load | Requires preplanning and additional resources — and you pay for that spare capacity even when *not* under attack |
| **Degrading Services** | Identify critical services and keep *those* functional while deliberately shedding non-critical ones | A good middle ground — keeps the business-critical path alive during an attack |
| **Shutting Down Services** | Shut down all services entirely until the attack subsides | Not ideal, but sometimes the only realistic option, and can limit damage/cost in extreme cases |

## 8.2 DDoS Attack Countermeasures (Detailed Catalog)

### Protect Secondary Victims
The single best way to reduce the overall DDoS problem is for potential **secondary victims**
(i.e., ordinary end-user systems) to keep themselves from ever being recruited into a botnet in
the first place:

- **Individual users** should monitor their own system's security regularly, ensure no DDoS agent
  software gets installed, keep antivirus/anti-Trojan software installed and current, apply
  security patches promptly, disable unnecessary services, uninstall unused applications, and scan
  all files received from external sources. Because this can feel like a lot to ask of an average
  user, modern OS/software vendors increasingly ship built-in defensive mechanisms by default —
  which is exactly why keeping those mechanisms **properly configured and regularly updated**
  matters so much.
- **Network service providers** can adopt dynamic pricing for network usage, which gives
  potential secondary victims a direct financial incentive to keep their own systems clean rather
  than unknowingly subsidize an attacker's traffic.

### Detect and Neutralize Handlers
In the classic agent-handler DDoS architecture, the **handler** is the intermediary the attacker
uses to control the wider agent/zombie army — and critically, there are usually **far fewer
handlers than agents**. That asymmetry is an opportunity: analyzing communication protocols and
traffic patterns between handlers-and-clients or handlers-and-agents can reveal which network
nodes are infected handlers. Neutralizing even a small number of handlers can render a large
number of agents useless, disrupting the whole attack network far more efficiently than trying to
chase down every individual bot.

There's also a reasonable probability that a DDoS packet's **spoofed source address doesn't
represent a valid address within its claimed subnet** — thoroughly understanding normal
communication patterns among handlers, clients, and agents helps identify these spoofed addresses
and stop the attack traffic from being trusted.

### Prevent Potential Attacks

**Egress Filtering**
Egress filtering scans the headers of IP packets **leaving** a network. Packets that meet the
network's own address-space specifications are allowed out; anything that doesn't (e.g., a
spoofed source address that doesn't belong to the internal network) never reaches its intended
target. This directly blocks spoofed-source DDoS traffic from *leaving* your network, and also
limits the effectiveness of exploit payloads that need to phone home — restricting outbound
exposure limits an attacker's ability to reach other systems or pull in additional tools even if
one host is already compromised.

**Ingress Filtering**
Ingress filtering is a packet-filtering technique widely used by **ISPs** to prevent source-address
spoofing of traffic **entering** the network. It indirectly combats several forms of net abuse by
making traffic traceable back to its true source, and specifically protects against flooding
attacks that originate from valid-looking source prefixes by allowing the true originator to be
traced.

**TCP Intercept**
TCP intercept is a router traffic-filtering feature that protects TCP servers from **SYN-flood**
attacks. A SYN flood sends a huge volume of connection requests with unreachable return addresses;
since those addresses can never respond, the connections stay open and unresolved, and the sheer
volume of stuck half-open connections can deny service even to legitimate requests.

In **TCP intercept mode**, a router intercepts SYN packets sent by clients toward a server and
matches them against an extended access list. On a match, the intercept software completes a
connection with the *client* on the server's behalf, and separately completes a connection with
the *server* on the client's behalf. Once both half-connections are established, the software
transparently splices them together — meaning fake/incomplete connection attempts never actually
reach the real server at all.

*Enabling TCP intercept on Cisco IOS software (source: cisco.com):*

| Step | Command | Purpose |
|---|---|---|
| 1 | `access-list access-list-number {deny \| permit} tcp any destination destination-wildcard` | Defines an IP extended access list |
| 2 | `ip tcp intercept list access-list-number` | Enables TCP intercept using that access list |

```
! Example: protect the 10.10.1.0/24 server subnet with TCP intercept
Router(config)# access-list 101 permit tcp any 10.10.1.0 0.0.0.255
Router(config)# ip tcp intercept list 101
```

An access list typically defines the **source as "any"** and the **destination as the specific
network/server to protect** — since it's the destination that needs shielding, not any particular
source. TCP intercept operates in one of two modes:

```
Router(config)# ip tcp intercept mode {intercept | watch}
```

- **Intercept mode (default):** the router actively intercepts *every* inbound SYN, replies with a
  SYN-ACK on the server's behalf, and waits for the client's ACK before ever contacting the real
  server. Once the three-way handshake genuinely completes, the router links the two half
  connections together.
- **Watch mode:** connection requests are allowed to pass through toward the server, but the
  router *watches* to confirm the handshake completes within **30 seconds**; if it doesn't, the
  router sends a reset to the server to clear the stale half-open state.

**Rate Limiting**
Rate limiting controls the rate of inbound or outbound traffic on a network interface controller,
directly reducing the high-volume inbound traffic that causes a DDoS impact. It's especially
useful on hardware appliances, where the technique can be configured to cap request rates at
**Layers 4 and 5** of the OSI model.

```bash
# Linux — simple ICMP rate-limit example with iptables (defends against ICMP floods, PoD, Smurf)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 4 -j ACCEPT
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

# Linux — rate-limit new inbound TCP connections per source using nftables
sudo nft add rule inet filter input tcp flags syn tcp option maxseg size 1-500 counter drop
sudo nft add rule inet filter input ct state new limit rate 20/second accept
```

### Deflect Attacks (Honeypots)
Systems deliberately deployed with **limited security** — **honeypots** — act as bait for
attackers. A honeypot can imitate essentially any part of a real network (web servers, mail
servers, clients) and serves two purposes: it draws attacker attention *away* from genuinely
sensitive systems, and it gives defenders a means of gathering intelligence about attacker
techniques and tools by recording all activity on the decoy system. A **defense-in-depth**
approach using **IPsec** at different points in the network can be used to divert suspicious DoS
traffic into one or more honeypots.

There are two categories of honeypot:
- **Low-interaction honeypots** — simulate limited services, lower risk and effort to maintain.
- **High-interaction honeypots** — a **honeynet** is the classic example: a full simulated network
  of decoy computers, sometimes with real applications running on real machines, purpose-built so
  every activity within it can be fully tracked and analyzed.

**Honeypot / deception tools:**
| Tool | Source |
|---|---|
| Blumira | https://www.blumira.com |
| KFSensor | https://www.kfsensor.net |
| Valhala Honeypot | https://sourceforge.net |
| Cowrie | https://github.com |
| HoneyHTTPD | https://github.com |
| StingBox | https://www.stingbox.com |

Blumira, for example, is deception technology that helps security teams detect unauthorized
access attempts and an attacker's lateral movement across the network with low ongoing maintenance
overhead — once it detects a honeypot-security event, it can immediately block the offending
source IP at the switch or firewall level.

### Mitigate Attacks

| Technique | Mechanism | Limitation |
|---|---|---|
| **Load Balancing** | Increase bandwidth on critical connections to absorb attack traffic; replicate servers for failsafe protection; balance load across a multiple-server architecture | Cost of maintaining spare/replicated capacity |
| **Throttling** | Configure routers with "min-max fair server-centric" logic to throttle incoming traffic to levels the server can safely handle, filtering legitimate traffic from DDoS traffic | Can trigger false alarms and occasionally drops some legitimate traffic along with the attack traffic |
| **Drop Requests** | The router/server drops packets as load increases, sometimes first forcing the requester to solve a computationally expensive puzzle before the request is processed further | Zombie systems may notice degraded performance and simply give up trying — a modest side benefit, not a full solution |

### Post-Attack Forensics

| Technique | Purpose |
|---|---|
| **Traffic Pattern Analysis** | Post-attack data is stored and analyzed to identify characteristics unique to the attack traffic, which then feeds back into updated load-balancing and throttling rules — and helps ensure your own servers aren't unwittingly usable as a launch platform against other sites |
| **Packet Traceback** | Similar to reverse engineering — the victim works backward from received packets to identify the true source, enabling both blocking of that source and further intelligence-gathering on the attacker's tools/techniques |
| **Event Log Analysis** | DDoS event logs (from honeypots, firewalls, packet sniffers, and server logs) assist forensic investigation and any subsequent legal action; router/firewall/IDS logs help identify DoS traffic sources, and — with the cooperation of intermediary ISPs and law enforcement — can sometimes be traced all the way back to the attacker's real IP address |

---

## 8.3 Techniques to Defend Against Botnets

| Technique | Mechanism |
|---|---|
| **RFC 3704 Filtering** | A basic ACL filter that limits DDoS impact by denying traffic with spoofed addresses — requiring packets to originate from valid, allocated address space consistent with network topology. A "bogon list" of unused/reserved IPs that should never appear as a source is maintained; any packet sourced from a bogon address gets dropped. Since the bogon list changes over time, administrators should confirm their ISP performs this filtering, or maintain their own bogon ACL rules if not. |
| **Cisco IPS Source IP Reputation Filtering** | Uses reputation services to determine whether a given IP/service is a known threat source. Cisco's "Global Correlation" capability (in Cisco IPS 7.0+) taps the **Cisco SensorBase Network**, a continuously updated database of known threats — botnets, malware outbreaks, dark nets, and botnet harvesters — to filter DoS traffic before it reaches critical assets, incorporating global threat intelligence for earlier detection. |
| **Black Hole Filtering** | Incoming traffic is silently discarded/dropped at a designated network node ("black hole") without informing the sender that their data never arrived. **Remotely-triggered black-hole (RTBH) filtering** performs this in coordination with the ISP, using **BGP** host routes to redirect traffic destined for the victim to a "null0" next hop — effectively vaporizing the attack traffic before it ever reaches the target. |
| **DDoS Prevention Offerings from ISP/DDoS Service** | Effective specifically against **IP spoofing** at the ISP level — the ISP scrubs/cleans traffic before it ever reaches the customer's Internet link. Because this runs in the ISP's cloud, the customer's own Internet link never gets saturated in the first place. Features like Cisco's **IP Source Guard** (or equivalents on other routers) filter traffic based on the DHCP snooping binding database or IP-source bindings, preventing bots from successfully sending spoofed packets in the first place. |

## 8.4 Additional DoS/DDoS Countermeasures (General Hardening Checklist)

- Use strong encryption (**WPA2/WPA3, AES-256**) on broadband/wireless networks to defend against
  eavesdropping that could otherwise feed a later attack.
- Keep software and protocols up to date; scan systems thoroughly for anomalous behavior.
- Update the kernel to its latest stable release; disable unused/insecure services.
- Block all inbound packets originating from known service ports commonly abused as reflectors.
- Enable **TCP SYN cookie** protection.
- Prevent transmission of fraudulently addressed packets at the **ISP level**.
- Implement cognitive radios in the physical layer to handle jamming/scrambling attacks (relevant
  for wireless infrastructure).
- Configure firewalls to deny unnecessary external **ICMP** traffic.
- Secure remote administration and connectivity-testing interfaces.
- Perform thorough input validation everywhere user-supplied data reaches your application.
- Avoid unnecessary, unsafe functions such as `gets` and `strcpy` in your own code (classic
  buffer-overflow enablers referenced in `05.1`).
- Use advanced network-level surveillance to continuously monitor the network perimeter.
- Ensure semi-accessible connections use assertive timeout functions.
- Implement a distributed-server model and colocation services as a backup architecture to reduce
  overload risk during an attack.
- Ensure servers are free of bottlenecks and single points of failure.
- Use third-party DDoS protection services for enhanced coverage against major attacks (see
  [`09-protection-tools-and-services.md`](09-protection-tools-and-services.md)).
- Use multi-cloud deployment models for critical applications, to guarantee backup capacity during
  a cloud-targeted DDoS event.
- Perform extensive DoS/DDoS attack **simulations** to avoid being caught off guard by sudden
  surges, and to validate your counteraction strategy in advance (see
  [`10-dos-ddos-resilience-testing.md`](10-dos-ddos-resilience-testing.md)).
- Share threat intelligence with industry peers and subscribe to threat-intel feeds to stay
  current on emerging DDoS trends.
- Use **AI/ML-based anomaly detection** to automatically flag deviations from typical traffic
  behavior in real time.
- Limit network broadcasting where it isn't operationally required.
- Disable legacy/abusable services such as **echo** and **CHARGEN**.

---

**Next:** [`09-protection-tools-and-services.md`](09-protection-tools-and-services.md) →