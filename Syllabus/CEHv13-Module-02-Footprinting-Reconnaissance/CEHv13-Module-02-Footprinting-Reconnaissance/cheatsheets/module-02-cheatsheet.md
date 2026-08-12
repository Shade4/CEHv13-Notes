# Module 02 Cheat Sheet

## Core flow

```text
Scope
 ↓
Passive OSINT
 ↓
Search engines
 ↓
Internet research
 ↓
Social networks
 ↓
WHOIS/RDAP
 ↓
DNS
 ↓
Network path
 ↓
Email metadata
 ↓
Authorized active validation
 ↓
Correlation
 ↓
Reporting
```

## Record types

```text
A     IPv4
AAAA  IPv6
MX    Mail
NS    Nameserver
CNAME Alias
TXT   Text/policy/verification
SOA   Zone authority metadata
PTR   Reverse DNS
SRV   Service location
```

## Tools

```text
Search engines → indexed public information
Shodan         → observed Internet services
WHOIS/RDAP     → registration/allocation
dig            → DNS
nslookup       → DNS
traceroute     → path
Maltego        → relationships
Recon-ng       → modular recon
AI             → analysis/automation, not truth
```

## Golden rules

1. Scope first.
2. Passive before active when appropriate.
3. Public does not mean harmless.
4. A finding is not automatically a vulnerability.
5. Validate important claims.
6. Keep evidence and timestamps.
7. Protect sensitive information.
8. Never confuse AI output with verified evidence.
