# 06 — DNS Footprinting

DNS translates names into information used to locate services.

For reconnaissance, DNS can reveal the structure of an organization's public naming system.

## Important DNS record types

| Record | Purpose |
|---|---|
| A | IPv4 address |
| AAAA | IPv6 address |
| MX | Mail exchange server |
| NS | Authoritative nameserver |
| CNAME | Alias to another name |
| TXT | Text data; commonly used for verification and email security policies |
| SOA | Start of Authority information |
| PTR | Reverse DNS mapping |
| SRV | Service location information |

## A record

Example:

```text
app.example.com → 203.0.113.10
```

The A record maps a hostname to an IPv4 address.

## AAAA record

Maps a hostname to an IPv6 address.

## MX record

Shows which servers receive email for a domain.

```text
example.com
  ↓ MX
mail.example.com
```

## NS record

Identifies authoritative nameservers.

## CNAME

Creates an alias:

```text
portal.example.com
       ↓ CNAME
app.provider.example
```

This can reveal relationships with third-party providers.

## TXT records

TXT records can contain:

- Domain verification data
- SPF policies
- Service verification
- Other administrative text

Do not assume every TXT record is a security weakness.

## SOA

SOA contains authoritative-zone metadata such as:

- Primary nameserver
- Responsible-party field
- Serial number
- Refresh/retry/expiry values

## Reverse DNS

PTR records can map an IP back to a hostname.

Conceptually:

```text
IP address
   ↓ PTR
hostname
```

Reverse DNS is useful for validating naming conventions and infrastructure relationships.

## Basic commands

### `nslookup`

```bash
nslookup example.com
nslookup -type=MX example.com
nslookup -type=NS example.com
```

### `dig`

```bash
dig example.com
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
```

### Reverse lookup

```bash
dig -x 93.184.216.34
```

## DNS zone transfer

A zone transfer can replicate DNS zone information between DNS servers.

A misconfigured authoritative DNS server may permit unauthorized transfer to arbitrary clients.

A successful unauthorized transfer can reveal many records at once.

### Defensive test

Only test this on infrastructure you own or are explicitly authorized to assess.

A conceptual test is:

```bash
dig AXFR example.com @ns1.example.com
```

Do not run it against unrelated domains.

## DNS footprinting methodology

```text
Domain
 ↓
NS
 ↓
SOA
 ↓
A/AAAA
 ↓
MX
 ↓
TXT
 ↓
CNAME
 ↓
PTR
 ↓
Correlate infrastructure
```

## DNS countermeasures

- Restrict zone transfers to authorized secondary servers
- Monitor DNS changes
- Remove stale records
- Avoid unnecessary internal naming exposure
- Use appropriate DNS security controls
- Separate internal and external DNS where appropriate
- Review third-party DNS records
- Protect DNS management accounts

## Key exam distinction

**Forward DNS:** name → address/resource.

**Reverse DNS:** address → name.

**Zone transfer:** replication of DNS zone data between DNS servers.
