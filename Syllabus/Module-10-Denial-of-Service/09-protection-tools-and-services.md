# 09 — Protection Tools and Services

> Exam objective: *Explain DoS/DDoS attack countermeasures* (products/services subset)

Beyond configuration-level countermeasures, the DDoS-protection market offers dedicated
**hardware appliances**, **host-based software tools**, and **cloud-delivered services**. This
file is a buyer's-guide-style tour of the main categories and named products referenced in the
CEH curriculum.

---

## 9.1 DoS/DDoS Protection at the ISP Level

One of the most effective places to stop a DoS attack is at the **gateway**, handled by the
contracted ISP. Many ISPs offer a **"clean pipes"** service-level agreement, guaranteeing a
certain bandwidth of *genuine* traffic rather than raw total bandwidth (which an attacker could
otherwise saturate with garbage). In practice, though, **many ISPs simply block all traffic**
during an active DDoS attack — which stops the attack but also denies legitimate users, which is
why organizations without a "clean pipes" arrangement often turn to third-party subscription
scrubbing services instead.

- **In-the-cloud DDoS protection** for Internet links prevents the link itself from becoming
  saturated. During an attack, traffic is redirected to the ISP (or a partner cloud-scrubbing
  provider), cleaned, and sent back — the attack traffic never actually reaches the customer's
  own bandwidth.
- Administrators can also request the ISP block the currently-affected IP and move the site to a
  new IP after performing DNS propagation, as an emergency last resort.
- Vendors such as **Imperva** and **VeriSign** offer subscription-based cloud protection services
  that sit as an intermediary: they receive traffic destined for your network, filter it, and pass
  on only the trusted connections.

---

## 9.2 Advanced DDoS Protection Appliances

| Appliance | Vendor / Source | Highlights |
|---|---|---|
| **FortiDDoS** (200F, 1500E, 1500E-DC, 1500F, 2000E, 2000E-DC, VM04/08/16) | Fortinet — https://www.fortinet.com | Massively parallel, machine-learning architecture delivering low-latency mitigation without the performance compromises typical of CPU-based systems; inspects both inbound and outbound Layer 3/4/7 traffic down to the smallest packet sizes for fast, accurate detection |
| **Quantum DDoS Protector** | Check Point — https://www.checkpoint.com | Multi-layered protection: behavioral baselining that blocks abnormal traffic, automatically generated + predefined attack signatures, advanced challenge/response techniques, sub-second response time against network-flood and application-layer attacks, customizable per environment, and pre-firewall traffic filtering; integrates with Check Point Security Management |
| **Huawei AntiDDoS1000** | Huawei — https://e.huawei.com | Uses Big Data analytics with modeling for 60+ traffic types, offering comprehensive defense against 100+ attack types; deployable in-line to defend against volumetric and application attacks in real time; when local scrubbing capacity is exceeded, it hands off to an upstream carrier/ISP AntiDDoS device to maintain service continuity |
| **A10 Thunder TPS** (Threat Protection System) | A10 Networks — https://a10networks.com | Detects and blocks external threats including DDoS before they escalate into costly outages; emphasizes maintained service availability, ability to "defeat growing attacks," scalable protection, and reduced security operating expense |

---

## 9.3 DoS/DDoS Protection Tools (Host / Network-Level Software)

| Tool | Source | Notes |
|---|---|---|
| **Anti DDoS Guardian** | https://beethink.com | Protects IIS, Apache, game servers, Camfrog servers, mail servers, FTP servers, VOIP PBX, and SIP servers. Monitors every incoming/outgoing packet in real time, displaying local/remote address and flow details; can cap network-flow counts, client bandwidth, concurrent TCP-connection counts and rate, plus UDP bandwidth/connection-rate/packet-rate limits. |
| DDoS-GUARD | https://ddos-guard.net | Network-level DDoS mitigation service/appliance |
| DOSarrest | https://www.dosarrest.com | Managed DDoS protection service |
| Radware DefensePro X | https://www.radware.com | Enterprise-grade DDoS mitigation appliance |
| Gatekeeper | https://github.com | Open-source DDoS mitigation project |
| F5 DDoS Attack Protection | https://www.f5.com | Application- and network-layer DDoS protection integrated with F5's app delivery stack |

---

## 9.4 DoS/DDoS Protection Services (Cloud-Delivered)

| Service | Source | Notes |
|---|---|---|
| **Cloudflare** | https://www.cloudflare.com | Defends against DDoS attacks using a **100 Tbps** network that blocks an average of **87 billion threats daily**. Provides rapid mitigation — typically within **three seconds** — using techniques including BGP-based protection and tight integration with Layer-7 services, aiming for comprehensive security with reduced operational overhead. |
| **Akamai DDoS Protection** | https://www.akamai.com | Leverages dedicated infrastructure to safeguard Internet-facing applications and systems while keeping DNS fast, secure, and always available. Stops DDoS attacks and malicious traffic in the cloud *before* they reach applications, data centers, or infrastructure — removing the need for multiple redundant on-prem firewalls. |
| Stormwall PRO | https://stormwall.network | Managed DDoS protection |
| Imperva DDoS Protection | https://www.imperva.com | Cloud-based scrubbing and mitigation |
| Nexusguard | https://www.nexusguard.com | Cloud-based DDoS mitigation service |
| BlockDoS | https://www.blockdos.net | DDoS protection service |

---

## 9.5 Choosing Between Appliance, Software Tool, and Cloud Service

| Consideration | On-prem Appliance | Host Software Tool | Cloud Service |
|---|---|---|---|
| Protects against volumetric attacks that saturate your own uplink | ❌ (your pipe is already full) | ❌ | ✅ (scrubbed upstream, before it reaches you) |
| Capital expense vs. operating expense | Higher CapEx | Low CapEx | Subscription OpEx |
| Time-to-mitigate for novel attacks | Depends on vendor signature/ML updates | Depends on vendor updates | Often fastest — shared threat intel across all customers (as in the Google Cloud case study, `03`) |
| Good fit for | Large enterprises with dedicated data centers/network teams | Small-to-mid servers, single applications | Any size — especially anyone whose uplink itself could be saturated |

In practice, most serious DDoS-defense postures use **all three layers together**: an
upstream cloud/ISP scrubbing service to absorb the largest volumetric attacks before they reach
your network at all, a perimeter appliance or firewall for protocol-layer filtering and rate
limiting, and host-level software/hardening for application-layer resilience.

---

**Next:** [`10-dos-ddos-resilience-testing.md`](10-dos-ddos-resilience-testing.md) →
(Bonus/extra content not in the original CEH slide deck — a full authorized load/resilience
testing methodology.)