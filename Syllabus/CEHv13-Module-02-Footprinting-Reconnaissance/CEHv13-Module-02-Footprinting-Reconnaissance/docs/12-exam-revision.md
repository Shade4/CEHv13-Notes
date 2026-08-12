# 12 — Exam Revision

## High-value definitions

### Footprinting

Systematic collection of information about a target to build a profile/blueprint.

### Reconnaissance

Information gathering performed before deeper attack or assessment activity.

### Passive reconnaissance

Gathering information without directly interacting with target infrastructure.

### Active reconnaissance

Gathering information through direct interaction with target infrastructure.

### OSINT

Intelligence derived from openly/publicly accessible sources.

## High-value distinctions

| Question | Answer |
|---|---|
| Name → IPv4 | A |
| Name → IPv6 | AAAA |
| Mail server | MX |
| Authoritative DNS server | NS |
| Alias | CNAME |
| Reverse DNS | PTR |
| DNS zone metadata | SOA |
| Service location | SRV |
| Registration research | WHOIS/RDAP |
| Path observation | traceroute/tracert |
| Internet-exposed service search | Shodan-style search |
| Search-engine advanced queries | Google hacking/dorking |
| Relationship graphing | Maltego |
| Modular recon framework | Recon-ng |

## Common traps

### Trap 1

"Public information = vulnerability."

False.

Public information may simply be information.

### Trap 2

"WHOIS gives all private owner information."

False.

Privacy protection, registry policy, and modern registration systems can limit data.

### Trap 3

"Traceroute shows the exact physical route."

False.

It shows responding network hops as observed from the tester's location.

### Trap 4

"Shodan finding = vulnerable host."

False.

A service observation is not vulnerability proof.

### Trap 5

"DNS zone transfer is normal enumeration."

A properly configured zone transfer is intended for authorized DNS secondary servers. An unauthorized transfer can be a serious information-disclosure issue.

### Trap 6

"Passive means legal."

False.

Authorization and applicable law still matter.

### Trap 7

"AI output is evidence."

False.

AI output is a hypothesis until verified against reliable sources.

## One-minute revision

```text
Recon = collect
Footprint = build profile
Passive = observe
Active = interact
WHOIS/RDAP = registration
DNS = names/resources
Traceroute = path
Search engines = indexed public information
Shodan = observed Internet services
Social engineering = human information source
Maltego = relationships
Recon-ng = modular automation
Countermeasures = reduce unnecessary exposure
```
