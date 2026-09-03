# 07 — Launching Wireless Attacks: DoS, MITM & Spoofing

> Objective 4 of the module (Step 3 of 5): *Demonstrate Wireless Hacking Methodology — Launch of Wireless Attacks (Part 1)*

## Table of Contents
- [The Aircrack-ng Suite (Full Reference)](#the-aircrack-ng-suite-full-reference)
- [Detection of Hidden SSIDs](#detection-of-hidden-ssids)
- [Denial-of-Service Attacks](#denial-of-service-attacks)
- [Man-in-the-Middle Attack](#man-in-the-middle-attack)
- [MITM Attack Using Aircrack-ng](#mitm-attack-using-aircrack-ng)
- [MAC Spoofing Attack](#mac-spoofing-attack)
- [Wireless ARP Poisoning Attack](#wireless-arp-poisoning-attack)
- [ARP Poisoning Attack Using Ettercap](#arp-poisoning-attack-using-ettercap)

---

After completing wireless network discovery, mapping, and traffic analysis, an attacker is in a position to launch an attack on the target wireless network — fragmentation attacks, MAC spoofing attacks, DoS attacks, and ARP poisoning attacks among them. This file and `08-rogue-ap-evil-twin-krack-advanced-attacks.md` cover every attack demonstrated in the module.

## The Aircrack-ng Suite (Full Reference)

**Source:** https://www.aircrack-ng.org

Aircrack-ng is a network software suite consisting of a detector, packet sniffer, WEP and WPA-PSK (WPA1 and WPA2) cracker, and analysis tool for 802.11 wireless networks. Runs under Linux and Windows (Linux is strongly preferred for injection support).

| Tool | Purpose |
|---|---|
| **airbase-ng** | Captures the WPA/WPA2 handshake and can act as an ad-hoc AP |
| **aircrack-ng** | The de facto WEP and WPA/WPA2-PSK cracking tool |
| **airdecap-ng** | Decrypts WEP/WPA/WPA2 and can be used to strip wireless headers from Wi-Fi packets |
| **airdrop-ng** | Targeted, rule-based de-authentication of users |
| **aireplay-ng** | Especially effective for gathering WEP IVs and WPA handshakes, which can then be fed into aircrack-ng for cracking |
| **airmon-ng** | Enables monitor mode on wireless interfaces from managed mode, and vice versa |
| **airodump-ng** | Captures packets of raw 802.11 frames and collects WEP IVs |
| **airolib-ng** | Stores and manages ESSID and password lists used in WPA/WPA2 cracking |
| **airgraph-ng** | Creates a client–AP relationship and common-probe graph from an airodump file |
| **airtun-ng** | Creates a virtual tunnel interface to monitor encrypted traffic and inject arbitrary traffic into a network |

This suite is used, in some combination, in nearly every attack from this point forward in the repository.

## Detection of Hidden SSIDs

Based on the principle of *security through obscurity*, many organizations hide their SSID by not broadcasting it in beacon frames — part of many orgs' security policy, on the theory that an attacker might otherwise take advantage of a visible SSID. **Hiding SSIDs does not increase real security** — it's trivially defeated the moment a client tries to connect (any association request/response necessarily contains the SSID in plaintext), and it can be brute-forced outright.

```bash
# Step 1 — put the adapter into monitor mode
airmon-ng start wlx00e02d886189
# If a process interferes ("Found 2 processes that could cause trouble"):
airmon-ng check kill

# Step 2 — discover SSIDs on the interface
airodump-ng wlx00e02d886189
# The target's SSID column will show "<length: 0>" — hidden

# Step 3 — brute-force the hidden SSID with mdk3
mdk3 wlx00e02d886189 p -b 1 -c 2 -t 1C:3B:F3:40:10:74
```

**`mdk3` flags used above:**
| Flag | Meaning |
|---|---|
| `p` | Basic probing and ESSID brute-force mode |
| `-b 1` | Beacon flood mode / EAPOL logoff test (`1`) |
| `-c 2` | Selection channel (here, channel 2) |
| `-t 1C:3B:F3:40:10:74` | Target BSSID |
| `wlx00e02d886189` | Wireless interface |

`mdk3` will cycle through probe requests until the AP responds and reveals its true SSID — after which `airodump-ng`'s ESSID column will populate for that BSSID.

## Denial-of-Service Attacks

Wireless networks are vulnerable to DoS attacks because of the relationships among the physical, data-link, and network layers — these networks operate in unlicensed bands transmitting mission-critical applications (VoIP, database access, project files, Internet access) as radio signals, and the MAC protocol, designed for simplicity, is vulnerable. Disrupting these applications via DoS causes real productivity loss or network downtime. **Wireless DoS attacks disrupt connections by broadcasting de-authenticate commands, forcing clients to disconnect from the AP.**

### Disassociation Attack
1. Client is authenticated and associated with the AP.
2. Attacker sends a **disassociate request packet**, spoofed as coming from the AP, to take a single client offline.
3. The client is still authenticated but no longer associated with the AP — it must re-associate to regain connectivity.

### De-authentication Attack
1. Client is authenticated and associated with the AP.
2. Attacker sends a **de-authenticate request packet** to take a single client offline.
3. The client is no longer authenticated or associated with the AP.

**De-authentication command:**
```bash
aireplay-ng --deauth 25 -h <TARGET_MAC> -b <AP_MAC> ath1
```
- `--deauth 25` — send 25 deauth packets
- `-h <TARGET_MAC>` — the client (victim) MAC address
- `-b <AP_MAC>` — the target AP's BSSID
- `ath1` — the wireless interface

This single command is arguably the most-reused primitive in the entire module — it appears again (with different flag counts) inside the WPA/WPA2/WPA3 handshake-capture workflows in `09-wifi-encryption-cracking.md`, inside the MITM flow below, and inside the Wi-Jacking attack in `08-rogue-ap-evil-twin-krack-advanced-attacks.md`.

## Man-in-the-Middle Attack

A MITM attack is an active Internet attack in which the attacker attempts to intercept, read, or alter information transmitted between two computers. MITM attacks apply to both 802.11 WLANs and wired communication systems.

### Eavesdropping
Eavesdropping is easy on a wireless network because no physical medium is used for communication — an attacker in the vicinity can receive radio waves without much effort or equipment, then examine the entire data frame sent across the network, or store it for later assessment. Several layers of encryption are needed to prevent this: WEP/data-link encryption at the link layer, plus a security mechanism such as **IPsec, SSH, or SSL/TLS** at a higher layer — otherwise sent data is available to attackers. As shown in `03-wireless-encryption-wep-wpa-wpa2-wpa3.md`, WEP can be cracked with freely available tools; accessing email over **POP** or **IMAP** is especially risky because these protocols can send credentials/mail over a wireless network with no extra encryption. A skilled attacker can log gigabytes of WEP-protected traffic, post-process it, and break the encryption offline.

### Manipulation
Manipulation is a level beyond eavesdropping — the attacker receives the victim's encrypted data, manipulates it, and retransmits the manipulated packets to the victim. In addition, an attacker can intercept packets encrypted with WEP/WPA and change the destination information to forward the packets across the Internet.

### Conceptual MITM Flow (6 steps)
1. Attacker **sniffs** the victim's wireless parameters (MAC address, ESSID/BSSID, number of channels).
2. Attacker sends a **deauthentication (deauth) request** to the victim with the spoofed source address of the victim's real AP.
3. Victim is deauthenticated and starts to search all channels for a new, valid AP.
4. Attacker sets a **forged AP** on a new channel using the **original MAC address (BSSID) and ESSID** of the victim's real AP.
5. After the victim successfully associates with the forged AP, the attacker spoofs the victim to connect through to the **original** AP.
6. Attacker now sits in between the real AP and the victim, **listening to all traffic** passing both directions.

## MITM Attack Using Aircrack-ng

A practical, tool-driven version of the flow above:

```bash
# Step 1 — monitor mode
airmon-ng start eth1

# Step 2 — discover SSIDs on the interface
airodump-ng --ivs --write capture eth1
# Example output includes BSSID / ESSID pairs such as:
#   1E:64:51:3B:FF:3E   SECRET_SSID   (WEP, channel 11)

# Step 3 — de-authenticate (deauth) the target client
aireplay-ng -0 5 -a 02:24:2B:CD:68:EE

# Step 4 — associate your wireless card (fake association) with the target AP
aireplay-ng -1 0 -e SECRET_SSID -a 1e:64:51:3b:ff:3e -h 02:24:2B:CD:68:EE eth1
```

Expected output on success:
```
Waiting for beacon frame (BSSID: 1E:64:51:3B:FF:3E) on channel 11
Sending Authentication Request
Authentication successful
Sending Association Request
Association successful :-)
```

**Command flag reference:**
| Flag | Meaning |
|---|---|
| `-0 <n>` | Deauthentication mode, send `n` packets |
| `-a <bssid>` | Target access point's BSSID |
| `-1 0` | Fake authentication, reassociation timing 0 |
| `-e <essid>` | Target network's ESSID |
| `-h <mac>` | Your card's spoofed source MAC (matches the victim you're impersonating) |

## MAC Spoofing Attack

A MAC address is a unique identifier hard-coded into a network card's circuit by its manufacturer. Some networks implement **MAC address filtering** as a security control. In MAC spoofing, attackers change their MAC address to match that of an authenticated user, bypassing the filter. To spoof a MAC address, an attacker sets the value ifconfig returns to another hex value in the format `aa:bb:cc:dd:ee:ff`; this typically requires root/sudo.

```bash
# Linux MAC spoofing
ifconfig wlan0 down                          # log in as root, disable the interface
ifconfig wlan0 hw ether 02:25:ab:4c:2a:bc     # set the new MAC address
ifconfig wlan0 up                             # bring the interface back up
```
*(Modern distros: the equivalent with `iproute2` is `ip link set wlan0 down`, `ip link set wlan0 address 02:25:ab:4c:2a:bc`, `ip link set wlan0 up`.)*

### MAC Spoofing Tools

**Technitium MAC Address Changer** — https://technitium.com
Allows a user to instantly change (spoof) their NIC's MAC address via a simple UI, and shows information about each NIC in the machine. Displays original vs. active MAC, hardware ID, link status/speed, and lets the user pick a random MAC or one from a specific vendor's OUI range, with an option to make the change persistent across reboots.

Other tools: **LizardSystems Change MAC Address** — used similarly on Windows to change the MAC address.

## Wireless ARP Poisoning Attack

ARP determines the MAC address of a device on the LAN given its IP address. Normally, ARP has no built-in feature to verify whether responses come from valid hosts. **ARP poisoning** exploits this lack of verification: an attacker corrupts the ARP cache maintained by the OS with wrong MAC-to-IP mappings, by sending a crafted ARP reply constructed with a false MAC address.

An ARP poisoning attack impacts **all hosts in a subnet** — every station associated with the subnet is vulnerable because most APs act as transparent MAC-layer bridges. Any host connected to a switch/hub directly attached to that AP, with no router/firewall in between, is susceptible.

**Attack flow** *(Figure 16.51)*:
1. Attacker's system spoofs the MAC address of the victim's ("Jessica's") wireless laptop and attempts to authenticate to AP1.
2. AP1 sends the updated MAC address information to the network's routers and switches, which update their routing/switching tables accordingly.
3. Traffic that was destined for the victim's system (via AP2) is now no longer sent to AP2 — it flows to the attacker instead.

Attackers use ARP poisoning tools such as **arpspoof** to perform this attack.

## ARP Poisoning Attack Using Ettercap

**Source:** https://www.ettercap-project.org

Attackers use Ettercap to identify the MAC addresses of clients and routers to perform various attacks — ARP poisoning, sniffing, and MITM. Using this tool, an attacker can obtain all network-traffic information about a victim.

**Steps:**
1. **Launch** the Ettercap graphical interface and enable unified sniffing: `Sniff → Unified Sniffing`. This lets the attacker bridge the connection and sniff traffic crossing the interfaces.
2. In the Ettercap **Setup** pop-up window, set the **Primary Interface** to sniff (e.g., `enp0s3`), and click **OK**. This reveals advanced menu options: Targets, Hosts, MITM, Plugins.
3. Identify the target host(s): `Hosts → Scan for Hosts`. Ettercap scans all live hosts on the network and displays a host list. Then `Hosts → Hosts List` to view them (IP / MAC / Description columns).
4. `View → Connections` to start snooping identified connections. Filter connections by IP address, protocol (TCP/UDP/Other), and connection state (Active/Idle/Closing/Closed/Killed).
5. Go to the **Hosts** window and select the target IP address(es); `Targets → Current targets` to add them to the target list for ARP spoofing.
6. `MITM → ARP poisoning`. In the resulting pop-up, select **Sniff remote connections** and click **OK** to launch the ARP poisoning attack.

**Note:** once the attack is running, if the target host's web traffic isn't encrypted with HTTPS, their login credentials can be sniffed in plaintext directly from the intercepted stream.

---
**Previous:** [`06-wireless-traffic-analysis.md`](06-wireless-traffic-analysis.md)
**Next:** [`08-rogue-ap-evil-twin-krack-advanced-attacks.md`](08-rogue-ap-evil-twin-krack-advanced-attacks.md) — rogue APs, evil twins, KRACK, jamming, and other advanced attacks.
