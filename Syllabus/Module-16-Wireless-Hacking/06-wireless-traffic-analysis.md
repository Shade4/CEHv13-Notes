# 06 — Wireless Traffic Analysis

> Objective 4 of the module (Step 2 of 5): *Demonstrate Wireless Hacking Methodology — Wireless Traffic Analysis*

## Table of Contents
- [Why Analyze Traffic Before Attacking](#why-analyze-traffic-before-attacking)
- [Monitor Mode — the Prerequisite](#monitor-mode--the-prerequisite)
- [802.11 Frame Types (Background)](#80211-frame-types-background)
- [Wi-Fi Packet Sniffing Tools](#wi-fi-packet-sniffing-tools)
- [Choosing the Optimal Wi-Fi Card](#choosing-the-optimal-wi-fi-card)
- [Performing Spectrum Analysis](#performing-spectrum-analysis)

---

## Why Analyze Traffic Before Attacking

The next step in the wireless hacking methodology, after discovery, is to **analyze the traffic** of the discovered wireless network. An attacker performs wireless traffic analysis *before* launching actual attacks — this analysis determines the network's vulnerabilities and susceptible victims, as well as the appropriate strategy for a successful attack.

Wi-Fi protocols are unique to Layer 2, and traffic over the air isn't serialized the way wired Ethernet is, which makes it comparatively easy to sniff and analyze wireless packets (there's no switch to bypass — everything in range is broadcast into the same shared medium). Attackers analyze a wireless network to determine:
- The broadcast SSID
- The presence of multiple access points
- The possibility of recovering hidden SSIDs
- The authentication method used (Open, PSK, EAP/RADIUS)
- The WLAN encryption algorithm(s) in play (WEP/WPA/WPA2/WPA3)

**Sniffing** is a type of eavesdropping in which attackers intercept all ongoing wireless communication. It's performed by simply tuning a receiver to the target transmission frequency and identifying the target communication protocol used. Attackers then analyze the captured traffic to plan further attacks on the target network.

## Monitor Mode — the Prerequisite

To sniff wireless traffic, an attacker needs to enable **monitor mode** on their Wi-Fi card. Monitor mode lets the adapter capture all 802.11 frames on a given channel — not just those addressed to it — without first associating with any AP. This is distinct from *promiscuous mode* on a wired NIC.

**Not every Wi-Fi card supports monitor mode, especially on Windows.** Check compatibility at:
```
https://secwiki.org/w/Npcap/WiFi_adapters
```

On Linux (Parrot OS/Kali), monitor mode is enabled with the Aircrack-ng suite's `airmon-ng` tool — see `07-wireless-attacks-dos-mitm-spoofing.md` and `09-wifi-encryption-cracking.md` for the exact command sequence used throughout this repository.

## 802.11 Frame Types (Background)

*(Supplementary detail — standard 802.11 knowledge that underpins everything sniffed in this section.)* Every frame captured by tools like Wireshark falls into one of three types, distinguishable via the frame-control field:

| Frame Type | Purpose | Examples |
|---|---|---|
| **Management** | Establish and maintain communication | Beacon, Probe Request/Response, Authentication, Association Request/Response, Deauthentication, Disassociation |
| **Control** | Assist in delivering data frames | RTS (Request to Send), CTS (Clear to Send), ACK (Acknowledgment) |
| **Data** | Carry the actual payload | Data, QoS Data, Null Data |

Two frame types matter disproportionately for this entire module:
- **Beacon frames** — broadcast continuously by an AP (roughly every 100 ms) to advertise its SSID (unless hidden), supported rates, channel, and security capabilities. This is what tools like `airodump-ng` passively collect to build the list of nearby networks.
- **Deauthentication/Disassociation frames** — management frames that, critically, are **unauthenticated and unencrypted** in WEP/WPA/WPA2 (fixed only by WPA3's mandatory Protected Management Frames, PMF). Anyone in range can forge one with the correct source/destination MAC addresses. This single design flaw is the basis for nearly every active attack in `07-wireless-attacks-dos-mitm-spoofing.md` and `09-wifi-encryption-cracking.md` — forcing a deauthentication is how attackers force a fresh 4-way handshake to capture, or simply deny service outright.

## Wi-Fi Packet Sniffing Tools

Attackers use Wi-Fi packet analyzer tools such as **AirMagnet™ G3 Pro**, **Wireshark**, **Riverbed Packet Analyzer**, **OmniPeek**, and **CommView for Wi-Fi** to capture and analyze the traffic of a target wireless network.

### Wireshark
**Source:** https://www.wireshark.org

A network protocol sniffer and analyzer. Wireshark can read live data from Ethernet networks, Token Ring networks, FDDI networks, Point-to-Point Protocol (PPP), Serial Line Internet Protocol (SLIP) networks, 802.11 wireless LANs, ATM connections (if the OS allows), and any device supported on Linux by recent versions of libpcap. **Npcap** is integrated with Wireshark for complete WLAN traffic analysis, visualization, drill-down, and reporting.

Attackers capture wireless traffic by enabling monitor mode in Wireshark. Wireshark lets attackers capture a huge amount of management frames, control frames, and data frames — and further analyze **Radiotap header fields** to gather critical information such as the protocols used, encryption techniques used, frame lengths, and MAC addresses.

```bash
# Typical Wireshark capture workflow on the monitor-mode interface
sudo wireshark -i wlx00e02d886189 -k
# Or headless capture with tshark:
sudo tshark -i wlx00e02d886189 -w capture.pcapng
```

### CommView for Wi-Fi
**Source:** https://www.tamos.com

A wireless network monitor and analyzer for 802.11 a/b/g/n networks. It captures packets and displays important information: the list of APs and stations, per-node and per-channel statistics, signal strength, a list of packets and network connections, and protocol distribution charts. A user can **decrypt packets with user-defined WPA-PSK keys** and decode them down to the lowest layer. Reveals every detail of a captured packet using a tree-like structure to display protocol layers and packet headers.

### Additional Wi-Fi Packet Sniffers
| Tool | Source |
|---|---|
| OmniPeek® Network Protocol Analyzer | https://www.liveaction.com |
| Kismet | https://www.kismetwireless.net |
| SolarWinds Network Performance Monitor | https://www.solarwinds.com |
| Acrylic Wi-Fi Analyzer | https://www.acrylicwifi.com |
| airgeddon | https://github.com |

## Choosing the Optimal Wi-Fi Card

Selecting the right Wi-Fi adapter is essential before any hands-on wireless hacking, because Windows systems generally cannot fully capture and inject packets the way Linux with the correct driver can. The factors to weigh:

1. **Determine the Wi-Fi hacking requirements** — passive listening only, or listening + injection? Injection support is the stricter requirement.
2. **Learn the capabilities of a wireless card** — determined by the brand and, more specifically, the **chipset**.
3. **Determine the chipset of the Wi-Fi card**:
   - Sometimes the chip is directly visible on the card/board, chipset number included.
   - The **FCC ID Search** can look up detailed manufacturer/model/chipset info if an FCC ID is printed on the board.
   - Manufacturers occasionally swap chipsets while keeping the same model number (a "card revision"/"card version") — always check the revision, not just the model.
   - `https://wireless.wiki.kernel.org/en/users/Drivers` can help confirm OS compatibility for a given chipset.
4. **Verify the chipset's capabilities** — confirm compatibility with your OS and that it meets your requirements before buying.
5. **Determine the drivers and patches required** for that chipset on your OS.

## Performing Spectrum Analysis

Beyond packet-level sniffing, an attacker can use **spectrum analyzers** to discover the presence of wireless networks at the RF-signal level. Spectrum analysis enables an attacker to actively monitor spectrum usage in a particular area and detect the target network's spectrum signal. It also helps measure the spectrum power of known and unknown signals. Spectrum analyzers employ statistical analysis to plot spectrum usage, quantify **"air quality,"** and isolate transmission sources. RF technicians use spectrum analyzers to install/maintain wireless networks and identify sources of interference; for an attacker, Wi-Fi spectrum analysis also helps detect **DoS attacks, authentication/encryption attacks, and network penetration attacks** already underway (or in progress against them).

### RF Explorer
**Source:** https://rfexplorer.com

An RF spectrum analysis tool that can operate as a **standalone handheld** RF spectrum analyzer or interface with a PC running more sophisticated analysis software. It's the instrument of choice for initial detection/identification of RF interference sources and subsequent health monitoring of a wireless system. RF Explorer gives a view of the local RF environment to help detect the presence of RF transmissions that are interference sources.

### Other RF Monitoring / Spectrum Analysis Tools
| Tool | Source |
|---|---|
| Chanalyzer | https://www.metageek.com |
| AirCheck G3 Pro | https://www.netally.com |
| Spectraware S1000 | https://thinkrf.com |
| RSA306B USB Spectrum Analyzer | https://www.tek.com |
| RF Explorer 6G | https://j3.rf-explorer.com |
| RFXpert | https://www.dektec.com |
| Monics® 200 / Monics® satID® | https://www.kratosdefense.com |
| Signal Hound | https://signalhound.com |
| FieldSENSE | https://www.fieldsense.com |

---
**Previous:** [`05-wifi-discovery-and-footprinting.md`](05-wifi-discovery-and-footprinting.md)
**Next:** [`07-wireless-attacks-dos-mitm-spoofing.md`](07-wireless-attacks-dos-mitm-spoofing.md) — the module's first hands-on active-attack procedures.
