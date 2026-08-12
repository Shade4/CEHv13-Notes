# Lab 02 — DNS and Registration Research

## Objective

Understand how registration information and DNS records complement each other.

## Prerequisite

Use a domain you own or a training domain.

## Commands

```bash
whois example.com
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
dig example.com SOA
```

Reverse lookup on an IP that is in your scope:

```bash
dig -x 203.0.113.10
```

## Questions

1. Which nameservers are authoritative?
2. Which mail servers are published?
3. Are IPv4 and IPv6 addresses present?
4. Are there CNAME relationships?
5. What TXT records exist?
6. Does reverse DNS provide a meaningful hostname?
7. Which information is verified and which is inferred?

## Optional authorized zone-transfer lab

Use a deliberately vulnerable DNS lab, not a random Internet domain.

```bash
dig AXFR lab.example @ns1.lab.example
```

## Expected lesson

DNS records are building blocks for an infrastructure map.
