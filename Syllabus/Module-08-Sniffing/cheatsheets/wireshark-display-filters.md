# Cheat Sheet — Wireshark Display Filters

Every display filter referenced in this module, consolidated into one quick-lookup table. See [07 — Sniffing Tools](../07-sniffing-tools.md) for full context.

## Protocol filters

| Filter | Shows |
|---|---|
| `arp` | Only ARP traffic |
| `http` | Only HTTP traffic |
| `tcp` | Only TCP traffic |
| `udp` | Only UDP traffic |
| `dns` | Only DNS traffic |
| `ip` | Only IP traffic |

## Port / host filters

| Filter | Shows |
|---|---|
| `tcp.port==23` | Traffic on TCP port 23 (Telnet) |
| `ip.addr==192.168.1.100` | Traffic to/from a specific machine |
| `ip.addr==192.168.1.100 && tcp.port==23` | Telnet traffic to/from a specific machine |
| `ip.addr == 10.0.0.4 or ip.addr == 10.0.0.5` | Traffic involving either of two IPs |
| `ip.addr == 10.0.0.4` | Traffic to/from a single IP |

## Compound / advanced filters

| Filter | Shows |
|---|---|
| `ip.dst == 10.0.1.50 && frame.pkt_len > 400` | Packets to a destination IP, larger than 400 bytes |
| `ip.addr == 10.0.1.12 && icmp && frame.number > 15 && frame.number < 30` | ICMP packets to/from an IP, within a specific frame-number window |
| `ip.src==205.153.63.30 or ip.dst==205.153.63.30` | Traffic where a given IP is either the source or the destination |
| `tcp.flags.reset==1` | All TCP RST (reset) packets |
| `udp contains 33:27:58` | UDP packets containing the hex byte sequence `0x33 0x27 0x58` anywhere in the payload |
| `http.request` | All HTTP GET/request lines |
| `tcp.analysis.retransmission` | All TCP retransmissions in the capture |
| `tcp contains traffic` | TCP packets whose payload contains the literal string "traffic" |
| `!(arp or icmp or dns)` | Excludes ARP, ICMP, and DNS noise — useful for isolating "real" application traffic |
| `tcp.port == 4000` | Traffic with 4000 as either the source or destination TCP port |
| `tcp.port eq 25 or icmp` | Only SMTP (port 25) and ICMP traffic |
| `ip.src==192.168.0.0/16 and ip.dst==192.168.0.0/16` | Only intra-LAN traffic (both ends in the 192.168.x.x range) — excludes internet-bound traffic |
| `ip.src != xxx.xxx.xxx.xxx && ip.dst != xxx.xxx.xxx.xxx && sip` | SIP traffic, excluding a specific pair of IP addresses |

## Practical recipes

- **Hunt for cleartext credentials:** `http.request.method == "POST"`, then right-click → Follow → HTTP Stream.
- **Find a Telnet session end-to-end:** `tcp.port==23`, select any packet in the conversation, then Analyze → Follow → TCP Stream.
- **Spot ARP spoofing in a capture:** `arp.duplicate-address-detected` or watch for repeated `arp.opcode==2` (reply) frames from the same IP with alternating MAC addresses.
- **Isolate one host's activity on a shared segment:** `ip.addr == <host>` combined with `!(arp or icmp or dns)` to strip out background chatter.
