# 00 — Module Overview

## 1. What is reconnaissance?

Reconnaissance is the information-gathering stage performed before deeper security assessment.

Imagine assessing a large organization. Before testing anything, you want to know:

- What company or system is in scope?
- What domains belong to it?
- Which subdomains are public?
- What IP ranges are associated with it?
- Which technologies are visible?
- What locations and business units exist?
- What public documents mention the organization?
- Which employees or roles are publicly associated with it?
- What DNS infrastructure is visible?
- What public email addresses exist?
- What systems appear to be exposed to the Internet?

The objective is not "collect everything." The objective is to collect **relevant, trustworthy information that improves the security assessment**.

## 2. Footprinting

Footprinting is the process of building a profile or blueprint of a target from gathered information.

A useful footprint can contain:

### Organization information

- Legal/business names
- Offices and locations
- Employees and roles
- Contact information
- Partners
- Subsidiaries
- Products
- Technology vendors
- Public documents
- News and press releases
- Patents and trademarks

### Network information

- Domains
- Subdomains
- IP addresses
- Network blocks
- DNS records
- Name servers
- Mail servers
- Public-facing services
- Network ownership/registration information
- Routing/path information

### System information

- Operating-system clues
- Web-server clues
- Application technologies
- Software versions when legitimately exposed
- Public service banners
- Cloud/service-provider indicators

### Security-relevant information

- Accidentally exposed documents
- Public configuration information
- Sensitive metadata
- Credential exposure
- Weak security policies visible from public sources
- Third-party relationships that affect the attack surface

## 3. Passive vs active reconnaissance

### Passive reconnaissance

The tester obtains information without directly probing target-controlled systems.

Examples:

- Search engines
- Public web pages
- Public DNS information
- Public registration records
- Public social profiles
- Public news
- Public repositories
- Public certificate information
- Public documents

Advantages:

- Lower chance of triggering target-side alerts
- Often low risk to target systems
- Useful for early mapping

Limitations:

- Data can be stale
- Data can be incomplete
- Search engines may index old content
- Attribution and ownership may require validation

### Active reconnaissance

The tester interacts with target infrastructure.

Examples:

- DNS queries against authoritative infrastructure
- Traceroute
- Service discovery
- Banner collection
- Authorized network probing

Advantages:

- Can validate whether something is currently reachable
- Can provide technical information not present in public sources

Risks:

- More detectable
- Can create logs
- Can accidentally affect systems
- Requires explicit scope and authorization

## 4. Reconnaissance workflow

```text
Define scope
    ↓
Identify target names
    ↓
Collect passive OSINT
    ↓
Correlate domains / people / technologies
    ↓
Research WHOIS / IP ownership
    ↓
Map DNS
    ↓
Map public network paths
    ↓
Analyze email/document metadata
    ↓
Validate selected findings with authorized active techniques
    ↓
Prioritize findings
    ↓
Document evidence
    ↓
Report
```

## 5. The golden rule of reconnaissance

**A finding is not automatically a vulnerability.**

Example:

Finding:
> A company uses a public cloud provider.

That is information.

Potential security issue:
> A public storage resource exposes sensitive internal documents without authorization.

The second finding requires evidence and context.

## 6. Data quality

Every finding should ideally have:

- Source
- URL/tool
- Timestamp
- Target
- Evidence
- Confidence
- Whether it was passive or active
- Whether it was verified
- Security relevance

A useful confidence model:

| Confidence | Meaning |
|---|---|
| High | Confirmed by multiple independent sources or directly verified within scope |
| Medium | Strong evidence from one reliable source |
| Low | Weak, stale, indirect, or unverified evidence |

## 7. Reconnaissance vs scanning vs enumeration

These are commonly confused.

### Reconnaissance

Broad information gathering.

### Scanning

Finding reachable hosts, ports, and services by probing.

### Enumeration

Extracting more detailed information from an identified service or system.

A simple sequence is:

```text
Recon → Scanning → Enumeration → Vulnerability Analysis → Exploitation (if authorized)
```

Not every engagement follows this exact sequence, but it is a useful learning model.

## 8. Threats created by excessive public information

Public information can enable:

- Targeted phishing
- Password-reset abuse attempts
- Employee impersonation
- Infrastructure targeting
- Vendor targeting
- Physical-security attacks
- Corporate espionage
- Privacy loss
- Discovery of outdated infrastructure
- Identification of technologies to research for known weaknesses

The defensive objective is **not to hide everything**. Organizations need public information. The objective is to minimize unnecessary exposure and protect information that does not need to be public.
