# Module 03 — Authorized Lab Guide

This guide turns the theory into a small isolated practice environment.

## Recommended lab

Use two VMs:

```text
VM-1: Kali/Parrot or another Linux security workstation
VM-2: intentionally exposed training VM
Network: host-only / internal network
```

A third VM running Windows can be added for OS discovery and SMB/NSE practice.

## Step 1 — Verify connectivity

```bash
ip addr
ip route
ping -c 3 <LAB-IP>
```

## Step 2 — Host discovery

```bash
nmap -sn <LAB-NETWORK>/24
sudo nmap -PR <LAB-NETWORK>/24
sudo nmap -PS22,80,443 <LAB-IP>
sudo nmap -PA80,443 <LAB-IP>
```

Record:

- Which hosts respond.
- Which discovery method found each host.
- Whether ARP behavior differs from routed discovery.

## Step 3 — TCP scans

```bash
nmap -sT -p 1-1000 <LAB-IP>
sudo nmap -sS -p 1-1000 <LAB-IP>
sudo nmap -sF <LAB-IP>
sudo nmap -sN <LAB-IP>
sudo nmap -sX <LAB-IP>
sudo nmap -sA <LAB-IP>
```

Compare the results rather than simply collecting screenshots.

## Step 4 — UDP

```bash
sudo nmap -sU --top-ports 25 <LAB-IP>
```

Pick a few known UDP services in your lab and compare open/closed/filtered behavior.

## Step 5 — Services and versions

```bash
nmap -sV <LAB-IP>
```

Create a table:

| Port | State | Service | Version | Notes |
|---:|---|---|---|---|
| 22 | | | | |
| 80 | | | | |
| 443 | | | | |

## Step 6 — OS detection

```bash
sudo nmap -O <LAB-IP>
```

Then capture traffic in Wireshark and inspect:

- IP TTL.
- TCP window.
- TCP options.
- DF bit.

Do not expect a single packet field to prove the OS.

## Step 7 — NSE

```bash
nmap --script-help "*"
nmap --script default <LAB-IP>
```

Then try a targeted script appropriate to your lab service.

## Step 8 — Version detection at scale

Create `targets.txt`:

```text
<LAB-IP-1>
<LAB-IP-2>
<LAB-IP-3>
```

Run:

```bash
nmap -sV -iL targets.txt -oA module03-services
```

## Step 9 — Packet-analysis exercise

1. Start Wireshark on the lab interface.
2. Capture a SYN scan.
3. Filter for TCP.
4. Identify SYN, SYN/ACK and RST.
5. Repeat with an ACK scan.
6. Compare TTL and window fields.
7. Write your own explanation of the observed state transitions.

## Step 10 — Defensive exercise

Put a firewall between the scanner and the training VM.

Repeat:

```bash
nmap -sS <LAB-IP>
nmap -sA <LAB-IP>
nmap -sU --top-ports 25 <LAB-IP>
```

Record what changes when ports are blocked versus when a host is actually offline.

## Step 11 — Detection

If you have a Snort/Suricata/SIEM lab, repeat a scan and observe the alerts.

Look for:

- repeated SYNs,
- wide port spread,
- sequential probes,
- ICMP sweep behavior,
- UDP bursts,
- malformed/fragmented packets.

## Step 12 — Documentation exercise

For every scan, record:

```text
Date/time
Source VM
Target
Network location
Scan type
Command
Observed state
Interpretation
Potential false positives
Defensive controls observed
```

## Safety

Do not perform spoofing, fragmented traffic, decoy scans or high-rate probing against public systems. Use a closed lab where packet behavior and side effects are fully controlled.
