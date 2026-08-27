# Cheatsheet — Tools, Links & Commands

Every tool referenced across this repo, grouped by purpose, with official sources and the core
commands to use each. **Authorized use only** — see the Legal & Ethical Use Notice in the repo
[`README.md`](../README.md).

---

## Attack Tools (recognition/detection reference — do not run outside an authorized lab)

| Tool | Purpose | Source |
|---|---|---|
| ISB ("I'm So Bored") | HTTP/UDP/TCP/ICMP flood GUI tool + recon commands | https://sourceforge.net |
| UltraDDOS-v2 | Simple GUI DDoS tool (IP + port + packet count) | https://sourceforge.net |
| High Orbit Ion Cannon (HOIC) | Volunteer-style HTTP flood tool with booster scripts | https://sourceforge.net |
| Low Orbit Ion Cannon (LOIC) | Simple TCP/UDP/HTTP stress tool, popular in hacktivist campaigns | https://sourceforge.net |
| HULK | Obfuscated, unique-per-request HTTP GET flood tool | https://github.com |
| Slowloris | Partial-HTTP-header connection-exhaustion tool | https://github.com |
| UFONet | Abuses open redirects on third-party sites to reflect traffic at a target | https://ufonet.03c8.net |
| Packet Flooder Tool | General-purpose raw packet flood generator (NetScanTools suite) | https://www.netscantools.com |

## Honeypot / Deception Tools

| Tool | Source |
|---|---|
| Blumira | https://www.blumira.com |
| KFSensor | https://www.kfsensor.net |
| Valhala Honeypot | https://sourceforge.net |
| Cowrie | https://github.com |
| HoneyHTTPD | https://github.com |
| StingBox | https://www.stingbox.com |

## Advanced DDoS Protection Appliances

| Appliance | Source |
|---|---|
| FortiDDoS (200F/1500E/1500F/2000E/VM series) | https://www.fortinet.com |
| Check Point Quantum DDoS Protector | https://www.checkpoint.com |
| Huawei AntiDDoS1000 | https://e.huawei.com |
| A10 Thunder TPS | https://a10networks.com |

## DoS/DDoS Protection Tools (software)

| Tool | Source |
|---|---|
| Anti DDoS Guardian | https://beethink.com |
| DDoS-GUARD | https://ddos-guard.net |
| DOSarrest | https://www.dosarrest.com |
| Radware DefensePro X | https://www.radware.com |
| Gatekeeper | https://github.com |
| F5 DDoS Attack Protection | https://www.f5.com |

## DoS/DDoS Protection Services (cloud)

| Service | Source |
|---|---|
| Cloudflare | https://www.cloudflare.com |
| Akamai DDoS Protection | https://www.akamai.com |
| Stormwall PRO | https://stormwall.network |
| Imperva DDoS Protection | https://www.imperva.com |
| Nexusguard | https://www.nexusguard.com |
| BlockDoS | https://www.blockdos.net |

---

## Command Reference — Detection

```bash
# Detect an NTP server with monlist enabled (amplification-attack risk) — see 04.2
nmap -sU -pU:123 -Pn -n --script=ntp-monlist <target>

# Quick per-source packet-volume snapshot from a live capture (flood signature check) — see 06
sudo tcpdump -i eth0 -n | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head

# Wireshark display filters for suspected flood traffic
tcp.flags.syn == 1 && tcp.flags.ack == 0        # possible SYN flood
tcp.analysis.retransmission                      # possible retransmission storm

# Baseline live connection counts / bandwidth (before + during a test) — see 10
watch -n1 'ss -s'
sar -n DEV 1 60
```

## Command Reference — Mitigation

### SYN Flood Defense (Linux)
```bash
sudo sysctl -w net.ipv4.tcp_syncookies=1
echo "net.ipv4.tcp_syncookies = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -w net.ipv4.tcp_synack_retries=2
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# iptables SYN rate-limit
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP
```

### ICMP Flood / Smurf / PoD Defense (Linux)
```bash
sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 4 -j ACCEPT
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

### nftables Rate Limiting
```bash
sudo nft add rule inet filter input ct state new limit rate 20/second accept
```

### TCP Intercept — Cisco IOS
```
! Step 1: define what traffic to intercept (protect 10.10.1.0/24)
Router(config)# access-list 101 permit tcp any 10.10.1.0 0.0.0.255

! Step 2: enable TCP intercept using that access list
Router(config)# ip tcp intercept list 101

! Optional: set the mode (intercept = active spoofing defense; watch = passive with 30s timeout)
Router(config)# ip tcp intercept mode {intercept | watch}
```

### Secure Erase / Hosts-File Checks (Pharming-adjacent hardening, cross-reference Module 09)
```bash
cat /etc/hosts
Get-Content C:\Windows\System32\drivers\etc\hosts
```

---

## Command Reference — Authorized Load/Resilience Testing (see `10` for full methodology)

```bash
# HTTP load test
ab -n 10000 -c 100 https://staging.example.com/
wrk -t12 -c400 -d30s https://staging.example.com/

# Controlled SYN/ICMP flood against YOUR OWN lab host only
sudo hping3 -S -p 80 --flood --rand-source 10.10.1.50
sudo hping3 --icmp --flood 10.10.1.50

# Slowloris-style slow-connection test against your own staging server
slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u https://staging.example.com/ -x 24 -p 3
```

---

*All tool links point to official project sources at time of writing. Always verify you're on
the genuine project domain before downloading — attackers have been known to publish trojanized
clones of well-known security tools.*