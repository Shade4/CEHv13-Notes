# 01 — Wireless Concepts

> Objective 1 of the module: *Summarize Wireless Concepts*

## Table of Contents
- [Why Wireless Is Different](#why-wireless-is-different)
- [Core Wireless Terminology](#core-wireless-terminology)
- [Types of Wireless Networks](#types-of-wireless-networks)
- [Service Set Identifier (SSID)](#service-set-identifier-ssid)
- [Wi-Fi Authentication Process](#wi-fi-authentication-process)
- [Wi-Fi Chalking](#wi-fi-chalking)
- [Advantages & Disadvantages of Wireless Networks](#advantages--disadvantages-of-wireless-networks)

---

## Why Wireless Is Different

Wired networks confine an attacker to a physical connection — someone has to plug a cable in somewhere you can see. Wireless networks broadcast into open air, so **anyone within radio range can attempt to intercept, inject, or interact with the network without ever touching a cable or entering a building.** This single fact is the root of every threat discussed in this module: the network boundary is no longer the wall of the building, it's the reach of the radio signal.

Wireless technology is heading toward a new era of technological evolution through wireless networking. Removing physical connections or cables allows people to work in more flexible ways, and this convenience is exactly why enterprises have adopted Wi-Fi so aggressively — and why it's such a rich target.

## Core Wireless Terminology

| Term | Definition |
|---|---|
| **GSM** (Global System for Mobile Communication) | An internationally accepted standard for cellular communication, used in mobile digital telephony. |
| **Bandwidth** | Describes the amount of information that can be broadcast over a connection. Usually measured in bits/second (bps). |
| **Access Point (AP)** | A hardware device or software that acts as a communication hub for devices to connect to a wired LAN, using Wi-Fi, Bluetooth, or related standards. It bridges wireless clients and the wired network. |
| **BSSID** (Basic Service Set Identifier) | The MAC address of an access point (AP) or base station that has set up a Basic Service Set (BSS). Wi-Fi devices identify a BSS via its BSSID. |
| **ISM band** (Industrial, Scientific, and Medical) | A band reserved internationally for industrial, scientific, and medical purposes other than telecommunications. Most Wi-Fi (2.4 GHz) operates here license-free. |
| **Hotspot** | Places where wireless network access is available for public use — cafes, airports, hotels — that allow Wi-Fi-enabled devices to connect to the Internet. |
| **Association** | The process of connecting a wireless device to an access point. |
| **Orthogonal Frequency-Division Multiplexing (OFDM)** | A method of digital modulation where a signal is split into several narrowband channels at different frequencies to reduce interference and crosstalk. |
| **Multiple Input, Multiple Output – OFDM (MIMO-OFDM)** | Increases wireless bandwidth and range by using several antennas instead of one, effectively enhancing OFDM's spectral efficiency. |
| **Direct-Sequence Spread Spectrum (DSSS)** | A spread-spectrum technique in which the original data signal is multiplied by a pseudo-random noise-spreading code. This increases the signal's bandwidth and protects against jamming. |
| **Frequency-Hopping Spread Spectrum (FHSS)** | A transmission technology where the sender's data signal is modulated with a narrowband carrier that "hops" in a predictable sequence from frequency to frequency, as a function of time, over a wide band. Protects against unauthorized interception because a receiver must know the hopping pattern to decode it. |

## Types of Wireless Networks

### 1. Extension to a Wired Network
Access points are placed strategically to extend an existing wired network with wireless coverage. Devices with a wireless network interface card (NIC) can connect to the network through the AP. There are two sub-types:
- **Software APs (SAPs)** — can be connected to a wired network interface card (NIC) and run on a computer.
- **Hardware APs (HAPs)** — support most wireless features and provide a richer feature set than SAPs.

### 2. Multiple Access Points
Multiple APs cover a single area with overlapping wireless coverage. This allows continuous connectivity as a wireless client roams the area — one AP's signal handing off to the next. Enterprise deployments generally use a controller to manage many APs centrally.

### 3. LAN-to-LAN Wireless Network
APs provide connectivity to local computers, and local computers on different networks can also be interconnected. Interconnecting LANs over wireless connections is a more complex task typically done with directional antennas or wireless bridges (e.g., linking two office buildings).

### 4. 3G/4G/5G Hotspot
A 3G/4G/5G hotspot is a type of wireless network that provides Wi-Fi access to Wi-Fi-enabled devices (MP3 players, notebooks, tablets, cameras, PDAs, netbooks, and more) by sharing a cellular data connection over Wi-Fi.

## Service Set Identifier (SSID)

An **SSID** is a case-sensitive, human-readable, unique identifier of a WLAN, up to **32 alphanumeric characters** in length. It's a token used to identify and locate 802.11 (Wi-Fi) networks. By default, it's part of the frame header of every packet sent over a WLAN, and it acts as a single shared identifier between APs and clients so a device can locate the correct AP to attempt a subsequent `AUTH` (authentication) and `ASSOC` (association).

**Security implications of the SSID:**
- SSID APs respond to probe requests with probe responses that include the SSID itself — even if it's "hidden," it isn't secret.
- Because the SSID is the unique identifier of a WLAN, every AP and device in it must use the same SSID.
- Non-secure access mode allows clients to connect using the configured SSID, a blank SSID, or an SSID configured as "any."
- **SSID provides no real security.** It's trivially obtained as plaintext from captured packets — an attacker doesn't need to break any cryptography, just sniff a beacon or probe frame.
- For many commercial products, the default SSID is simply the vendor's name (`NETGEAR`, `Linksys`, `TP-Link`, etc.), which itself leaks information about the hardware and its likely default configuration/vulnerabilities.
- SSID can be kept confidential only in closed networks with *no activity at all* — which is inconvenient to legitimate users and defeated the moment any client tries to connect (see `05-wifi-discovery-and-footprinting.md` → *Detection of Hidden SSIDs*).

## Wi-Fi Authentication Process

There are two authentication modes in Wi-Fi networks.

### Pre-Shared Key (PSK) Mode
Also known as **WPA-PSK** or **WPA2-PSK**, this mode secures a wireless network using a single shared password for authentication. It's popular in homes and small offices for its simplicity — the same passphrase is manually entered into both the router and every connecting device. The convenience trades off against security: the strength of the whole network rests entirely on the complexity and secrecy of that one shared passphrase.

**PSK authentication flow** *(Figure 16.5)*:
1. Client sends an authentication request to the AP.
2. AP sends a challenge text back to the client.
3. Client encrypts the challenge text (using the shared key) and sends it back to the AP.
4. AP decrypts the challenge text; if it matches, the client is authenticated.
5. Client connects to the network (and onward to the switch/cable modem/Internet).

### Centralized Authentication Mode
A **centralized authentication server**, known as **RADIUS** (Remote Authentication Dial-In User Service), sends authentication keys to both the AP and the client. Each user gets **unique credentials**, providing much stronger security because access is verified independently per user rather than via one shared secret.

**RADIUS (802.1X/EAP) authentication flow** *(Figure 16.6)*:
1. Client sends a connection request to the Access Point.
2. AP sends an EAP-Request to determine the client's identity.
3. Client sends an EAP-Response containing its identity.
4. AP forwards the identity to the RADIUS server over the uncontrolled port.
5. RADIUS server sends a request to the wireless client (via the AP) specifying the authentication mechanism to use.
6. Wireless client responds to the RADIUS server with its credentials.
7. RADIUS server sends an encrypted authentication key to the AP if the credentials are acceptable.
8. AP sends a multicast/global authentication key, encrypted with a per-station unicast session key, to the client.

This is exactly the flow abused in **Authentication Attacks** (see `04-wireless-threats.md`) and is why enterprise deployments (WPA2/WPA3-**Enterprise**) are considered significantly harder to attack at scale than PSK/Personal networks — compromising one user's credentials doesn't hand over the master network key.

## Wi-Fi Chalking

**Wi-Fi Chalking** (or *WarChalking*) is the practice of drawing symbols in public places to advertise open or exploitable Wi-Fi networks, historically done with chalk on sidewalks/walls near the AP. The standardized symbols:

| Symbol Meaning | Description |
|---|---|
| **Free Wi-Fi** | Two back-to-back half-circles ("open node") — network is open, no authentication required |
| **Wi-Fi with MAC Filtering** | Half-circles with a padlock icon — open, but MAC filtering is enabled |
| **Restricted Wi-Fi** | A full circle ("closed node") — access requires credentials |
| **Pay for Wi-Fi** | Half-circles with a `$` symbol — commercial hotspot |
| **Wi-Fi with WEP** | Half-circles with a `W` — WEP-encrypted network |
| **Wi-Fi with Multiple Access Controls** | Half-circles with an `X` — multiple restrictions in place |
| **Wi-Fi with Closed SSID** | Half-circles with a `−` (minus) — SSID is not broadcast |
| **Wi-Fi Honeypot** | A circle marked `HUNY` — flags a suspected honeypot AP |

Related "War-" techniques covered in depth in `05-wifi-discovery-and-footprinting.md`:
- **WarWalking** — walking around with a Wi-Fi-enabled laptop to map open wireless networks.
- **WarDriving** — the same activity done from a moving vehicle, often combined with a GPS unit to geo-tag every discovered AP.
- **WarFlying** — using a drone instead of a vehicle, for wide-area surveys.

## Advantages & Disadvantages of Wireless Networks

**Advantages**
- Installation is fast and easy, without the need for pulling cable through walls and ceilings.
- Easily provides connectivity in areas where it's difficult to lay cable.
- The network can be accessed from anywhere within range of the AP.
- Public spaces (libraries, airports, coffee shops) can offer visitors constant Internet connectivity through WLANs.

**Disadvantages**
- Security may not meet expectations by default — many deployments ship insecure or with defaults unchanged.
- Bandwidth suffers as the number of devices on the network increases (shared medium).
- Wi-Fi upgrades may require new wireless cards and/or APs across an entire fleet of devices.
- Electronic equipment (microwaves, cordless phones, Bluetooth devices, baby monitors) can interfere with Wi-Fi, especially in the 2.4 GHz band.

---
**Next:** [`02-wireless-standards-topologies-antennas.md`](02-wireless-standards-topologies-antennas.md) — the 802.11 standards family, network topologies, and antenna theory.
