# 07 — Network and Email Footprinting

## Network footprinting

Network footprinting attempts to understand the public network presence of a target.

Possible information:

- Network ranges
- Public IP addresses
- Routing relationships
- Network providers
- Gateways
- Paths to services
- Public-facing infrastructure

## Traceroute

Traceroute helps show the path packets appear to take toward a destination.

It works by manipulating hop limits/TTL values so intermediate routers can generate responses.

### Linux

```bash
traceroute example.com
```

### Windows

```powershell
tracert example.com
```

### What traceroute can show

- Approximate path
- Intermediate routers that respond
- Network/provider transitions
- Latency observations

### What traceroute cannot guarantee

- A complete path
- Exact physical locations
- That every hop is visible
- That displayed names are accurate
- That the path is stable

Routers may filter, rate-limit, or hide responses.

## Network range research

A public organization may own or use:

- Individual IPs
- CIDR ranges
- Autonomous systems
- Cloud allocations
- Third-party hosting

Do not treat an entire provider's network as the target.

## Email footprinting

Email reconnaissance can reveal:

- Sender infrastructure
- Receiving servers
- Message routing
- Authentication results
- Client/application information
- Timestamps
- Sometimes IP information, depending on the mail system

## Email headers

Important header fields include:

- `From`
- `To`
- `Date`
- `Subject`
- `Received`
- `Message-ID`
- `Reply-To`
- `Return-Path`
- Authentication-related results

### `Received` headers

Mail servers add `Received` headers as a message moves through infrastructure.

Reading them from the newest hop toward older hops can help reconstruct the route.

Be careful:

- Some headers can be forged.
- Modern email systems may hide client IPs.
- Relays and security gateways can alter the visible path.

## Email authentication

### SPF

Sender Policy Framework helps domain owners publish which servers are authorized to send mail for a domain.

### DKIM

DomainKeys Identified Mail uses cryptographic signatures to provide message/domain integrity and authentication signals.

### DMARC

Domain-based Message Authentication, Reporting, and Conformance builds policy around SPF/DKIM alignment and handling.

## Defensive lessons

Organizations should:

- Configure SPF carefully
- Deploy DKIM
- Publish appropriate DMARC policy
- Avoid unnecessary internal details in headers
- Use secure mail gateways
- Train employees
- Monitor spoofing and impersonation attempts

## Exam distinction

**Network footprinting:** understand network ranges, paths, and public infrastructure.

**Email footprinting:** understand mail infrastructure and message metadata.

**Traceroute:** path discovery/observation.

**DNS:** name/resource mapping.
