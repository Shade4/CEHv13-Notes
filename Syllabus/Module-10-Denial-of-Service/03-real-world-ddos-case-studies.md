# 03 — Real-World DDoS Case Studies

> Exam objective: *Summarize DoS/DDoS concepts* (illustrated with real incidents)

Theory is easier to retain when it's anchored to a real event. This file covers two case studies:
a composite "volunteer botnet" scenario built around a real, widely-used attack tool
(**HOIC**), and a fully documented, dated, CVE-tracked real-world incident — the September 2023
**HTTP/2 "Rapid Reset"** attack that Google Cloud's DDoS response team defended against.

---

## 3.1 Case Study: The "Volunteer Botnet" Pattern (HOIC / Anonymous-style Attacks)

This pattern illustrates how a DDoS attack can be crowdsourced rather than purely
botnet-automated — a technique associated with hacktivist campaigns:

```
 1. An anonymous attacker hosts the High Orbit Ion Cannon (HOIC) DDoS tool on a
    web server they own (or on a compromised web server)
 2. The attacker advertises the HOIC download — with a malicious link — on
    social platforms and search engines (Twitter, Facebook, Google, etc.)
 3. Sympathetic users ("volunteers") find the ad and download the tool
 4. Volunteers connect via an IRC channel to the anonymous attacker and await instructions
 5. The attacker instructs everyone to flood a target (e.g., a payment processor) at once
 6. The combined flood overwhelms the target, which stops responding even to legitimate users
```

The key insight: the attacker doesn't need to compromise thousands of machines with malware — they
only need to *recruit* enough willing participants, each running the tool voluntarily against a
shared target on command. This is functionally a "botnet" made of human volunteers instead of
malware-infected zombies.

**Hackers also advertise botnet download links** disguised as ordinary security software or
system alerts — fake antivirus pop-ups ("Protect your PC from viruses and threats"), forged
Windows Defender/OS notifications claiming viruses were found, and even fake ransomware-style
warnings ("YOUR FILES ARE ENCRYPTED") — all engineered to get a victim to click through and
unknowingly join a botnet or install malware. Recognizing these lures is a core social-engineering
skill covered in depth in `CEHv13-Module09-Social-Engineering`.

---

## 3.2 Case Study: Google Cloud vs. the HTTP/2 "Rapid Reset" Attack (2023)

**Source:** https://cloud.google.com (Google Cloud's own DDoS incident writeup)

### Background
In September 2023, Google's DDoS response team disclosed that they had successfully defended
against the largest Layer-7 DDoS attack recorded up to that point: a peak of **398 million
requests per second (rps)** — roughly **7.5x larger** than the previous record attack they had
observed (46 million rps). The attack used a novel technique dubbed **"HTTP/2 Rapid Reset,"**
targeting websites, Internet services, and Internet infrastructure companies broadly (not just
Google).

### Attack Timeline
The campaign was first recorded in late August 2023 and continued through the end of September
2023. The Rapid Reset technique attempted to impact major infrastructure providers — including
Google services and Google Cloud infrastructure customers — for short bursts of **2–3 minutes**
at peak intensity. Though individual bursts were short-lived, the targeted services experienced an
unexpected surge of TCP packets carrying the **RST (Reset)** flag, aimed at flooding and resetting
connections on the target server. Analysis of the campaign showed dozens of discrete "rapid reset"
incidents scattered across September, several spiking well above baseline request rates before
Google's mitigations matured.

### Attack Mechanism
The attack exploited **stream multiplexing**, a core feature of the widely adopted **HTTP/2**
protocol. HTTP/2 allows a single TCP connection to carry up to roughly **100 concurrent live
streams**. The attackers abused this by rapidly opening a stream and then *immediately*
resetting it, over and over, in a tight sequence — all reset streams — within the same
connection. Because opening and cancelling a stream is cheap for the *client* to do but still
costs the *server* real work to process (allocate state, route the request, then tear it down),
this let a modest number of attacking machines generate an enormous effective request rate
against backend services, without needing a traditional room-sized botnet.

### Google's Response
Google's response team credits their success in weathering the attack to substantial pre-existing
investment in **edge capacity** at the perimeter of Google's network, which kept both Google's own
services and their customers' services largely unaffected. As the response team gained deeper
insight into the attack methodology, they:

- Devised and deployed new countermeasures, upgrading proxies and defense systems specifically
  to neutralize the Rapid Reset technique.
- Extended the same hardened infrastructure that protects Google's own Internet-facing services to
  Google Cloud customers using **Application Load Balancer** and **Cloud Armor**.
- Quickly began a **collaborative, cross-industry response** with other cloud providers and
  maintainers of the HTTP/2 protocol stack, sharing real-time threat intelligence and mitigation
  guidance to prevent broader disruption across the industry.
- Facilitated **coordinated responsible disclosure** of the new attack methodology and its
  potential impact on widely used open-source and commercial proxies, application servers, and
  load balancers — giving vendors across the ecosystem time to ship patches.

### The Vulnerability: CVE-2023-44487
The underlying weakness that made Rapid Reset possible was assigned **CVE-2023-44487**, rated
**High Severity** with a **CVSS score of 7.5 out of 10**. Because the flaw was rooted in how the
HTTP/2 protocol's stream-multiplexing feature is commonly implemented, it affected a broad swath
of the Internet's infrastructure software — not just one vendor's product — which is exactly why
the coordinated, cross-industry disclosure process mattered so much here.

### Why This Case Study Matters for CEH
- It's a clean real-world example of an **application-layer / protocol-hybrid attack** — see
  `04` and `05` for the named-technique taxonomy this maps onto (it shares DNA with both
  connection-flood/protocol attacks and application-layer resource-exhaustion attacks).
- It demonstrates that **defense-in-depth at the edge** (Google's phrase: "substantial investment
  in edge capacity") — not any single silver-bullet control — is what kept services available.
- It shows the real-world value of **responsible disclosure** and **cross-vendor coordination**
  once a novel technique is discovered, rather than each provider patching in isolation.

---

**Next:** [`04-volumetric-and-protocol-attacks.md`](04-volumetric-and-protocol-attacks.md) →