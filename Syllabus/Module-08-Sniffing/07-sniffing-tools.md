# 07 — Sniffing Tools

## Table of Contents
- [Wireshark](#wireshark)
- [Follow TCP Stream in Wireshark](#follow-tcp-stream-in-wireshark)
- [Wireshark Display Filters](#wireshark-display-filters)
- [Additional Wireshark Filters](#additional-wireshark-filters)
- [Other Sniffing Tools](#other-sniffing-tools)

System administrators use automated tools to monitor their own networks, but attackers misuse the exact same tools to sniff network data. This section covers the tools an attacker (or a defender doing traffic analysis) can use for sniffing.

---

## Wireshark

- **Source:** [wireshark.org](https://www.wireshark.org)

Wireshark lets you capture and interactively browse traffic running on a computer network. It uses **WinPcap**/`libpcap` to capture packets on its own supported interfaces, and can capture live traffic from Ethernet, IEEE 802.11, PPP/HDLC, ATM, Bluetooth, USB, Token Ring, Frame Relay, and FDDI. Captured files can be programmatically edited via the command line, and a rich set of filters can be applied to refine the displayed data.

**Basic capture workflow:**
1. Open Wireshark and select the network interface to capture on (e.g., `eth0`).
2. Start the capture — Wireshark lists every packet with its time, source, destination, protocol, length, and a summary `Info` field.
3. Click any packet to expand its full protocol stack (Frame → Ethernet → IP → TCP/UDP → Application layer) in the lower panes, viewable as hex dump or ASCII.

Attackers use Wireshark to sniff a target network and extract critical information — capturing network traffic and attempting to gain the credentials of a target machine, or monitoring traffic generated from a user's browsing activities to extract confidential information.

### Follow TCP Stream in Wireshark

**"Follow TCP Stream"** displays data from the TCP port the same way the application layer sees it — as a continuous stream rather than individual packets — which is exactly what you need to find passwords sent in a Telnet session or any other unencrypted protocol.

**Steps:**
1. In the packet list, select a TCP packet that's part of the conversation you want to inspect.
2. Go to the **Analyze** menu → **Follow** → **TCP Stream**.
3. Wireshark opens a new window showing all the data for that stream, in the same sequence as the network saw it, and gives you a choice of view format: **ASCII**, **EBCDIC**, hex dump, C array, or raw.

**Example from the courseware:** capturing an HTTP login form submission and following its TCP stream reveals the raw POST body, including a plaintext password field such as:
```
_wpnonce=747d47a6f0&log=admin&pwd=Pa$$w0rd&wp-submit=Log+In&...
```
— the password is fully visible in the reconstructed stream, exactly as it appeared on the wire.

---

## Wireshark Display Filters

**Source:** [wiki.wireshark.org](https://wiki.wireshark.org)

Display filters change *what you see* in an already-captured file (they don't affect what's captured, unlike capture filters).

| Purpose | Filter Example |
|---|---|
| Filter by protocol | `arp`, `http`, `tcp`, `udp`, `dns`, `ip` |
| Monitor a specific port | `tcp.port==23` |
| Monitor a specific machine + port | `ip.addr==192.168.1.100 && tcp.port==23` |
| Filter by multiple IP addresses | `ip.addr == 10.0.0.4 or ip.addr == 10.0.0.5` |
| Filter by a single IP address | `ip.addr == 10.0.0.4` |
| Filter by destination IP + a packet-length threshold | `ip.dst == 10.0.1.50 && frame.pkt_len > 400` |
| Combine IP, protocol, and a frame-number range | `ip.addr == 10.0.1.12 && icmp && frame.number > 15 && frame.number < 30` |
| Filter by source **or** destination IP | `ip.src==205.153.63.30 or ip.dst==205.153.63.30` |

---

## Additional Wireshark Filters

| Filter | What It Shows |
|---|---|
| `tcp.flags.reset==1` | Displays all TCP resets |
| `udp contains 33:27:58` | Sets a filter for the hex values `0x33 0x27 0x58` at any offset in the payload |
| `http.request` | Displays all HTTP GET requests |
| `tcp.analysis.retransmission` | Displays all retransmissions in the trace |
| `tcp contains traffic` | Displays all TCP packets that contain the literal word "traffic" |
| `!(arp or icmp or dns)` | Masks out ARP, ICMP, DNS, or other noisy protocols and shows only the traffic you actually care about |
| `tcp.port == 4000` | Filters for any TCP packet with 4000 as source or destination port |
| `tcp.port eq 25 or icmp` | Displays only SMTP (port 25) and ICMP traffic |
| `ip.src==192.168.0.0/16 and ip.dst==192.168.0.0/16` | Displays only traffic within the LAN (192.168.x.x ↔ 192.168.x.x) — between workstations and servers, excluding anything to/from the internet |
| `ip.src != xxx.xxx.xxx.xxx && ip.dst != xxx.xxx.xxx.xxx && sip` | Filters by a specific protocol (e.g., SIP) while excluding a given pair of IPs |

---

## Other Sniffing Tools

### Capsa Portable Network Analyzer
- **Source:** [colasoft.com](https://www.colasoft.com)
- A portable network performance analysis and diagnostics tool that provides packet capture and analysis capabilities through an easy-to-use interface, letting users protect and monitor networks in a critical business environment.
- An attacker can use this tool to sniff packets from a target network and detect network vulnerabilities.

### OmniPeek
- **Source:** [liveaction.com](https://www.liveaction.com)
- OmniPeek Network Analyzer provides real-time visibility and expert analysis of every part of a target network — it can analyze, drill down, and fix performance bottlenecks across multiple network segments. Analytic plug-ins provide targeted visualization and search abilities within OmniPeek; a Google Maps plug-in enhances the capture window by showing the physical locations of the public IP addresses in captured packets.
- Attackers can use OmniPeek to monitor and analyze target-network traffic in real time, identify the source of that traffic, and attempt to find network loopholes.

### Additional sniffing tools

| Tool | Source |
|---|---|
| RITA (Real Intelligence Threat Analytics) | [github.com](https://github.com) |
| Observer Analyzer | [viavisolutions.com](https://www.viavisolutions.com) |
| PRTG Network Monitor | [paessler.com](https://www.paessler.com) |
| Network Performance Monitor | [solarwinds.com](https://www.solarwinds.com) |
| Xplico | [xplico.org](https://www.xplico.org) |

---

**Previous:** [← 06 — DNS Poisoning](06-dns-poisoning.md) · **Next:** [08 — Countermeasures & Detection →](08-countermeasures-and-detection.md)
