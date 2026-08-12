# 05 — WHOIS and IP Research

## What is WHOIS?

WHOIS is a protocol/service historically used to query registration information for Internet resources.

Today, many registration systems use web-based RDAP services, but the learning objective remains similar:

> Determine registration and allocation information associated with an Internet resource.

## What can registration research reveal?

Depending on privacy controls and registry policies:

- Registrar
- Registration dates
- Nameservers
- Domain status
- Registrant information in some cases
- Organization/contact information in some cases
- Registration/registry relationships

Privacy services may intentionally hide personal details.

## Why WHOIS matters in reconnaissance

Registration information can help answer:

- Who manages a domain?
- Which registrar is involved?
- Which nameservers are associated?
- Is the domain likely connected to the target?
- What organization or allocation is associated with an IP range?

## IP ownership

An IP address can be associated with:

- ISP
- Cloud provider
- Hosting company
- Organization
- Autonomous system

An IP being hosted by a provider does not automatically mean the provider is the target.

## Safe workflow

```text
Domain
 ↓
Registration/RDAP
 ↓
Nameservers
 ↓
DNS
 ↓
IP addresses
 ↓
IP registration/ASN
 ↓
Ownership validation
```

## Example command

On a system where `whois` is installed:

```bash
whois example.com
```

For an IP:

```bash
whois 93.184.216.34
```

These examples are for learning. Replace the target only when it is in your authorized scope.

## IP geolocation

Geolocation databases can provide approximate:

- Country
- Region
- City
- Provider

Geolocation is not exact physical location.

It can be wrong because:

- IPs are mobile
- VPNs exist
- Cloud infrastructure is distributed
- Databases are stale
- Traffic may pass through proxies/CDNs

## RDAP

Registration Data Access Protocol is the modern standards-based approach to registration data.

Conceptually:

```text
Domain/IP
  ↓
RDAP service
  ↓
Registration objects
  ↓
Registrar/registry/organization information
```

## Exam distinction

**WHOIS/registration research = ownership/registration intelligence.**

**DNS = name-to-resource information.**

They are related but not interchangeable.
