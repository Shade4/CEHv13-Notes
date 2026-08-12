# 01 — Footprinting Concepts

## Footprinting methodology

A structured methodology prevents random browsing.

### Phase 1 — Scope

Write down:

- Organization/domain
- IP ranges
- Applications
- Employees/roles if explicitly in scope
- Third parties
- Time window
- Allowed techniques
- Prohibited techniques
- Evidence requirements

### Phase 2 — Organization discovery

Identify:

- Official names
- Alternative names
- Subsidiaries
- Locations
- Business units
- Technology partners

### Phase 3 — Internet presence

Map:

- Domains
- Subdomains
- Public applications
- DNS infrastructure
- IP ranges
- Email infrastructure

### Phase 4 — Technology discovery

Look for:

- Web servers
- Frameworks
- CMS platforms
- CDNs
- Hosting/cloud providers
- Mail platforms
- Security products that are intentionally exposed

### Phase 5 — Human and document OSINT

Research:

- Public employees
- Job advertisements
- Public documents
- Press releases
- Presentations
- Technical blogs
- Public code
- Social profiles

### Phase 6 — Correlation

Connect individual facts.

Example:

```text
Company
 ├── Domain
 │    ├── DNS
 │    ├── Subdomains
 │    └── Mail
 ├── IP ranges
 │    └── Hosting/provider
 ├── Employees
 │    └── Roles/technology mentions
 └── Public documents
      └── Technology clues
```

### Phase 7 — Validation

Do not assume two similarly named assets belong to the same organization.

Validate ownership through:

- Registration information
- Official sources
- DNS relationships
- Certificate information
- Corporate documentation
- Multiple independent sources

## Information leakage

Information leakage occurs when an organization unintentionally reveals information that could assist an attacker.

Examples:

- Internal hostnames in public documents
- Detailed server headers
- Debug information
- Metadata containing usernames
- Old documents
- Exposed configuration files
- Public source-code secrets
- Internal email addresses

## What footprinting can and cannot prove

Footprinting can reveal:

- What appears to exist
- What information is public
- What technologies are associated with assets
- What infrastructure relationships appear likely

Footprinting alone generally cannot prove:

- That an identified system is vulnerable
- That a credential is still valid
- That a hostname is currently active
- That a person is still employed
- That a third-party asset is authorized for testing

Those require validation.

## Exam memory trick

**Passive = observe. Active = interact.**

The boundary is about **interaction with the target**, not whether the information itself is publicly available.
