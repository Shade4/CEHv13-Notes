# 02 — Wireless Standards, Topologies & Antennas

> Supporting detail for Objective 1: *Summarize Wireless Concepts*

## Table of Contents
- [The IEEE 802.11 Family](#the-ieee-80211-family)
- [Full Standards Reference Table](#full-standards-reference-table)
- [Standard-by-Standard Notes](#standard-by-standard-notes)
- [Related 802 Standards (Bluetooth, ZigBee, WiMAX)](#related-802-standards-bluetooth-zigbee-wimax)
- [Types of Wireless Antennas](#types-of-wireless-antennas)
- [Choosing the Optimal Wi-Fi Card for Hacking](#choosing-the-optimal-wi-fi-card-for-hacking)

---

## The IEEE 802.11 Family

IEEE Standard 802.11 has evolved from a standard for a basic wireless extension to a wired LAN into a mature protocol supporting enterprise authentication, strong encryption, and quality of service (QoS). When introduced in 1997, the WLAN standard specified operation at 1 and 2 Mbps in the infrared range as well as the license-exempt **2.4-GHz ISM band**. In the early days, an 802.11 network had a few PCs with wireless capability connected to an Ethernet (IEEE 802.3) LAN through a single AP. Now, 802.11 networks operate at substantially higher speeds and in additional bands, and new issues have arisen — security, roaming among multiple APs, and quality of service. Amendments to the standard are indicated by letters of the alphabet derived from the 802.11 task groups that created them.

## Full Standards Reference Table

*(Table 16.1 from the module, reproduced exactly)*

| Amendment | Frequency (GHz) | Modulation | Speed (Mbps) | Range (Meters) |
|---|---|---|---|---|
| 802.11 (Wi-Fi) | 2.4 | DSSS, FHSS | 1, 2 | 20 – 100 |
| 802.11a | 5 / 3.7 | OFDM | 6, 9, 12, 18, 24, 36, 48, 54 | 35–100 / 5000 |
| 802.11ax | 2.4 to 5 | 1024-QAM | 2400 | 240 |
| 802.11b | 2.4 | DSSS | 1, 2, 5.5, 11 | 35 – 140 |
| 802.11be | 2.4, 5, 6 | QAM | 3000 | 120 |
| 802.11g | 2.4 | OFDM | 6, 9, 12, 18, 24, 36, 48, 54 | 38 – 140 |
| 802.11n | 2.4, 5 | MIMO-OFDM | 54 – 600 | 70 – 250 |
| 802.15.1 (Bluetooth) | 2.4 | GFSK, π/4-DPSK, 8DPSK | 25 – 50 | 10 – 240 |
| 802.15.4 (ZigBee) | 0.868, 0.915, 2.4 | O-QPSK, GFSK, BPSK | 0.02, 0.04, 0.25 | 1 – 100 |
| 802.16 (WiMAX) | 2 – 11 | SOFDMA | 34 – 1000 | 1609.34 – 9656.06 (1–6 miles) |

## Standard-by-Standard Notes

| Standard | Description |
|---|---|
| **802.11** | Applies to WLANs and uses FHSS or DSSS as the frequency-hopping spectrum. Allows an electronic device to establish a wireless connection in any network. |
| **802.11a** | The first amendment to the original 802.11 standard. Operates in the 5 GHz band, up to 54 Mbps via OFDM. High max speed but more sensitive to walls/obstacles than 2.4 GHz. |
| **802.11ax (Wi-Fi 6)** | Latest generation, enhances 802.11ac (Wi-Fi 5). Up to 9.6 Gbps, uses OFDMA to efficiently manage multiple connections, improves performance in crowded areas via **BSS Coloring** and **Target Wake Time (TWT)**. Ideal for dense environments (stadiums, airports, smart homes). |
| **802.11b** | Extended 802.11 in 1999. Operates in 2.4 GHz ISM band, up to 11 Mbps via DSSS. |
| **802.11be (Wi-Fi 7)** | Emerging standard, significantly improves on Wi-Fi 6/6E. Up to 30 Gbps, uses **Multi-Link Operation (MLO)** to aggregate multiple channels across different bands, reduces latency for real-time applications. Designed for ultra-high-speed Internet, VR, AR, and advanced IoT. |
| **802.11d** | Enhancement to 802.11a/802.11b enabling global portability by allowing variation in frequencies, power levels, and bandwidth per regulatory domain. Specifications can be set at the MAC layer. |
| **802.11e** | Provides guidance for prioritization of data, voice, and video transmissions, enabling QoS at Layer 2 (MAC layer) — critical for VoIP/video over Wi-Fi. |
| **802.11g** | Extension of 802.11b/802.11, up to 54 Mbps via OFDM, same 2.4 GHz band, backward compatible with 802.11b. |
| **802.11i** | Improves WLAN security by defining new encryption protocols: **TKIP** and **AES**. This is the standard that formally introduced **WPA2** and defines **WPA2-Enterprise/WPA2-Personal**. |
| **802.11n** | Revision enhancing 802.11g with **MIMO** antennas. Works in both 2.4 GHz and 5 GHz bands. |
| **802.11ah (Wi-Fi HaLow)** | Uses 900 MHz band for extended-range Wi-Fi; supports IoT communication with higher data rates and wider coverage than earlier standards. |
| **802.11ac** | High-throughput at 5 GHz — faster and more reliable than 802.11n; "Gigabit networking" with near-instantaneous data transfer. |
| **802.11ad** | New physical layer for 802.11 networks operating on the **60 GHz** spectrum — much higher propagation speed than 2.4/5 GHz standards. |
| **802.12** | Media utilization dominated by the demand priority protocol; 100 Mbps Ethernet speed; compatible with 802.3 and 802.5. |

## Related 802 Standards (Bluetooth, ZigBee, WiMAX)

- **802.15**: Defines standards for a wireless personal area network (**WPAN**) — specifications for wireless connectivity with fixed or portable devices.
- **802.15.1 (Bluetooth)**: Used mainly for exchanging data over short distances on fixed or mobile devices. Operates in the 2.4 GHz band.
- **802.15.4 (ZigBee)**: Low data rate and complexity. Transmits long-distance data through a mesh network. Handles applications with a low data rate (250 Kbps) but increases battery life — hence its popularity in IoT sensors.
- **802.15.5**: Deploys on a full-mesh or half-mesh topology. Includes network initialization, addressing, and unicasting.
- **802.16 (WiMAX)**: A wireless communications standard providing multiple physical-layer (PHY) and MAC options. A specification for fixed broadband wireless metropolitan area networks (MANs) using a point-to-multipoint architecture.

## Types of Wireless Antennas

Antennas are an integral part of Wi-Fi networks. Beyond sending/receiving radio signals, they convert electrical impulses into radio signals and vice versa. **Antenna choice materially affects attack range** — pairing a directional or parabolic antenna with your adapter is one of the simplest ways to extend the practical distance of Wi-Fi discovery and injection attacks.

### Directional Antenna
Broadcasts and receives radio waves from a single direction. This focuses the design to work effectively in only a few directions, improving transmission/reception and reducing interference. Used, e.g., for site-to-site backhaul links.

### Omnidirectional Antenna
Radiates electromagnetic (EM) energy in **all directions** — a 360° horizontal radiation pattern. Radiates strong waves uniformly in two dimensions, though not as strong in the third. Efficient for stations using time-division multiple access. Radio-station antennas are a classic example; effective for signal transmission when the receiver isn't stationary.

### Parabolic Grid Antenna
Uses the same principle as a satellite dish but without a solid dish — a semi-dish in the form of a grid of aluminum wires. Achieves **very-long-distance Wi-Fi transmissions** through highly focused radio beams, useful for transmitting weak radio signals over distances **on the order of 10 miles**. This lets an attacker obtain better signal quality — more data to eavesdrop on, more bandwidth to abuse, and higher power output, which matters for Layer-1 DoS and MITM attacks. Lightweight, space-saving design; can receive both horizontally and vertically polarized Wi-Fi signals.

### Yagi Antenna
Also called **Yagi–Uda**, a unidirectional antenna commonly used at frequency bands from 10 MHz to VHF/UHF. High gain, low signal-to-noise ratio for radio signals. Not only unidirectional in radiation/response pattern but also *concentrates* that radiation and response. Consists of a reflector, a dipole, and multiple directors, producing an end-fire radiation pattern.

### Dipole Antenna
A straight electrical conductor measuring **half a wavelength** end to end, connected at the center to the RF feed line. Also called a *doublet* — bilaterally symmetrical and therefore inherently balanced. Feeds on a balanced parallel-wire RF transmission line. This is the classic "rubber duck" antenna shape found on most consumer routers and USB Wi-Fi adapters.

### Reflector Antennas
Used to concentrate EM energy radiated or received at a focal point; the reflectors are generally parabolic. If the parabolic surface is within tolerance, it can serve as a primary mirror for all frequencies, preventing interference while communicating with other emitters (e.g., satellites). A larger reflector (in wavelength multiples) yields higher gain. High manufacturing cost.

## Choosing the Optimal Wi-Fi Card for Hacking

Selecting the right Wi-Fi card is one of the most important preparatory steps for wireless hacking — a card that lacks monitor mode or injection support will block nearly every technique in this repository. The key factors to consider:

1. **Determine the Wi-Fi hacking requirements** — will you need to listen to network traffic, or both listen and inject packets? Injection is a stricter requirement than passive sniffing. Windows systems can listen to network traffic but do not fully support capturing/injecting packets; Linux (e.g., Parrot OS/Kali) with the right driver supports both.
2. **Learn the capabilities of a wireless card** — the brand of the card and the chipset it's built around determine what it can do. An attacker can determine the capabilities of a Wi-Fi card using the chipset name.
3. **Determine the chipset of the Wi-Fi card** — search the Internet, check the Windows driver filenames (which often reveal the chipset name), or check the manufacturer's page.
4. **Verify the capabilities of a chosen card and its drivers and patches** — determine whether the chipset is compatible with the OS, and whether required drivers/patches are available for the chosen OS.

**Commonly cited chipsets for injection-capable adapters** (from the module's tool discussions and widely documented in the aircrack-ng compatibility list): Atheros (AR9271), Ralink (RT3070/RT5572/MT7601U — the chipset used in the module's own screenshots), and Realtek (RTL8812AU).

---
**Previous:** [`01-wireless-concepts.md`](01-wireless-concepts.md)
**Next:** [`03-wireless-encryption-wep-wpa-wpa2-wpa3.md`](03-wireless-encryption-wep-wpa-wpa2-wpa3.md) — WEP, WPA, WPA2, and WPA3 internals.
