# 01 — DoS/DDoS Concepts

> Exam objective: *Summarize DoS/DDoS concepts*

## 1.1 What Is a DoS Attack?

A **Denial-of-Service (DoS) attack** is an attack on a computer or network that reduces,
restricts, or prevents access to system resources for legitimate users. The attacker floods the
victim's system with non-legitimate service requests or traffic to overload its resources,
bringing the system down or significantly degrading performance. Crucially, **the goal of a DoS
attack is availability sabotage, not unauthorized access or data theft** — although a DoS attack
can sometimes be used as a smokescreen for a separate data-theft operation (see the "diversion"
pattern in `02`).

**Example categories of DoS attacks:**
- Flooding a victim's system with more traffic than it can handle
- Flooding a service (e.g., IRC) with more events than it can handle
- Crashing a TCP/IP stack by sending corrupt/malformed packets
- Crashing a service by interacting with it in an unexpected way
- Hanging a system by forcing it into an infinite loop

**What DoS attacks target/cause:**
- Consumption of resources (bandwidth, disk space, CPU time, data structures)
- Consumption of bandwidth specifically
- Actual physical destruction or alteration of network components
- Destruction of programming and files on a computer system

DoS attacks generally fall into two broad targeting strategies:
- **Bandwidth attacks** — overflow the network with high-volume traffic using existing network
  resources, starving legitimate users of capacity.
- **Connectivity attacks** — overflow a system with a large number of connection requests,
  consuming all available OS resources so the system can't process legitimate requests.

> 📞 **Analogy:** think of a food-catering company that does all its business by phone. If an
> attacker wants to disrupt that business, they just need to keep every phone line busy. A DoS
> attack does the same thing to a server — it occupies every available "line" (connection slot,
> CPU cycle, memory buffer) so legitimate customers can never get through.

**Impact of DoS attacks:** loss of goodwill, network outages, financial losses, and operational
disruptions. In the worst case, a DoS attack can even cause accidental destruction of files and
programs for everyone who was connected to the victim system at the time of the attack.

## 1.2 What Is a DDoS Attack?

A **Distributed Denial-of-Service (DDoS) attack** is a large-scale, coordinated attack on the
availability of services on a victim's system or network resources, launched **indirectly**
through many compromised computers (a **botnet**) spread across the Internet.

As defined by the World Wide Web Security FAQ:
> "A distributed denial-of-service (DDoS) attack uses many computers to launch a coordinated DoS
> attack against one or more targets. Using client/server technology, the perpetrator is able to
> multiply the effectiveness of the denial of service significantly by harnessing the resources
> of multiple unwitting accomplice computers, which serve as attack platforms."

The flood of incoming messages essentially forces the target system to shut down, denying service
to legitimate users.

**Primary vs. secondary victims:**
- The services under attack belong to the **primary victim**.
- The compromised systems used to *launch* the attack are the **secondary victims**.
- Using secondary victims lets the attacker mount a large, disruptive attack while making it very
  difficult to trace the attack back to the original attacker.

The primary objective of a DDoS attack is to first gain administrative access to as many systems
as possible. Attackers typically use a customized attack script to identify vulnerable systems;
once access is gained, the attacker uploads and runs DDoS software on those systems, ready to
fire at a time of their choosing. DDoS attacks have become popular because exploit kits are easily
accessible and require very little skill to operate — yet they can quickly consume the largest
hosts on the Internet.

### The 12-Step DDoS Attack Lifecycle

```
 01. Attacker sets a C&C center and crimeware toolkit database
 02. Attacker recruits affiliates from an affiliation network
 03. Affiliates contribute malware and release the DDoS toolkit
 04. Malicious website redirects users to the crimeware toolkit database
 05. Victims are redirected to a malicious website (phishing/social engineering) or
     a new malicious website is created
 06. Users visit the malicious/compromised website
 07. The malicious website redirects users to the crimeware toolkit database
 08. Malware infects the users' systems
 09. Bots connect back to the C&C center
 10. (same connect-back loop as above; bots register with C&C)
 11. Infected systems look for other vulnerable systems and infect them,
     growing the botnet
 12. The (now large) botnet attacks the primary target — the organization
```

This is the same lifecycle whether the "malicious website" is a purpose-built phishing clone or a
legitimate site an attacker has quietly compromised to serve as a silent redirector.

## 1.3 How Do DDoS Attacks Work?

In a DDoS attack, many applications barrage a target with fake, external requests that make the
system, network, browser, or site slow, useless, disabled, or outright unavailable.

```
   ATTACKER          HANDLER (x2 shown)         COMPROMISED PCs (ZOMBIES)      TARGET
  ┌─────────┐   1   ┌──────────────┐   2    ┌───────────────────────────┐  3  ┌────────┐
  │Attacker │──────▶│   Handler    │───────▶│  Compromised PCs (Zombies) │────▶│ Target │
  │ sets a  │       │ (infects a   │        │  instructed to attack the │     │ Server │
  │ handler │       │ large # of   │        │       target server        │     └────────┘
  │ system  │       │ computers)   │        └───────────────────────────┘
  └─────────┘       └──────────────┘
```

1. The attacker sets up one or more **handler** systems.
2. Each handler infects a large number of Internet-connected computers with malware, turning them
   into **zombie agents** managed via a Command-and-Control (C&C) server.
3. The zombie systems are instructed to attack a target server, typically all at once.

**Reflection variant:** zombie agents send a connection request to a large number of *reflector*
systems, but spoof the source IP address to be the **victim's** address. The reflector systems
believe the request came from the victim and send their response *to the victim* instead of to
the zombie. The victim's machine is now flooded with unsolicited responses from many reflectors
simultaneously — this either degrades performance or shuts the victim down completely. (This
reflection pattern is explored in depth as amplification/DRDoS attacks in `04` and `05`.)

## 1.4 Chapter Roadmap

| Concept | Where it's covered |
|---|---|
| Botnets, cybercrime hierarchy, propagation, scanning | [`02-botnets-and-cybercrime-ecosystem.md`](02-botnets-and-cybercrime-ecosystem.md) |
| Real-world case studies (Anonymous/HOIC, Google Cloud Rapid Reset) | [`03-real-world-case-studies.md`](03-real-world-case-studies.md) |
| Volumetric & protocol attack techniques | [`04-volumetric-and-protocol-attacks.md`](04-volumetric-and-protocol-attacks.md) |
| Application-layer & advanced attack techniques | [`05-application-layer-and-advanced-attacks.md`](05-application-layer-and-advanced-attacks.md) |
| Attack tools | [`06-dos-ddos-attack-tools.md`](06-dos-ddos-attack-tools.md) |
| Detection & countermeasures | [`07-detection-techniques.md`](07-detection-techniques.md), [`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) |
| Protection products/services | [`09-protection-tools-and-services.md`](09-protection-tools-and-services.md) |

---

**Next:** [`02-botnets-and-cybercrime-ecosystem.md`](02-botnets-and-cybercrime-ecosystem.md) →