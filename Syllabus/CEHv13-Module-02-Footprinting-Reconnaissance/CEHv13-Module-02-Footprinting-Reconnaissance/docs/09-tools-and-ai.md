# 09 — Footprinting Tools and AI

## Maltego

Maltego is a graphical investigation and link-analysis platform.

Its core idea is:

```text
Entity → Relationships → Transformations → More entities
```

Examples of entities:

- Domains
- IP addresses
- DNS records
- Organizations
- People
- Email addresses

The value is **relationship analysis**, not simply collecting a list of facts.

## Recon-ng

Recon-ng is a modular reconnaissance framework.

Conceptually:

```text
Workspace
  ↓
Modules
  ↓
Data collection
  ↓
Database
  ↓
Correlation/reporting
```

Use modules only within the engagement's authorized scope.

## DNS tools

Common utilities:

- `dig`
- `nslookup`
- `host`

## WHOIS/RDAP

Useful for:

- Registration research
- Allocation research
- Nameserver information
- Ownership validation

## Search tools

- Search engines
- GHDB
- Shodan
- Internet archives
- Public certificate information

## AI-assisted OSINT

AI can help with:

- Query generation
- Search-term expansion
- Document summarization
- Entity extraction
- Deduplication
- Timeline construction
- Relationship mapping
- Report drafting
- Hypothesis generation

### AI must not become the source of truth

AI can hallucinate.

Therefore:

```text
AI hypothesis
      ↓
Original source
      ↓
Human validation
      ↓
Evidence
      ↓
Finding
```

## Safe AI workflow

1. Define the target and scope.
2. Feed AI only information you are permitted to process.
3. Ask it to identify relationships.
4. Ask for source citations.
5. Verify every important claim.
6. Remove sensitive information that is not needed.
7. Store evidence separately.
8. Document uncertainty.

## Automation

Automation is useful when the task is repetitive.

Examples:

- Querying DNS record types
- Normalizing domains
- Building structured notes
- Generating reports
- Comparing observations over time

Avoid uncontrolled scanning.

## Example: DNS baseline script

See:

`scripts/dns_baseline.py`

The script is intentionally limited to basic DNS lookups and is not a port scanner.

## Tool-selection matrix

| Goal | Suitable category |
|---|---|
| Public web research | Search engine |
| Internet-exposed service research | Shodan-like search engine |
| Registration research | WHOIS/RDAP |
| DNS mapping | dig/nslookup |
| Visual relationship mapping | Maltego |
| Recon workflow automation | Recon-ng |
| Path observation | traceroute/tracert |
| Email metadata | Header analyzer |
| Summarization/correlation | AI with human verification |
