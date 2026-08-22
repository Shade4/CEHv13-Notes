# Module 2: Footprinting and Reconnaissance
## Part E — Whois, IP Geolocation, and DNS Footprinting

[← Back to Part D: Footprinting Through Social Networking Sites](04-footprinting-through-social-networking-sites.md) | [Next: Network and Email Footprinting →](06-network-and-email-footprinting.md)

---

## Table of Contents

1. [Whois Lookup](#whois-lookup)
2. [Whois Lookup Tools](#whois-lookup-tools)
3. [Finding IP Geolocation Information](#finding-ip-geolocation-information)
4. [DNS Footprinting](#dns-footprinting)
5. [DNS Interrogation Tools](#dns-interrogation-tools)
6. [DNS Lookup with AI](#dns-lookup-with-ai)
7. [Reverse DNS Lookup](#reverse-dns-lookup)
8. [Quick-Reference Summary](#quick-reference-summary)

---

## Whois Lookup

**Whois** is a query/response protocol used to look up the registered users or assignees of an internet resource — a domain name, an IP address block, or an autonomous system. It listens on port 43 (TCP). **Regional Internet Registries (RIRs)** maintain the actual Whois databases, which hold the personal information of domain owners: registration and expiry dates, name servers, contact details, and more.

### Three Whois Data Models

| Model | How It Works |
|---|---|
| **Thick Whois (Distributed Model)** | Stores the *complete* Whois information from every registrar for a given data set |
| **Thin Whois (Centralized Model)** | Stores only the name of the Whois server for a domain's registrar, which in turn holds the full details |
| **Decentralized Whois** | Stores complete Whois information with multiple independent entities managing the database |

### What a Whois Query Returns

- Domain name details and registrar
- Contact details of the domain owner
- Domain name servers
- NetRange
- When the domain was created, its expiry date, and last-updated date
- Domain status (available, registered, or suspended)
- IP address information

By querying a Whois database, an attacker can build a map of the organization's network, mislead domain owners through social engineering, and pull internal network details — all without ever touching the target directly.

### The 5 Regional Internet Registries (RIRs)

- **ARIN** — American Registry for Internet Numbers (arin.net)
- **AFRINIC** — African Network Information Center (afrinic.net)
- **APNIC** — Asia Pacific Network Information Center (apnic.net)
- **RIPE** — Réseaux IP Européens Network Coordination Centre (ripe.net)
- **LACNIC** — Latin American and Caribbean Network Information Center (lacnic.net)

---

## Whois Lookup Tools

- **whois.domaintools.com** and **whois.tamos.com** — run a Whois lookup by entering the target domain or IP address directly. A typical result (a "Whois Record") includes the registrant, registrar, registrar status, key dates, name servers, tech contact, IP address, IP location, ASN, domain status, and historical change counts (IP history, registrar history, hosting history).
- **Batch IP Converter** (sabsoft.com) — provides information about an IP address, hostname, or domain, including country, state/province, city, phone/fax numbers, and administrative/technical-support contacts. It supports Internationalized Domain Names (IDNs) and IPv6 addresses.
- **WHOIS Domain Lookup** and **Active Whois** — additional dedicated Whois lookup tools attackers use on a target domain.

Attackers typically run more than one of these tools, since no single tool reliably surfaces every piece of available information.

---

## Finding IP Geolocation Information

**IP geolocation** identifies where a target actually is: country, region/state, city, ZIP/postal code, time zone, connection speed, ISP (hosting company), domain name, IDD country code, area code, weather station code and name, mobile carrier, and elevation.

Once an attacker has this, they can layer on social engineering, physical surveillance, and non-technical attacks (dumpster diving, posing as a technical expert). If they geolocate the victim precisely enough, they can even set up a compromised web server *near* the victim's physical location, or tailor malware to that specific region.

### IP Geolocation Lookup Tools

- **IP2Location** (ip2location.com) — identifies a visitor's country, region, city, coordinates, time zone, connection speed, ISP, domain, IDD/area code, weather station, mobile carrier, elevation, usage type, address type, and ASN, using a proprietary geolocation database (e.g., the IP2Location DB26 database).

---

## DNS Footprinting

After Whois records are collected, the next step in the footprinting methodology is **DNS footprinting** — gathering information about DNS servers, DNS records, and the server types the target organization runs. This reveals the hosts connected in the target's network and creates further exploitation opportunities. DNS zone data specifically includes domain names, computer names, and IP addresses — exactly the raw material an attacker uses to identify key hosts before layering on social engineering.

### DNS Record Types

| Record Type | Description |
|---|---|
| **A** | Points to a host's IP address |
| **AAAA** | Points to a host's IPv6 address |
| **MX** | Points to the domain's mail server |
| **NS** | Points to the host's name server |
| **CNAME** | Canonical naming — allows aliases to a host |
| **SOA** | Indicates authority for a domain |
| **SRV** | Service records |
| **PTR** | Maps an IP address to a hostname |
| **RP** | Responsible person |
| **HINFO** | Host information record — includes CPU type and OS |
| **TXT** | Unstructured text records |

---

## DNS Interrogation Tools

Attackers query DNS servers using dedicated interrogation tools to retrieve the record structure containing information about the target DNS — extracting IP address ranges via IP routing lookup. If a target network allows unknown, unauthorized users to transfer DNS zone data, obtaining this information becomes trivial for an attacker.

- **SecurityTrails** (securitytrails.com) — an advanced DNS enumeration tool that builds a DNS map of a target domain. It enumerates both current and historical DNS records (A, AAAA, NS, MX, SOA, TXT) and can brute-force existing subdomains.
- **Fierce** (github.com) — a DNS reconnaissance tool for scanning and collecting information about a target domain, enumerating subdomains, and identifying non-contiguous IP spaces linked to specified domains/subdomains.
- **DNSChecker**, **zdns**, **DNSdumpster.com** — additional DNS interrogation tools used for the same purpose.

### Fierce — Example Commands

```bash
# Basic scan on the target domain
fierce --domain certifiedhacker.com

# Scan for subdomains containing specific words
fierce --domain certifiedhacker.com --subdomains write admin mail

# Scan domains near discovered records (contiguous IP blocks within a range of 10)
fierce --domain certifiedhacker.com --subdomains mail --traverse 10

# Attempt an HTTP connection on discovered domains
fierce --domain certifiedhacker.com --subdomains mail --connect

# Full detailed scan of all discovered records
fierce --domain certifiedhacker.com --wide
```

The `--traverse 10` option instructs Fierce to search for contiguous blocks of IPs within a range of 10 around any discovered record.

---

## DNS Lookup with AI

Attackers increasingly pair generative AI with DNS enumeration to skip the manual setup work. A prompt to an AI shell assistant like **ShellGPT** — for example, *"Install and use DNSRecon to perform DNS enumeration on the target domain www.certifiedhacker.com"* — can get translated automatically into a working install-and-run pipeline:

```bash
sudo apt-get update && sudo apt-get install -y dnsrecon && dnsrecon -d certifiedhacker.com -t std
```

**Command breakdown:**
- `sudo apt-get update` — refreshes package lists for upgrades and new installs
- `&&` — chains commands to run sequentially
- `sudo apt-get install -y dnsrecon` — installs DNSRecon, auto-confirming prompts
- `dnsrecon -d certifiedhacker.com -t std` — runs standard DNS enumeration against the target domain

A run like this typically surfaces the SOA record, NS records with BIND version info, MX records, the A record, and a TXT/SPF record — followed by a deeper enumeration pass that pulls SRV records (e.g., `_caldav._tcp`, `_autodiscover._tcp`) tied to the domain's mail and calendar infrastructure.

---

## Reverse DNS Lookup

A **reverse DNS lookup** goes the opposite direction of a standard DNS lookup — instead of resolving a domain name to an IP address, it resolves an IP address (or a range of IPs) back to a domain name by locating a **PTR record**.

### Tools

- **DNSRecon** (github.com) — supports reverse lookups by brute force across an IP range:
  ```bash
  dnsrecon -r 162.241.216.0-162.241.216.255
  ```
  The `-r` option specifies the first-to-last IP range for the brute-force reverse lookup, returning any PTR records found for hosts across that range.
- **Reverse Lookup** (mxtoolbox.com) — a web-based tool that performs a reverse IP lookup by taking a single IP address and returning its associated domain name (via its PTR record), along with TTL and record-status information.
- **puredns**, **Reverse IP Domain Check**, **Reverse IP Lookup** — additional tools that serve the same purpose: turning a known IP (or IP range) into the domain name(s) hosted there.

---

## Quick-Reference Summary

- **Whois** = port-43 protocol for looking up domain/IP registration data, served by 5 RIRs (ARIN, AFRINIC, APNIC, RIPE, LACNIC) under 3 data models (Thick, Thin, Decentralized)
- **IP geolocation** turns an IP into a real-world location — country down to weather station and elevation — enabling physical/social attacks
- **DNS footprinting** = extracting the 11 standard record types (A, AAAA, MX, NS, CNAME, SOA, SRV, PTR, RP, HINFO, TXT) via tools like SecurityTrails and Fierce
- **AI-assisted DNS recon** (e.g., ShellGPT + DNSRecon) automates the install-and-enumerate workflow from a single natural-language prompt
- **Reverse DNS lookup** flips the direction — IP → domain name — via PTR records, using tools like DNSRecon (`-r`) and MxToolbox's Reverse Lookup

---

*Part of the CEH Module 2 study series — continues in [Part F: Network and Email Footprinting](06-network-and-email-footprinting.md).*
