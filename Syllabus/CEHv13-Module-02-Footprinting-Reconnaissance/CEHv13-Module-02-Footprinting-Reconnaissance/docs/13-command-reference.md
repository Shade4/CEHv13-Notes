# 13 — Command Reference

> Use only against systems you own or have explicit authorization to assess.

## DNS

### A record

```bash
dig example.com A
```

### AAAA

```bash
dig example.com AAAA
```

### MX

```bash
dig example.com MX
```

### NS

```bash
dig example.com NS
```

### TXT

```bash
dig example.com TXT
```

### SOA

```bash
dig example.com SOA
```

### Reverse DNS

```bash
dig -x 93.184.216.34
```

### `nslookup`

```bash
nslookup example.com
nslookup -type=MX example.com
nslookup -type=NS example.com
```

## WHOIS

```bash
whois example.com
```

```bash
whois 93.184.216.34
```

## Traceroute

Linux:

```bash
traceroute example.com
```

Windows:

```powershell
tracert example.com
```

## Search engines

```text
site:example.com
site:example.com filetype:pdf
site:example.com intitle:"security"
site:example.com inurl:docs
site:example.com "technology term"
```

## DNS zone-transfer concept

Authorized lab only:

```bash
dig AXFR example.com @ns1.example.com
```

## Tooling checklist

Before executing:

```text
[ ] Is the target explicitly in scope?
[ ] Is this technique authorized?
[ ] Could it affect availability?
[ ] Could it collect personal/sensitive data?
[ ] Do I know where the evidence will be stored?
[ ] Is the command necessary?
```
