# 05 — Wi-Fi Discovery & Footprinting

> Objective 4 of the module (Step 1 of 5): *Demonstrate Wireless Hacking Methodology — Wi-Fi Discovery*

## The Wireless Hacking Methodology

The wireless hacking methodology helps an attacker reach the goal of hacking a target wireless network. An attacker usually follows this methodology to be sure of finding every single entry point into the target network. The objective is to compromise a Wi-Fi network to gain unauthorized access to network resources. The five steps:

1. **Wi-Fi discovery** ← *this file*
2. **Wireless traffic analysis** → `06-wireless-traffic-analysis.md`
3. **Launch of wireless attacks** → `07-wireless-attacks-dos-mitm-spoofing.md`, `08-rogue-ap-evil-twin-krack-advanced-attacks.md`
4. **Wi-Fi encryption cracking** → `09-wifi-encryption-cracking.md`
5. **Wi-Fi network compromising** (the outcome of steps 1–4 combined)

## Table of Contents
- [Wireless Network Footprinting](#wireless-network-footprinting)
- [Wi-Fi Chalking Techniques](#wi-fi-chalking-techniques)
- [Wi-Fi Discovery Tools (Desktop)](#wi-fi-discovery-tools-desktop)
- [Mobile-Based Wi-Fi Discovery Tools](#mobile-based-wi-fi-discovery-tools)
- [Finding WPS-Enabled APs](#finding-wps-enabled-aps)

---

## Wireless Network Footprinting

An attack on a wireless network begins with its **discovery and footprinting**. Footprinting involves locating and analyzing (understanding) the network. To footprint a wireless network, an attacker needs to identify the **BSS** provided by the AP — possibly identifying the BSS or Independent BSS (IBSS) with the help of the network's SSID. The attacker needs to determine the SSID of the target network, which can then be used to establish an association with the AP in order to compromise its security.

There are two footprinting methods used to detect the SSID of a wireless network:

### Passive Footprinting Method
The attacker detects the existence of an AP by **sniffing packets from the airwaves** — this discloses wireless devices, APs, and the SSID. Critically, **the attacker neither attempts to connect to any APs or clients, nor injects any data packet into the wireless traffic.** This makes passive footprinting essentially undetectable — there's no way for the target network to distinguish "someone listening" from "no one listening."

### Active Footprinting Method
The attacker's wireless device **sends a probe request with the SSID** to an AP and waits for a response. If the device doesn't have the SSID in advance, it sends a probe request with an **empty SSID** instead — most APs respond to an empty-SSID probe with their own SSID in the probe response packet, which is why empty SSIDs are useful for learning the SSIDs of nearby APs. In this method, the attacker learns the correct BSS to associate with — but it's detectable, since a properly configured AP can be set to ignore probe requests with an empty SSID.

An attacker can scan for Wi-Fi networks with tools such as **NetSurveyor** and **Wi-Fi Scanner**. The SSID appears in beacons, probe requests/responses, and association/re-association requests. If passive scanning doesn't reveal the SSID, active scanning will. Wireless network scanning works by sniffing while tuning into the various radio channels used by nearby devices.

## Wi-Fi Chalking Techniques

The first task for an attacker searching for Wi-Fi targets is to check potential networks in range to find the best one to attack. Attackers use various techniques, collectively called "War-" techniques:

| Technique | Description |
|---|---|
| **WarWalking** | Attackers walk around with a Wi-Fi-enabled laptop installed with a wireless discovery tool to map out open wireless networks. |
| **WarChalking** | Symbols are drawn in public places to advertise open Wi-Fi networks (see the symbol table in `01-wireless-concepts.md`). |
| **WarFlying** | Attackers use **drones** to detect open wireless networks — extending discovery range well beyond what's walkable or drivable. |
| **WarDriving** | Attackers drive around with a Wi-Fi-enabled laptop installed with a discovery tool to map out open wireless networks over a much larger area than walking allows, often combined with a GPS receiver to geo-tag every AP found. |

## Wi-Fi Discovery Tools (Desktop)

### inSSIDer
**Source:** https://www.metageek.com

A Wi-Fi optimization and troubleshooting tool that scans for wireless networks with the user's own Wi-Fi adapter, letting them visualize signal strengths and channels in use. Lists useful information about every discovered network. Attackers use inSSIDer to discover Wi-Fi APs and devices in their vicinity.

**Features:**
- Inspects the WLAN and surrounding networks to troubleshoot competing APs.
- Tracks the strength of a received signal in dBm over time and filters APs.
- Highlights APs for areas with high Wi-Fi concentration.
- Exports Wi-Fi and GPS data to a KML file to view in Google Earth.
- Shows overlapping Wi-Fi network channels.

*(UI layout: a **Networks Table**, a **Details Pane**, and a **Networks Graph** — the classic three-pane discovery-tool layout you'll see echoed in most competitors below.)*

### Sparrow-wifi
**Source:** https://github.com (Sparrow-wifi project)

A GUI-based, comprehensive 2.4 GHz and 5 GHz Wi-Fi spectral awareness tool. It integrates software-defined radio (RTL-SDR) advanced Bluetooth tools (Ubertooth), traditional GPS (via gpsd), and other hardware to discover Wi-Fi access points and devices, conduct spectrum hunting, and perform source hunting. It imports/exports capabilities for CSV and JSON, and can produce Google Maps for discovered devices. Its UI (`Sparrow-WiFi Analyzer`) shows a live table of MAC address / vendor / SSID / security / privacy / channel / frequency / signal strength / bandwidth / utilization / stations / last-seen / first-seen / GPS, plus a live dBm-vs-channel graph for both the 2.4 GHz and 5 GHz bands.

### Other Desktop Wi-Fi Discovery Tools
| Tool | Source |
|---|---|
| Wi-Fi Scanner | https://lizardsystems.com |
| Acrylic Wi-Fi Heatmaps | https://www.acrylicwifi.com |
| WirelessMon | https://www.passmark.com |
| Ekahau Wi-Fi Heatmaps | https://www.ekahau.com |
| NetSpot | https://www.netspotapp.com |
| AirMagnet® Survey PRO | https://www.netally.com |

## Mobile-Based Wi-Fi Discovery Tools

### WiFi Analyzer
**Source:** https://play.google.com

A Wi-Fi network optimization tool used to examine surrounding Wi-Fi networks, measure their signal strengths, and identify crowded channels. Attackers use WiFi Analyzer to detect nearby APs, graph channel signal strengths, and estimate distances to APs.

### Other Mobile Discovery Tools
| Tool | Source |
|---|---|
| Opensignal | https://opensignal.com |
| Network Signal Info Pro | https://www.keibis-software.com |
| Net Signal Pro & 5G Meter | https://www.google.com/play |
| NetSpot WiFi Analyzer | https://www.netspotapp.com |
| WiFiman | https://play.google.com |

## Finding WPS-Enabled APs

Attackers use the **Wash** command-line utility (bundled with the Reaver package) to identify **WPS-enabled** APs in the target wireless network, and to check whether the AP is in a **locked** or **unlocked** state. Most WPS-enabled routers lock automatically after 5 consecutive incorrect PIN attempts and can only be unlocked manually via the router's admin interface. The Wash command supports the **5 GHz channel** and requires Reaver to be installed.

Basic usage:

```bash
sudo wash -i wlan0
```

**Wash command arguments** (as documented in the module):

| Flag | Meaning |
|---|---|
| `-i, --interface=<iface>` | Specifies the interface to capture packets |
| `-a, --all` | Displays all access points, including those with WPS disabled |
| `-f, --file [FILE1 FILE2 FILE3 ...]` | Reads packets from previously captured files |
| `-c, --channel=<num>` | Specifies the channel to listen on (default: auto) |
| `-o, --out-file=<file>` | Writes data to a file |
| `-n, --probes=<num>` | Specifies the maximum number of probes to send to each AP in scan mode |
| `-D, --daemonize` | Runs Wash as a daemon |
| `-5, --5ghz` | Use 5 GHz 802.11 channels |
| `-s, --scan` | Run in scan mode |
| `-u, --survey` | Run in survey mode (default) |

**Sample output fields:** `BSSID | Ch | dBm | WPS | Lck | Vendor | ESSID` — the `Lck` column tells you at a glance whether WPS PIN entry is currently locked out on that AP.

If WPS-enabled devices cannot be detected using Wash, fall back to **Airodump-ng**:

```bash
# If your adapter shows as wlan0mon in monitor mode:
airodump-ng wlan0mon
```

This displays all available BSSIDs (MAC addresses of APs) in range, from which you select your target for the next phase — see `06-wireless-traffic-analysis.md`.

---
**Previous:** [`04-wireless-threats.md`](04-wireless-threats.md)
**Next:** [`06-wireless-traffic-analysis.md`](06-wireless-traffic-analysis.md) — sniffing and analyzing 802.11 traffic once a target is chosen.
